import random
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
from environs import Env
from logging_handlers import TelegramLogsHandler
from dialogflow_api import detect_intent_texts
import logging

logger = logging.getLogger("Логер")


def send_vk_message(text, vk_api, vk_bot_id):
    response = detect_intent_texts(text, vk_bot_id)
    if response.query_result.intent.is_fallback:
        return None
    else:
        vk_api.messages.send(user_id=event.user_id, message=response.query_result.fulfillment_text,
                             random_id=random.randint(1,1000))


if __name__ == "__main__":
    env = Env()
    env.read_env()
    vk_bot_token = env("VK_BOT_TOKEN")
    telegram_bot_token = env("TELEGRAM_BOT_TOKEN")
    telegram_user_id = env("TELEGRAM_USER_ID")
    vk_bot_id = env("VK_BOT_ID")
    logger.setLevel(logging.DEBUG)
    logger.addHandler(TelegramLogsHandler(telegram_user_id, telegram_bot_token))
    logger.info("Бот ВКонтакте запущен")

    try:
        vk_session = vk.VkApi(token=vk_bot_token)
        vk_api = vk_session.get_api()
        longpoll = VkLongPoll(vk_session)
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                send_vk_message(event.text, vk_api, vk_bot_id)
    except Exception as error:
        logger.exception(f"Бот ВКонтакте упал с ошибкой: {error}")
