import requests
import os
import logging
from typing import Dict, List, Optional

class GeminiClient:
    def __init__(
        self,
        temperature: float = 1.6,
        top_k: int = 40,
        top_p: float = 0.99,
        max_output_tokens: int = 2048,
        model: str = "gemini-1.5-flash-002"
    ):
        self.api_key = os.environ["GEMINI_API_KEY"]
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"
        self.model = model
        self.headers = {'Content-Type': 'application/json'}
        
        # Generation config
        self.generation_config = {
            "temperature": temperature,
            "topK": top_k,
            "topP": top_p,
            "maxOutputTokens": max_output_tokens,
        }
        
        # Safety settings
        self.safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ]
        
    async def generate_response(self, conversation: List[Dict]) -> Optional[str]:
        try:
            url = f"{self.base_url}/{self.model}:generateContent?key={self.api_key}"
            
            data = {
                "contents": conversation,
                "safetySettings": self.safety_settings,
                "generationConfig": self.generation_config
            }
            
            response = requests.post(url, headers=self.headers, json=data)
            response.raise_for_status()
            
            content = response.json()["candidates"][0].get("content")

            if response.status_code != 200 or not content:
                logging.error(f"Gemini API error: {response.status_code}")
                logging.error(f"Response: {response.text}")
                return None
        
            return content["parts"][0]["text"]
            
            
        except Exception as e:
            logging.error(f"Gemini API error: {str(e)}")
            
            try:
                logging.error(f"Response: {response.text}")
            except:
                pass

            return None
            
    # def _format_conversation(self, conversation: List[Dict]) -> List[Dict]:
    #     """No formatting needed as we're using the raw API format"""
    #     return conversation