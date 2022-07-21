from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters
from telegram import Update
import logging
from environs import Env
from google.cloud import dialogflow
from json import loads


env=Env()
env.read_env()

TELEGRAM_BOT_TOKEN = env('TELEGRAM_BOT_TOKEN')
TELEGRAM_ID = env("TELEGRAM_ID")
GOOGLE_APPLICATION_CREDENTIALS = env("GOOGLE_APPLICATION_CREDENTIALS")
PROJECT_ID = env("PROJECT_ID")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


def detect_intent_texts(update: Update, context: CallbackContext, project_id=PROJECT_ID, session_id=TELEGRAM_ID):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.TextInput(text=update.message.text, language_code="ru")
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(request={"session": session, "query_input": query_input})
    context.bot.send_message(chat_id=update.effective_chat.id, text=response.query_result.fulfillment_text)


def create_intent(project_id):
    with open("questions.json", "r", encoding="utf-8") as my_file:
        questions = my_file.read()

    questions = loads(questions)
    intent_name = "Устройство на работу"
    training_phrases_parts = questions[intent_name]["questions"]
    answer = questions[intent_name]["answer"]
    intents_client = dialogflow.IntentsClient()
    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []

    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=[answer])
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(display_name=intent_name, training_phrases=training_phrases, messages=[message])
    response = intents_client.create_intent(request={"parent": parent, "intent": intent})


if __name__ == "__main__":
    updater = Updater(token=TELEGRAM_BOT_TOKEN)
    dispatcher = updater.dispatcher
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    response_handler = MessageHandler(Filters.text & (~Filters.command), detect_intent_texts)
    dispatcher.add_handler(response_handler)
    updater.start_polling()