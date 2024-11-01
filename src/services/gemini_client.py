from typing import Dict, List, Optional
import requests
from config import get_settings
import logging

class GeminiClient:
    def __init__(self):
        self.settings = get_settings()
        self.headers = {"Content-Type": "application/json"}
        self.url = f"{self.settings.GEMINI_URL}?key={self.settings.GEMINI_API_KEY}"

    async def generate_response(self, conversation: List[Dict]) -> Optional[str]:
        try:
            response = requests.post(
                self.url,
                headers=self.headers,
                json={"contents": conversation}
            )
            response.raise_for_status()
            
            content = response.json()["candidates"][0].get("content")
            if not content:
                return None
                
            return content["parts"][0]["text"]
            
        except Exception as e:
            logging.error(f"Gemini API error: {str(e)}")
            logging.error(f"Response: {response.json()}")
            return None 