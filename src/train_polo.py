from langchain.memory import ConversationBufferMemory
import requests
from prompt import DIMA_POLO_PROMPT

# Initialize your API key and endpoint
YOUR_API_KEY = "AIzaSyAvb5Av5gKbV0lV4HwkEpiuFopLtGBRZd4"
url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={YOUR_API_KEY}'

# Messages
USER_MSG_END_TOKEN = "<USER_END_OF_MSG>"
ERROR_MSG = "Статус розыгрыша.........загрузка......89%............ катастрофически высокий шанс розыгрыша от Дима более чем на 50к"

# Set up 
DEBUG = True
headers = {
    'Content-Type': 'application/json',
}

# Initialize LangChain's conversation memory
memory = ConversationBufferMemory()

system_prompt = {"role": "user", "parts": [{"text": DIMA_POLO_PROMPT}]}

def ask_gemini(question):
    # Format conversation history for API, with each entry having a "role" and "content"
    conversation_history = memory.load_memory_variables({})
    convo_with_history = "History:\n" + conversation_history["history"]
    convo_with_question = convo_with_history + "\n" + "Human: " + question

    conversation = [system_prompt, {"role": "user", "parts": [{"text": convo_with_question}] } ]
    
    if DEBUG:
        print("Sending conversation to Gemini: \n", conversation)
    
    # Set up data for the API request
    data = {
        "contents": conversation
    }

    # Make API request
    response = requests.post(url, headers=headers, json=data)

    # Check if the request was successful
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        print("Response content:", response.text)
        return ERROR_MSG
    
    if DEBUG:
        print(f"Response from Gemini Client: {response.json()}")
    
    content = response.json()["candidates"][0].get("content")
    if not content:
        return ERROR_MSG 
    
    answer = content["parts"][0]["text"]
    last_answer = answer.split("AI:")[-1].split("Дмитрий:")[-1]
    memory.save_context(inputs={"input": question}, outputs={"output": last_answer})
    return last_answer

# # Example of usage
# ask_gemini("Привет! Как работает искусственный интеллект?")
# ask_gemini("О чем мы только что говорили?.")
