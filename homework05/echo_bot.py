import telebot

access_token = '794825197:AAG5OCLESmv0r_M1tUw0zJ3mWUYDE7yhJz8'
bot = telebot.TeleBot(access_token)

@bot.message_handler(content_types=['text'])
def echo(message):
    bot.send_message(message.chat.id, message.text)

if __name__ == '__main__':
    bot.polling(none_stop=True)

