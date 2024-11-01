from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    def __init__(self):
        self.TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
        self.GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
        self.GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
        self.DEBUG = False

def get_settings() -> Settings:
    return Settings() 