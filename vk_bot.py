import random
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
from environs import Env
from google.cloud import dialogflow

env=Env()
env.read_env()

VK_BOT_TOKEN = env("VK_BOT_TOKEN")
VK_BOT_ID = env("VK_BOT_ID")
GOOGLE_APPLICATION_CREDENTIALS = env("GOOGLE_APPLICATION_CREDENTIALS")
PROJECT_ID = env("PROJECT_ID")


def echo(event, vk_api):
    vk_api.messages.send(
        user_id=event.user_id,
        message=event.text,
        random_id=random.randint(1,1000)
    )

def detect_intent_texts(project_id, session_id, event_text):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.TextInput(text=event_text, language_code="ru")
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(request={"session": session, "query_input": query_input})
    vk_api.messages.send(user_id=event.user_id, message=response.query_result.fulfillment_text, random_id=random.randint(1,1000))


if __name__ == "__main__":
    vk_session = vk.VkApi(token=VK_BOT_TOKEN)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            detect_intent_texts(PROJECT_ID, VK_BOT_ID, event.text)
