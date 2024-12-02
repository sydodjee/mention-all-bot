import os
import logging
from telegram import Bot, Update
from telegram.ext import CommandHandler, MessageHandler, Application, filters
from flask import Flask, request
from database import BotDatabase

# Инициализация базы данных
db = BotDatabase('database.db')

# Устанавливаем токен из переменной окружения
TOKEN = os.getenv('TGBOT_TOKEN')

# Настроим логирование
logging.basicConfig(filename='logs.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Создаем объект бота
bot = Bot(token=TOKEN)

# Создаем объект Flask приложения
app = Flask(__name__)

# Команда /start - Приветствие
def start_command(update, context):
    message = 'Привет! Я могу упомянуть всех участников в чате. Используй /in, чтобы подписаться, и /all, чтобы упомянуть всех.'
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

# Команда /in - Подписка на упоминания
def in_command(update, context):
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    chat_id = update.effective_chat.id
    db.add_user(user_id, username)
    db.add_user_to_chat(chat_id, user_id)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Вы подписались на упоминания!")

# Команда /out - Отписка от упоминаний
def out_command(update, context):
    user_id = update.message.from_user.id
    chat_id = update.effective_chat.id
    db.delete_user_from_chat(chat_id, user_id)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Вы отписались от упоминаний!")

# Команда /all - Упоминание всех подписанных
def all_command(update, context):
    chat_id = update.effective_chat.id
    users = db.get_users_from_chat(chat_id)
    if users:
        mentions = [f"@{user[1]}" for user in users]  # Составляем список упоминаемых пользователей
        message = " ".join(mentions)
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Нет подписанных пользователей для упоминания.")

# Обработчики команд
handlers = [
    CommandHandler('start', start_command),
    CommandHandler('in', in_command),
    CommandHandler('out', out_command),
    CommandHandler('all', all_command),
]

# Создаем объект Application (замена Dispatcher)
application = Application.builder().token(TOKEN).build()

# Добавляем обработчики команд в приложение
for handler in handlers:
    application.add_handler(handler)

# Вебхук для обработки сообщений
@app.route('/webhook', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = Update.de_json(json_str, bot)
    application.process_update(update)
    return 'ok'

# Устанавливаем вебхук на URL, предоставленный Render
webhook_url = 'https://mention-all-bot.onrender.com/webhook'  # Замените на URL вашего приложения на Render
application.bot.set_webhook(url=webhook_url)

# Запускаем приложение
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)
