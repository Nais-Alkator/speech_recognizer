from dialogflow_api import create_intents
from environs import Env


if __name__ == "__main__":
    env = Env()
    env.read_env()
    project_id = env("PROJECT_ID")
    create_intents(project_id)