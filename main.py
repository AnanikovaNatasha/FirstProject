import telebot
import nn
import os


TOKEN = ''

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start_help_handler(message):
    bot.send_message(message.from_user.id,  "Привет, отправь сюда картинку, а я тебе отвечу, кошка или собака на ней")


@bot.message_handler(content_types=['photo'])
def photo_handler(message):
    user_id = message.from_user.id
    user_first_name = message.from_user.first_name
    user_last_name = message.from_user.last_name
    """Функция обрабатывает сообщение с картинкой"""
    file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    parent_dir = "/home/nt/prgrms/FP/imges"
    derivative_directory = f'{user_first_name}_{user_last_name}_{user_id}_'
    path = os.path.join(parent_dir, derivative_directory)
    os.makedirs(path)

    name = message.photo[1].file_id + ".jpg"
    with open(f'{parent_dir}/{derivative_directory}/{name}', 'wb') as new_file:
        new_file.write(downloaded_file)

    reply = 'Фото добавлено, {}, {}, {}'
    bot.reply_to(message, reply.format(user_id, user_first_name, user_last_name))

    res = nn.predict_img_from_dir(f'{parent_dir}/{derivative_directory}', name)

    # Отправим пользователю сообщение с результатом
    reply = 'На картинке изображено{}'
    bot.reply_to(message, reply.format(res))


@bot.message_handler(func=lambda m: True)
def all_handler(message):
    """Все остальные сообщения будут попадать в эту функцию"""
    bot.send_message(message.from_user.id, "Пожалуйста, отправьте картинку")


# Запустим нашего бота
bot.polling(none_stop=True, interval=0, timeout=20)
