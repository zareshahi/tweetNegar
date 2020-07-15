# ===============================================================
# Author: Ali Zareshahi & Mohammad Pooshesh
# Email:
# Twitter:
# Telegram:
#
# ABOUT COPYING OR USING PARTIAL INFORMATION:
# This script was originally created by Ali Zareshahi & Mohammad Pooshesh. Any
# explicit usage of this script or its contents is granted
# according to the license provided and its conditions.
# ===============================================================

from telegram.ext import Updater, CommandHandler, MessageHandler, RegexHandler, ConversationHandler, Filters
from bot import *
import json


def main():
    """
    Main function.
    This function handles the conversation flow by setting
    states on each step of the flow. Each state has its own
    handler for the interaction with the user.
    """
    # use config json file to hide security API keys
    # config.json is git ignored - you can see this file template in config.template.json
    with open('./config.json') as json_file:
        config_json = json.load(json_file)
    # set telegram token updater
    telegram_token = config_json['telegram']['token']
    bot_obj = TweetNegarTelegramBot()
    bot_obj.main_bot(telegram_token)

if __name__ == '__main__':
    main()
