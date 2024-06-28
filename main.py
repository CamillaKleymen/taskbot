import telebot
from telebot.types import Message
from database import TaskDatabase

# Замените 'YOUR_BOT_TOKEN' на токен вашего бота
bot = telebot.TeleBot('7072243317:AAHbAk1UNvanLlGH5vD32yrKMq8qMN4GoYY')

# Инициализация базы данных
db = TaskDatabase()

@bot.message_handler(commands=['start'])
def start(message: Message):
    bot.reply_to(message, 'Привет! Я бот для управления задачами. '
                          'Используй /add для добавления задачи, /list для просмотра задач и '
                          '/done для отметки задачи как выполненной.')

@bot.message_handler(commands=['add'])
def add_task(message: Message):
    user_id = message.from_user.id
    task_description = message.text.replace('/add', '').strip()
    if not task_description:
        bot.reply_to(message, 'Пожалуйста, укажите описание задачи после команды /add.')
        return
    task_id = db.add_task(user_id, task_description)
    bot.reply_to(message, f'Задача добавлена с ID: {task_id}')

@bot.message_handler(commands=['list'])
def list_tasks(message: Message):
    user_id = message.from_user.id
    tasks = db.get_tasks(user_id)
    if not tasks:
        bot.reply_to(message, 'У вас пока нет задач.')
        return
    task_list = '\n'.join([f"{task[0]}. {task[2]} - {'Выполнено' if task[3] == 'completed' else 'В процессе'}" for task in tasks])
    bot.reply_to(message, f'Ваши задачи:\n{task_list}')

@bot.message_handler(commands=['done'])
def mark_done(message: Message):
    user_id = message.from_user.id
    try:
        task_id = int(message.text.split()[1])
    except (IndexError, ValueError):
        bot.reply_to(message, 'Пожалуйста, укажите ID задачи после команды /done.')
        return
    if db.mark_task_done(task_id, user_id):
        bot.reply_to(message, f'Задача {task_id} отмечена как выполненная.')
    else:
        bot.reply_to(message, f'Задача {task_id} не найдена или уже выполнена.')

def main():
    print("Бот запущен...")
    bot.polling(none_stop=True)

if __name__ == '__main__':
    main()