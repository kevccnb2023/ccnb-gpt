import time
import speech_recognition as speech
from gtts import gTTS
import pygame
from constants import AUDIO_FOLDER_LOCATION, LANGUAGE, DEFAULT_MODEL_NAME
pygame.init()
from chatbotv2.ChatBot import ChatBot

class VoiceChatbot:
    """
    A voice chatbot that uses Google Text-to-Speech (gTTS) and SpeechRecognition to
    listen and respond to user input.

    Args:
        model (str): The OpenAI model name to use (default is 'davinci').
        initial_message (str): The initial message sent by the chatbot.

    Attributes:
        chatbot (ChatBot): The ChatBot instance used by the voice chatbot.
    """
    def __init__(self, model=DEFAULT_MODEL_NAME, initial_message="You are a helpful assistant."):
        """
        Initializes the voice chatbot.

        Args:
            model (str): The OpenAI model name to use (default is 'davinci').
            initial_message (str): The initial message sent by the chatbot.
        """
        self.chatbot = ChatBot(model=model, initial_message=initial_message)

    def get_audio_input(self):
        """
        Listens for audio input from the microphone and converts it to text using Google Speech Recognition.

        Returns:
            str: The text transcription of the audio input.
        """
        recognize = speech.Recognizer()

        with speech.Microphone() as source:
            print("Talk")
            recognize.adjust_for_ambient_noise(source, duration=0.2)
            audio_text = recognize.listen(source)
            print("Done listening")

        try:
            speech_to_text_result = recognize.recognize_google(audio_text, language=LANGUAGE)
            return speech_to_text_result

        except:
            print("Sorry, I did not get that")
            return None

    def _play_audio(self, audio_file_location):
        """
        Plays the audio file at the specified location using Pygame.

        Args:
            audio_file_location (str): The file location of the audio file to play.
        """
        pygame.mixer.music.load(audio_file_location)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue

    def _save_audio(self, response, audio_folder_location):
        """
        Saves the response as an MP3 file using Google Text-to-Speech.

        Args:
            response (str): The response to convert to speech.
            audio_folder_location (str): The folder location to save the audio file.

        Returns:
            str: The file location of the saved audio file.
        """
        tts = gTTS(text=response, lang=LANGUAGE)
        generated_file_name = int(time.time())
        audio_file_location = audio_folder_location + str(generated_file_name) + ".mp3"
        tts.save(audio_file_location)
        return audio_file_location

    def get_response(self, temperature=0.7, presence_penalty=0, frequency_penalty=0, n=1):
        """
        Gets a response from the chatbot and converts it to speech for the user to hear.

        Returns:
            str: The text of the response.
        """
        response = self.chatbot.get_response(temperature, presence_penalty, frequency_penalty, n)
        audio_file_location = self._save_audio(response, AUDIO_FOLDER_LOCATION)
        self._play_audio(audio_file_location)
        return response

    def send_message(self, message):
        self.chatbot.send_message(message)

    def clear_messages(self):
        self.chatbot.clear_messages()

    def get_prompt_tokens_used(self):
        return self.chatbot.get_prompt_tokens_used()

    def get_completion_tokens_used(self):
        return self.chatbot.get_completion_tokens_used()

    def get_total_tokens_used(self):
        return self.chatbot.get_total_tokens_used()





