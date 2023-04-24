import openai
import os
from dotenv import load_dotenv

class CommandProcessor:
    def __init__(self, model="gpt-3.5-turbo", initial_message="You are a helpful assistant."):
        load_dotenv()
        self.model = model
        self.messages = [{"role": "system", "content": initial_message}]
        self.api_key = os.getenv("OPENAI_API_KEY")
        openai.api_key = self.api_key

    def set_role(self, initial_message):
        self.messages[0] = {"role": "system", "content": initial_message}

    def send_message(self, message):
        self.messages.append({"role": "user", "content": message})

    def get_response(self, temperature=0.7, presence_penalty=0, frequency_penalty=0, n=1):
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=self.messages,
            temperature=temperature,
            presence_penalty=presence_penalty,
            frequency_penalty=frequency_penalty,
            n=n,
        )
        self.messages.append({"role": "assistant", "content": response.choices[0].message.content})
        return response.choices[0].message.content