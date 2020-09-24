import os
from dotenv import load_dotenv


def load_env():
    is_prod = os.getenv("PROD", False)

    if is_prod:
        load_dotenv(dotenv_path="/etc/laciudadinvisible/.env", verbose=True)
    else:
        load_dotenv(dotenv_path=".env", verbose=True)
