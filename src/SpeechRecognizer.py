import speech_recognition as sr

class SpeechRecognizer:
    def __init__(self, language: str):
        self.r = sr.Recognizer()
        self.r.pause_threshold = 1
        self.language = language

    def listen(self) -> str:
        with sr.Microphone() as source:
            print("Listening...")
            audio = self.r.listen(source)
            print("done listening")
        try:
            print("trying to recognize audio with google api")
            text = self.r.recognize_google(audio, language=self.language)
            print(f"got results back from google api! : {text}")
            return text
        except Exception as e:
            print("Error recognizing speech:", e)
            return None
