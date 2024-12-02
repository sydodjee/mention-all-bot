# Используем официальный образ Python
FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы с зависимостями в контейнер
COPY requirements.txt /app/

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Устанавливаем дополнительные зависимости, если они нужны
RUN pip install gevent

# Копируем остальные файлы проекта в контейнер
COPY . /app

# Открываем порт 8080
EXPOSE 8080

# Указываем переменную окружения для Flask
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Запускаем приложение
CMD ["python", "app.py"]
