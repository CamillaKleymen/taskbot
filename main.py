import telebot
from telebot.types import Message
from database import TaskDatabase

# Replace 'YOUR_BOT_TOKEN' with your bot's token
bot = telebot.TeleBot('7072243317:AAHbAk1UNvanLlGH5vD32yrKMq8qMN4GoYY')

# Database initialization
db = TaskDatabase()

@bot.message_handler(commands=['start'])
def start(message: Message):
    bot.reply_to(message, 'Hello! I am a task management bot. '
                          'Use /add to add a task, /list to view tasks, and '
                          '/done to mark a task as completed.')

@bot.message_handler(commands=['add'])
def add_task(message: Message):
    user_id = message.from_user.id
    task_description = message.text.replace('/add', '').strip()
    if not task_description:
        bot.reply_to(message, 'Please specify the task description after the /add command.')
        return
    task_id = db.add_task(user_id, task_description)
    bot.reply_to(message, f'Task added with ID: {task_id}')

@bot.message_handler(commands=['list'])
def list_tasks(message: Message):
    user_id = message.from_user.id
    tasks = db.get_tasks(user_id)
    if not tasks:
        bot.reply_to(message, 'You have no tasks yet.')
        return
    task_list = '\n'.join([f"{task[0]}. {task[2]} - {'Completed' if task[3] == 'completed' else 'In progress'}" for task in tasks])
    bot.reply_to(message, f'Your tasks:\n{task_list}')

@bot.message_handler(commands=['done'])
def mark_done(message: Message):
    user_id = message.from_user.id
    try:
        task_id = int(message.text.split()[1])
    except (IndexError, ValueError):
        bot.reply_to(message, 'Please specify the task ID after the /done command.')
        return
    if db.mark_task_done(task_id, user_id):
        bot.reply_to(message, f'Task {task_id} marked as completed.')
    else:
        bot.reply_to(message, f'Task {task_id} not found or already completed.')

def main():
    print("Bot started...")
    bot.polling(none_stop=True)

if __name__ == '__main__':
    main()