from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
import os

# Инициализация Flask
app = Flask(__name__)

# Получаем токен бота из переменной окружения
TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: CallbackContext):
    """Команда /start"""
    update.message.reply_text("Привет! Используйте /in, чтобы добавиться в список.")

async def main():
    """Главная функция для запуска бота"""
    application = Application.builder().token(TOKEN).build()

    # Команды
    application.add_handler(CommandHandler("start", start))

    await application.run_polling()

# Настройка порта для Flask
@app.route('/')
def index():
    return 'Bot is running!'

if __name__ == "__main__":
    # Запуск Flask, который будет слушать на порту 8080
    from threading import Thread
    Thread(target=lambda: app.run(host="0.0.0.0", port=8080)).start()
    
    # Запуск бота
    import asyncio
    asyncio.run(main())
