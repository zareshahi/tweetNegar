import re

import requests
from telegram.ext import CommandHandler, InlineQueryHandler, Updater

from app import get_image


def get_url():
    contents = requests.get('https://random.dog/woof.json').json()    
    url = contents['url']
    return url

def bop(bot, update):
    url = get_url()
    chat_id = update.message.chat_id
    bot.send_photo(chat_id=chat_id, photo=url)

def hello(bot, update):
    update.message.reply_text(
        'سلام علیکم {}'.format(update.message.from_user.first_name))

def post_image(bot, update):
    chat_id = update.message.chat_id
    image = get_image(chat_id)
    bot.send_photo(chat_id=chat_id, photo=image)

def main():
    updater = Updater('1130555713:AAEfpdkRQIT7AbvjyUQfWQMZN2pzRRVwf0w')
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('bop',bop))
    dp.add_handler(CommandHandler('hello', hello))
    dp.add_handler(CommandHandler('image', post_image))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
