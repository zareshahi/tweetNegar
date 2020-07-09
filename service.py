import json

from telegram.ext import CommandHandler, InlineQueryHandler, Updater

from app import get_image


def post_image(bot, update):
    chat_id = update.message.chat_id
    update.message.reply_text("لطفا کمی صبر کنید")
    image = get_image(chat_id)
    bot.sendDocument(chat_id=chat_id, document=image)


def main():
    # use config json file to hide security API keys
    # config.json is git ignored - you can see this file template in config.template.json
    with open('./config.json') as json_file:
        config_json = json.load(json_file)
    # set telegram token updater
    telegram_token = config_json['telegram']['token']
    updater = Updater(telegram_token)
    # set dispacher for bot
    dp = updater.dispatcher
    # bot handlers (such: /image command)
    dp.add_handler(CommandHandler('image', post_image))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
