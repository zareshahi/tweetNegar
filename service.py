import json
from functools import wraps

from telegram import ChatAction, ReplyKeyboardMarkup
from telegram.ext import CommandHandler, InlineQueryHandler, Updater

from app import get_image


def is_typing_action(func):
    """is typing action while processing func command."""
    @wraps(func)
    def command_func(*args, **kwargs):
        bot, update = args
        bot.send_chat_action(chat_id=update.message.chat_id,
                             action=ChatAction.TYPING)
        func(bot, update, **kwargs)

    return command_func


def is_sending_action(func):
    """is sending action while processing func command."""
    @wraps(func)
    def command_func(*args, **kwargs):
        bot, update = args
        bot.send_chat_action(chat_id=update.message.chat_id,
                             action=ChatAction.UPLOAD_DOCUMENT)
        func(bot, update, **kwargs)

    return command_func


@is_sending_action
def post_image(bot, update):
    chat_id = update.message.chat_id
    image = get_image(chat_id)
    bot.sendDocument(chat_id=chat_id, document=image)


@is_typing_action
def menu(bot, update):
    """
    Main menu function.
    This will display the options from the main menu.
    """
    # Create buttons to select action:
    custom_keyboard = [['تنظیمات', 'ایجاد طرح جدید'], ['درباره ما']]

    reply_markup = ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True)
    chat_id = update.message.chat_id
    bot.send_message(
        chat_id=chat_id, text="لطفا گزینه مورد نظر را انتخاب کنید", reply_markup=reply_markup)


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
    dp.add_handler(CommandHandler('start', menu))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
