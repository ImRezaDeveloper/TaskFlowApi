import os
from dotenv import load_dotenv, find_dotenv

get_env = load_dotenv(find_dotenv())

class JWTConfig:
    
    SECRET_KEY = os.environ.get("SECRET_kEY")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 20