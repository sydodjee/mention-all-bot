# Используем официальный образ Python
FROM python:3-slim

# Обновляем пакеты и устанавливаем libpq-dev, который необходим для работы с PostgreSQL
RUN apt-get update && apt-get install -y libpq-dev

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл с зависимостями requirements.txt в контейнер
COPY requirements.txt .

# Устанавливаем все зависимости из requirements.txt
RUN pip3 install -r requirements.txt

# Копируем остальные файлы проекта в контейнер
COPY . .

# Команда для запуска приложения
CMD [ "python3", "app.py"]
