from google.cloud import dialogflow
from environs import Env
import json

env = Env()
env.read_env()
project_id = env("PROJECT_ID")
telegram_user_id = env("TELEGRAM_USER_ID")

def detect_intent_texts(text, session_id):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.TextInput(text=text, language_code="ru")
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(request={"session": session, "query_input": query_input})
    return response


def create_intent(project_id):
    with open("questions.json", "r", encoding="utf-8") as questions:
        questions = questions.read()

    questions = json.loads(questions)
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