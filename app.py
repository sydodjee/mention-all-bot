import os
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from database import BotDatabase

# Настраиваем логирование
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Получаем токен бота из переменной окружения
TOKEN = os.getenv("BOT_TOKEN")
db = BotDatabase()


def start(update: Update, context: CallbackContext):
    """Команда /start"""
    update.message.reply_text("Привет! Используйте /in, чтобы добавиться в список.")


def in_command(update: Update, context: CallbackContext):
    """Добавить пользователя в список"""
    user = update.effective_user
    chat_id = update.effective_chat.id

    db.add_user(user.id, user.username or user.first_name)
    db.add_user_to_chat(chat_id, user.id)

    update.message.reply_text(f"{user.first_name}, вы добавлены в список!")


def out_command(update: Update, context: CallbackContext):
    """Удалить пользователя из списка"""
    user = update.effective_user
    chat_id = update.effective_chat.id

    db.delete_user_from_chat(chat_id, user.id)

    update.message.reply_text(f"{user.first_name}, вы удалены из списка!")


def all_command(update: Update, context: CallbackContext):
    """Упомянуть всех участников чата"""
    chat_id = update.effective_chat.id
    users = db.get_users_from_chat(chat_id)

    if not users:
        update.message.reply_text("Список пуст. Добавьтесь с помощью команды /in.")
    else:
        mentions = [f"@{username}" for _, username in users if username]
        update.message.reply_text(" ".join(mentions))


def main():
    """Главная функция для запуска бота"""
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("in", in_command))
    dispatcher.add_handler(CommandHandler("out", out_command))
    dispatcher.add_handler(CommandHandler("all", all_command))

    updater.start_polling()
    updater.idle()

    db.close()


if __name__ == "__main__":
    main()
