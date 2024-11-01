from typing import Dict, List, Optional
import google.generativeai as genai
import os
import logging

class GeminiClient:
    def __init__(self):
        # Configure the API with your key
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])
        # Initialize the model
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    async def generate_response(self, conversation: List[Dict]) -> Optional[str]:
        try:
            # Convert conversation format if needed
            prompt = self._format_conversation(conversation)
            
            # Generate content using the model
            response = self.model.generate_content(prompt)
            
            return response.text
            
        except Exception as e:
            logging.error(f"Gemini API error: {str(e)}")
            return None
            
    def _format_conversation(self, conversation: List[Dict]) -> str:
        """Convert conversation format to a string prompt if needed"""
        # If the conversation is already in the correct format, return the last message
        if len(conversation) > 0:
            return conversation[-1].get("parts", [{}])[0].get("text", "")
        return ""