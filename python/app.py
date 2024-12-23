from flask import Flask, request, jsonify, Response
from db import init_db, store_data, retrieve_data
from api_service import get_bitcoin_price, process_bitcoin_price
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)

metrics = PrometheusMetrics(app, group_by='endpoint')
# Инициализируем базу данных при запуске приложения
with app.app_context():
    init_db()


@app.route("/process", methods=["POST"])
def process_route():
    """Получает данные от пользователя, получает цену Bitcoin, обрабатывает и возвращает результат."""
    user_id = request.json.get("user_id")

    if not user_id:
        return jsonify({"error": "Не указан user_id"}), 400

    # Запрос к API CoinDesk
    bitcoin_data = get_bitcoin_price()
    if bitcoin_data:
        processed_data = process_bitcoin_price(bitcoin_data)
    else:
        processed_data = "Ошибка при обращении к api"

    # Сохранение в БД
    store_data(user_id, processed_data)
    return jsonify({"user_id": user_id, "processed_data": processed_data})


@app.route("/data/<user_id>", methods=["GET"])
@metrics.counter(
    'cnt_collection', 'Number of invocations per collection', labels={
        'user': lambda: request.view_args['user_id'],
        'status': lambda resp: resp.status_code
    })

def get_user_data(user_id):
    """Получает данные из базы данных по user_id."""
    data = retrieve_data(user_id)
    if data:
        return jsonify({"user_id": user_id, "data": data})
    else:
        return jsonify({"error": "Нет данных для данного user_id"}), 404



if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False)
