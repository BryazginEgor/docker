FROM python:3.11-slim-buster

WORKDIR /app

COPY python/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY python/* .

EXPOSE 5000

CMD ["python", "app.py"]
