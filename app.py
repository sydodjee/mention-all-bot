import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from database import BotDatabase

# Настроим логирование
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Получаем токен из переменных окружения
TOKEN = os.getenv("BOT_TOKEN")
db = BotDatabase()

async def start(update: Update, context: CallbackContext):
    """Команда /start"""
    await update.message.reply_text("Привет! Используйте /in, чтобы добавиться в список.")

async def in_command(update: Update, context: CallbackContext):
    """Добавить пользователя в список"""
    user = update.effective_user
    chat_id = update.effective_chat.id

    db.add_user(user.id, user.username or user.first_name)
    db.add_user_to_chat(chat_id, user.id)

    await update.message.reply_text(f"{user.first_name}, вы добавлены в список!")

async def out_command(update: Update, context: CallbackContext):
    """Удалить пользователя из списка"""
    user = update.effective_user
    chat_id = update.effective_chat.id

    db.delete_user_from_chat(chat_id, user.id)

    await update.message.reply_text(f"{user.first_name}, вы удалены из списка!")

async def all_command(update: Update, context: CallbackContext):
    """Упомянуть всех участников чата"""
    chat_id = update.effective_chat.id
    users = db.get_users_from_chat(chat_id)

    if not users:
        await update.message.reply_text("Список пуст. Добавьтесь с помощью команды /in.")
    else:
        mentions = [f"@{username}" for _, username in users if username]
        await update.message.reply_text(" ".join(mentions))

async def main():
    """Главная функция для запуска бота"""
    application = Application.builder().token(TOKEN).build()

    # Регистрация команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("in", in_command))
    application.add_handler(CommandHandler("out", out_command))
    application.add_handler(CommandHandler("all", all_command))

    # Запуск бота в фоновом режиме
    await application.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
