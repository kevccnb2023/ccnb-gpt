import openai
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from the .env file


class ChatBot:
    def __init__(self, model="gpt-3.5-turbo", initial_message="You are a helpful assistant."):
        """
        Initialize a new ChatBot instance.

        Args:
        - model (str): The name of the GPT-3 model to use (default: "gpt-3.5-turbo").
        - initial_message (str): The initial message that the assistant will send (default: "You are a helpful assistant.").

        Returns:
        - None
        """
        # ...
        self.model = model
        self.messages = [{"role": "system", "content": initial_message}]
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.prompt_tokens_used = []
        self.completion_tokens_used = []
        self.total_tokens_used = []
        openai.api_key = self.api_key

    def set_role(self, initial_message):
        """
        Set the role of the assistant.

        Args:
        - initial_message (str): The new initial message that the assistant will send.

        Returns:
        - None
        """
        # ...
        self.messages[0] = {"role": "system", "content": initial_message}

    def send_message(self, message):
        """
        Send a message from the user to the assistant.

        Args:
        - message (str): The message text.

        Returns:
        - None
        """
        # ...
        self.messages.append({"role": "user", "content": message})

    def get_response(self, temperature=0.7, presence_penalty=0, frequency_penalty=0, n=1):
        """
        Get a response from the assistant.

        Args:
        - temperature (float): Controls the "creativity" of the response (default: 0.7).
        - presence_penalty (float): Controls the likelihood of the response repeating itself (default: 0).
        - frequency_penalty (float): Controls the likelihood of the response using a rare word (default: 0).
        - n (int): The number of responses to generate (default: 1).

        Returns:
        - str or List[str]: The generated response(s).
        """
        # ...

        response = openai.ChatCompletion.create(
            model=self.model,
            messages=self.messages,
            temperature=temperature,
            presence_penalty=presence_penalty,
            frequency_penalty=frequency_penalty,
            n=n,
        )
        usage = response.get("usage", {})
        self.prompt_tokens_used.append(usage.get("prompt_tokens", 0))
        self.completion_tokens_used.append(usage.get("completion_tokens", 0))
        self.total_tokens_used.append(usage.get("total_tokens", 0))

        self.messages.append({"role": "assistant", "content": response.choices[0].message.content})

        return response.choices[0].message.content

    def clear_messages(self):
        """
        Clear the message history and token usage.

        Args:
        - None

        Returns:
        - None
        """
        # ...
        self.messages = [{"role": "system", "content": "You are a helpful assistant."}]
        self.prompt_tokens_used = []
        self.completion_tokens_used = []
        self.total_tokens_used = []

    def get_prompt_tokens_used(self):
        """
        Get the number of tokens used for prompts in each API call.

        Args:
        - None

        Returns:
        - List[int]: A list of token counts for each API call.
        """
        # ...
        return self.prompt_tokens_used

    def get_completion_tokens_used(self):
        """
        Get the number of tokens used for completions in each API call.

        Args:
        - None

        Returns:
        - List[int]: A list of token counts for each API call.
        """
        # ...
        return self.completion_tokens_used
    
    def get_total_tokens_used(self):
        """
        Get the total number of tokens used in each API call.

        Args:
        - None

        Returns:
        - List[int]: A list of total token counts for each API call.
        """
        # ...
        return self.total_tokens_used
    