import speech_recognition as sr

class SpeechRecognizer:
    def __init__(self, language: str):
        self.r = sr.Recognizer()
        self.language = language

    def listen(self) -> str:
        with sr.Microphone() as source:
            print("Listening...")
            audio = self.r.listen(source)

        try:
            text = self.r.recognize_google(audio, language=self.language)
            print(f"Recognized: {text}")
            return text
        except Exception as e:
            print("Error recognizing speech:", e)
            return None
