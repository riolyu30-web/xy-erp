import os
from dotenv import load_dotenv
# 加载环境变量
load_dotenv()

DEBUG_MODE = os.getenv("DEBUG_MODE", "False") == "True"


def log(msg: str):
    if DEBUG_MODE:
        print(msg)
