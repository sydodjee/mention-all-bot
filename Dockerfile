FROM python:3-slim

RUN apt-get update && apt-get install -y sqlite3

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]
