RUN apt-get update && apt-get install -y libpq-dev

FROM python:3-slim

WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "app.py"]
