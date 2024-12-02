import os
import logging
from telegram import Bot, Update
from telegram.ext import CommandHandler, MessageHandler, Filters, Dispatcher
from flask import Flask, request

# Устанавливаем токен из переменной окружения
TOKEN = os.getenv('TGBOT_TOKEN')

# Настроим логирование
logging.basicConfig(filename='logs.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Создаем объект бота
bot = Bot(token=TOKEN)

# Создаем объект Flask приложения
app = Flask(__name__)

# Обработчик команд
def start_command(update, context):
    message = 'Hello! This bot can mention all users in the chat. Use /in to opt-in and /all to mention everyone.'
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

def in_command(update, context):
    # Логика для добавления пользователя в базу
    pass

def out_command(update, context):
    # Логика для исключения пользователя
    pass

def all_command(update, context):
    # Логика для упоминания всех участников чата
    pass

# Обработчики команд
handlers = [
    CommandHandler('start', start_command),
    CommandHandler('in', in_command),
    CommandHandler('out', out_command),
    CommandHandler('all', all_command),
]

# Создаем диспетчер
dispatcher = Dispatcher(bot, None)

# Добавляем обработчики команд в диспетчер
for handler in handlers:
    dispatcher.add_handler(handler)

# Вебхук для обработки сообщений
@app.route('/webhook', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = Update.de_json(json_str, bot)
    dispatcher.process_update(update)
    return 'ok'

# Устанавливаем вебхук на URL, предоставленный Render
webhook_url = 'https://your-app-name.onrender.com/webhook'
bot.set_webhook(url=webhook_url)

# Запускаем Flask приложение
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)
