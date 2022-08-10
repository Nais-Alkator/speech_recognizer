from google.cloud import dialogflow
from environs import Env
import json


def detect_intent_texts(text, project_id, session_id):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.TextInput(text=text, language_code="ru")
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(request={"session": session, "query_input": query_input})
    return response


def create_intents(project_id):
    with open("questions.json", "r", encoding="utf-8") as questions:
        questions = questions.read()

    questions = json.loads(questions)
    for question in questions.items():
        intent_name, context = question
        training_phrases_parts = context["questions"]
        answer = context["answer"]
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