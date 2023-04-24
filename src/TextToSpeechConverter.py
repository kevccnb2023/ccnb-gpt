from gtts import gTTS
import tempfile
import pygame
import time
import os
from playsound import playsound
from google.cloud import texttospeech
from google.oauth2 import service_account

class TextToSpeechConverter:
    def __init__(self, language: str):
        self.language = language
        self.client = texttospeech.TextToSpeechClient.from_service_account_json("/home/evo/Programming/google_key.json")

    def convert(self, text):
        input_text = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(
            language_code=self.language,
            ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
            name="en-US-Wavenet-F")
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3)

        response = self.client.synthesize_speech(
            input=input_text, voice=voice, audio_config=audio_config)

        # Create a temporary directory for storing the MP3 file
        temp_dir = tempfile.mkdtemp()

        # Generate a temporary file path within the temporary directory
        file_path = os.path.join(temp_dir, 'output.mp3')

        # Write the audio content to the temporary file
        with open(file_path, 'wb') as f:
            f.write(response.audio_content)

        # Play the audio file
        self.play_sound(file_path)

        # Remove the temporary directory and its contents
        os.remove(file_path)
        os.rmdir(temp_dir)

    def play_sound(self, file_path: str) -> None:
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        time.sleep(0.5)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        pygame.mixer.quit()