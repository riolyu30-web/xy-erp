import os
  
from dotenv import load_dotenv
import json
# 加载环境变量
load_dotenv()

DEBUG_MODE = os.getenv("DEBUG_MODE", "False") == "True"


def get_project_dir():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  


def log(msg: str):
    if DEBUG_MODE:
        print(msg)

def print_j(obj: dict)->str:
    return log(json.dumps(obj, ensure_ascii=False, indent=4))
