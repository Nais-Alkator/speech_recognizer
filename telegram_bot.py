from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters
from telegram import Update
import logging
from environs import Env
from logging_handlers import TelegramLogsHandler
from dialogflow_api import detect_intent_texts


logger = logging.getLogger("Логер")


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


def send_tg_message(update: Update, context: CallbackContext):
    response = detect_intent_texts(update.message.text, project_id, telegram_user_id)
    context.bot.send_message(chat_id=update.effective_chat.id, text=response.query_result.fulfillment_text)


def main():
    logger.setLevel(logging.DEBUG)
    logger.addHandler(TelegramLogsHandler(telegram_user_id, telegram_bot_token))
    logger.info("Бот Телеграм запущен")

    try:
        updater = Updater(token=telegram_bot_token)
        dispatcher = updater.dispatcher
        start_handler = CommandHandler('start', start)
        dispatcher.add_handler(start_handler)
        response_handler = MessageHandler(Filters.text & (~Filters.command), send_tg_message)
        dispatcher.add_handler(response_handler)
        updater.start_polling()
    except Exception as error:
        logger.exception(f"Бот Телеграм упал с ошибкой: {error}")

if __name__ == "__main__":
    env = Env()
    env.read_env()
    telegram_bot_token = env("TELEGRAM_BOT_TOKEN")
    telegram_user_id = env("TELEGRAM_USER_ID")
    project_id = env("PROJECT_ID")
    main()
