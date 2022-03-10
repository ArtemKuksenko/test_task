import os
from dotenv import load_dotenv


def load_env():
    dotenv_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../.env.config')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
