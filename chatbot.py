import logging
from time import sleep

import telegram
from telegram.ext import Updater, CommandHandler

import datetime
import random

from settings import *


class DailyBot:

    def __init__(self, token):
        logging.basicConfig(
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            level=logging.INFO,
        )
        self.logger = logging.getLogger("LOG")
        self.logger.info("Starting BOT.")
        self.updater = Updater(token, use_context=True)
        self.dispatcher = self.updater.dispatcher
        self.job = self.updater.job_queue
        self.chat_ids = CHAT_IDS
        self.job_daily = self.job.run_daily(self.send_daily, time=DAILY_TIME, days=DAYS)

        start_handler = CommandHandler("start", self.send_start)
        self.dispatcher.add_handler(start_handler)

        # daily_handler = CommandHandler("daily", self.send_daily)
        # self.dispatcher.add_handler(daily_handler)

        self.dispatcher.add_error_handler(self.error)

    @staticmethod
    def send_type_action(update, context):
        """
        Shows status typing when sending message
        """
        context.bot.send_chat_action(
            chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING
        )
        sleep(1)

    def send_start(self, update, context):
        """
        Start command to receive /start message on Telegram.
        @BOT = information about the BOT
        @update = the user info.
        """
        self.logger.info("Start command received.")
        self.logger.info(f"{update}")
        self.send_type_action(update, context)

        chat_id = update.message["chat"]["id"]
        if update.message["chat"]["type"] == "private":
            name = update.message["chat"]["first_name"]
        else:
            name = update.message["from_user"]["first_name"]

        # try:
        #     with open(START_FILE) as start_file:
        #         start_text = start_file.read()
        #         start_text = start_text.replace("{{name}}", name)
        #         context.bot.send_message(
        #             chat_id=chat_id,
        #             text=start_text,
        #             parse_mode=telegram.ParseMode.MARKDOWN,
        #         )
        # except Exception as error:
        #     self.logger.error(error)
        try:
            chat_ids = [int(i) for i in self.chat_ids]
            if chat_id not in chat_ids:
                with open("app/msg/error.md") as error:
                    error = error.read()
                    context.bot.send_message(
                        chat_id=chat_id,
                        text=error.format(chat_id),
                        parse_mode=telegram.ParseMode.MARKDOWN,
                    )
            else:
                with open("app/msg/success.md") as success:
                    success = success.read()
                    context.bot.send_message(
                        chat_id=chat_id,
                        text=success,
                        parse_mode=telegram.ParseMode.MARKDOWN,
                    )
        except Exception as error:
            self.logger.error(error)
        return 0

    def get_daily_file(self, day):
        subfile = random.randint(0,1)
        f = "msg/{}_{}.md".format(day, subfile)
        return f

    def send_daily(self, context):
        """
        Sends text on `daily.md` daily to groups on CHAT_ID
        @BOT = information about the BOT
        @update = the user info.
        """
        self.logger.info("Sending dailies")
        day = datetime.datetime.today().weekday()
        file_of_day = self.get_daily_file(day)
        chat_ids = [int(i) for i in self.chat_ids]
        self.logger.info(f"Daily file: {file_of_day}")
        for chat_id in chat_ids:
            self.logger.info(f"Sending daily to {chat_id}")
            with open(file_of_day, encoding="utf-8") as daily_file:
                daily_text = daily_file.read()
                context.bot.send_message(
                    chat_id=chat_id,
                    text=daily_text,
                    parse_mode=telegram.ParseMode.MARKDOWN,
                )
        return 0

    def text_message(self, update, context):
        self.send_type_action(update, context)

        context.bot.send_message(
            chat_id=update.message.chat_id,
            text="ok",
            parse_mode=telegram.ParseMode.MARKDOWN,
        )
        return 0

    def error(self, update, context):
        self.logger.warning(f'Update "{update}" caused error "{context.error}"')
        return 0

    def run(self):
        # Start the Bot
        self.logger.info("Polling BOT.")
        self.updater.start_polling()

        # Run the BOT until you press Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the BOT gracefully.
        self.updater.idle()
        return 0


if __name__ == "__main__":
    if TOKEN is not None:
        if PORT is not None:
            BOT = DailyBot(TOKEN)
            BOT.updater.start_webhook(
                listen="0.0.0.0",
                port=int(PORT),
                url_path=TOKEN)
            if LINK:
                BOT.updater.bot.set_webhook(LINK)
            else:
                BOT.updater.bot.set_webhook(f"https://{HEROKU_NAME}.herokuapp.com/{TOKEN}")
            BOT.updater.idle()
            print("Found a PORT to which try to set up webhook")
        else:
            # Run on local system once detected that it's not on Heroku nor ngrok
            print("Run with polling")
            BOT = DailyBot(TOKEN)
            BOT.run()
    else:
        HOUR = int(os.environ.get("HOUR"))
        MINUTE = int(os.environ.get("MINUTE"))
        print(f"Token {TOKEN}\n"
              f"Port {PORT}\n"
              f"Name {NAME}\n"
              f"Hour {HOUR}\n"
              f"Minute {MINUTE}\n")
