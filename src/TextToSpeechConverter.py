from gtts import gTTS
import tempfile
import pygame

class TextToSpeechConverter:
    def __init__(self, language: str):
        self.language = language

    def convert(self, text: str) -> None:
        tts = gTTS(text, lang=self.language)
        with tempfile.NamedTemporaryFile(delete=True) as fp:
            tts.save(f"{fp.name}.mp3")
            self.play_sound(f"{fp.name}.mp3")

    def play_sound(self, file_path: str) -> None:
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        pygame.mixer.quit()
