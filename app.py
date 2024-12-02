import os
import logging
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
import asyncio

# Инициализация Flask
app = Flask(__name__)

# Настройка логирования
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Получаем токен бота из переменной окружения
TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: CallbackContext):
    """Команда /start"""
    update.message.reply_text("Привет! Используйте /in, чтобы добавиться в список.")

async def main():
    """Главная функция для запуска бота"""
    # Создаем приложение Telegram
    application = Application.builder().token(TOKEN).build()

    # Добавляем обработчики команд
    application.add_handler(CommandHandler("start", start))

    # Запускаем бота
    await application.run_polling()

# Настройка порта для Flask
@app.route('/')
def index():
    return 'Bot is running!'

# Запуск Flask и Telegram бота одновременно
def run():
    loop = asyncio.get_event_loop()

    # Запуск бота в фоновом режиме
    loop.create_task(main())

    # Запуск Flask
    app.run(host="0.0.0.0", port=8080)

if __name__ == "__main__":
    run()
