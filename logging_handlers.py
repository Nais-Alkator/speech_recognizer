import logging
from telegram import Bot


class TelegramLogsHandler(logging.Handler):
    def __init__(self, chat_id, telegram_bot_token):
        super().__init__()
        self.chat_id = chat_id
        self.bot = Bot(token=telegram_bot_token)

    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_message(self.chat_id, log_entry)