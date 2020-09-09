import logging
import telebot
from FilesInDirectory import Look

TOKEN = '1370653802:AAESm2VaGnz-BKY0-GIL29u3Cg0PjM0T9QQ'

logging.basicConfig(level=logging.INFO)

bot = telebot.TeleBot(TOKEN)

Directory = r'C:\Users\gabit\WhatTheStickerID\Users'

@bot.message_handler(commands=['update'])
def send_update(message):
    for id in Look.look_directory(Directory):
         bot.send_message(id, 'added support (sup,you message)')


@bot.message_handler(commands=['start'])
def send_start(message):
    if message.from_user.language_code == 'ru':
        bot.send_message(message.chat.id,
                         'Отправь мне стикер и я отправлю его id или отправь id стикера в формате (id: sticker_id) и я его тебе отправлю')
    else:
        bot.send_message(message.chat.id,
                         'Send me a sticker and I will send its id or send a sticker id in the format (id: sticker_id) and I will send it to you')


@bot.message_handler(content_types=['sticker'])
def send_sticker_id(message):
    if message.from_user.language_code == 'ru':
        bot.send_message(message.chat.id,
                         'Id этого стикера: ' + message.sticker.file_id + '\nЭмоджи: ' + message.sticker.emoji +
                         '\nНазвание пака: ' + message.sticker.set_name)
    else:
        bot.send_message(message.chat.id,
                         'This sticker id: ' + message.sticker.file_id + '\nemoji: ' + message.sticker.emoji +
                         '\nset name: ' + message.sticker.set_name)
    print(message.chat.id, 'sticker id: ' + message.sticker.file_id)
    if not str(message.chat.id) in Look.look_directory(Directory):
        print('send sticker reg ' + str(message.chat.id))
        file = open('{0}/{1}'.format(Directory, message.chat.id), 'w')
        file.write(message.sticker.file_id)
    else:
        file = open('{0}/{1}'.format(Directory, message.chat.id), 'a')
        file.write('\n' + message.sticker.file_id)


@bot.message_handler(content_types=['text'])
def send_sticker(message):

    # if message.chat.id == 1173441935:
    #     bot.send_message(message.chat.id, r"hi creator")
    if message.text[:3] == 'sup':
        try:
            id_and_message = message.text.split(',')
            print('SUPPORT id:' + str(message.chat.id) + ' message:' + id_and_message[1])
        except:
            print('invalid sup')
    if message.text[:4] == '2008' and message.text[5:8] == 'sup':
        message_text = message.text.split(',') #2008,sup,user_id,text
        bot.send_message(message_text[2], 'SUPPORT: ' + message_text[3])

    if message.text[:2].lower() == 'id':
        try:
            bot.send_sticker(message.chat.id, message.text[4:])
            if not str(message.chat.id) in Look.look_directory(Directory):
                print('send sticker ID reg ' + str(message.chat.id))
                file = open('{0}/{1}'.format(Directory, message.chat.id), 'w')
                file.write(message.text)
                file.close()
            else:
                file = open('{0}/{1}'.format(Directory, message.chat.id), 'a')
                file.write('\n' + message.text)
                file.close()
        except telebot.apihelper.ApiException:
            if message.from_user.language_code == 'ru':
                bot.send_message(message.chat.id, r"Прости, я незнаю стикер с этим id")
            else:
                bot.send_message(message.chat.id, r"Sorry, but I don't know this sticker ID :\ ")


if __name__ == '__main__':
    bot.polling()
# 'C:/Users\gabitovy\PycharmProjects\ThatTheStickerId/Users'
# '/home/vurdalack/Users'
