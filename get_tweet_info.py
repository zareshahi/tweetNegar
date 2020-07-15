# ===============================================================
# Author: Ali Zareshahi & Mohammad Pooshesh & SomeOneElse
# Email:
# Twitter:
# Telegram:
#
# ABOUT COPYING OR USING PARTIAL INFORMATION:
# This script was originally created by Ali Zareshahi & Mohammad Pooshesh. Any
# explicit usage of this script or its contents is granted
# according to the license provided and its conditions.
# ===============================================================

from telegram.ext import Updater, CommandHandler, MessageHandler, RegexHandler, ConversationHandler, CallbackQueryHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ChatAction, ReplyKeyboardMarkup, ReplyKeyboardRemove
from functools import wraps
from app import get_image
import logging
import json

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)

# Global vars:
MENU, SET_STAT, GET_LINK = range(3)
STATE = MENU


def action_status(action_type):

    def is_typing_or_sending_action(func):
        """is typing or sending action while processing func command."""
        @wraps(func)
        def command_func(*args, **kwargs):

            bot, update = args
            if action_type == "typing":
                bot.send_chat_action(chat_id=update.message.chat_id,
                                     action=ChatAction.TYPING)
            elif action_type == "sending":
                bot.send_chat_action(chat_id=update.message.chat_id,
                                     action=ChatAction.UPLOAD_DOCUMENT)
            func(bot, update, **kwargs)

        return command_func

    return is_typing_or_sending_action


@action_status("sending")
def image_builder(bot, update):
    chat_id = update.message.chat_id
    image = get_image(chat_id)
    bot.sendDocument(chat_id=chat_id, document=image)


@action_status("typing")
def start(bot, update):
    """
    Start function. Displayed whenever the /start command is called.
    This function is for base menu of the bot.
    """
    # Create buttons to slect menu:
    keyboard = [['تنظیمات', 'ایجاد طرح جدید'], ['درباره ما']]

    # Create initial message:
    message = "سلام من توییت نگارم. چه کمکی میتونم بهت بکنم؟"

    reply_markup = ReplyKeyboardMarkup(keyboard,
                                       one_time_keyboard=True,
                                       resize_keyboard=True)
    update.message.reply_text(message, reply_markup=reply_markup)

    return MENU


@action_status("typing")
def menu(bot, update):
    global STATE
    global Select
    Select = update.message.text
    user = update.message.from_user

    logger.info("Select option by {} to {}.".format(user.first_name, Select))

    if update.message.text == 'ایجاد طرح جدید':
        update.message.reply_text("لطفا لینک توییت خود را وارد کنید",
                                  reply_markup=ReplyKeyboardRemove())
        return GET_LINK

    elif update.message.text == 'تنظیمات':
        update.message.reply_text("لطفا گزینه مورد نظر را انتخاب کنید",
                                  reply_markup=ReplyKeyboardRemove())
        return MENU

    elif update.message.text == 'درباره ما':
        about_bot(bot, update)

    else:
        return MENU


@action_status("typing")
def get_link(bot, update):
    user = update.message.from_user
    logger.info("user {} send tweet link.".format(user.first_name))
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)
    return


@action_status("typing")
def about_bot(bot, update):
    """
    About function. Displays info about DisAtBot.
    """
    user = update.message.from_user
    logger.info("About info requested by {}.".format(user.first_name))
    text = """
    ربات توییت نگار اولین ربات طراحی و ایجاد تصاویر جذاب برای توییت های شما است.
    """
    update.message.reply_text(text,
                              reply_markup=ReplyKeyboardRemove())
    return


@action_status("typing")
def help(bot, update):
    """
    Help function.
    This displays a set of commands available for the bot.
    """
    user = update.message.from_user
    logger.info("User {} asked for help.".format(user.first_name))
    update.message.reply_text("help_info[LANG]",
                              reply_markup=ReplyKeyboardRemove())


@action_status("typing")
def cancel(bot, update):
    """
    User cancelation function.
    Cancel conersation by user.
    """
    user = update.message.from_user
    logger.info("User {} canceled the conversation.".format(user.first_name))
    update.message.reply_text("ممنون که ما رو انتخاب کردی",
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


@action_status("typing")
def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    """
    Main function.
    This function handles the conversation flow by setting
    states on each step of the flow. Each state has its own
    handler for the interaction with the user.
    """
    # use config json file to hide security API keys
    # config.json is git ignored - you can see this file template in
    # config.template.json
    with open('./config.json') as json_file:
        config_json = json.load(json_file)
    # set telegram token updater
    telegram_token = config_json['telegram']['token']
    updater = Updater(telegram_token)
    dp = updater.dispatcher

    # Add conversation handler with predefined states:
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            MENU: [RegexHandler('^(تنظیمات|ایجاد طرح جدید|درباره ما)$', menu)],
            GET_LINK: [MessageHandler(Filters.text, get_link)]
        },

        fallbacks=[CommandHandler('cancel', cancel),
                   CommandHandler('help', help)]
    )

    dp.add_handler(conv_handler)

    # Log all errors:
    dp.add_error_handler(error)

    # Start DisAtBot:
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process
    # receives SIGINT, SIGTERM or SIGABRT:
    updater.idle()


if __name__ == '__main__':
    main()
