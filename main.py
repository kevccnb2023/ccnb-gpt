import cv2

import sqlite3
import speech_recognition as sr
from gtts import gTTS
import tempfile
import openai
import pygame
import numpy as np
import threading
import multiprocessing
import os
from dotenv import load_dotenv

from src.SpeechRecognizer import SpeechRecognizer
from src.TextToSpeechConverter import TextToSpeechConverter
from src.CommandProcessor import CommandProcessor
from src.VideoCapture import VideoCapture


from src.Utils import Utils
load_dotenv()  # Load environment variables from the .env file

class DigitalAssistant:
    def __init__(self, db_file, speech_recognizer: SpeechRecognizer, text_to_speech_converter: TextToSpeechConverter):
        self.db_file = db_file
        self.cp = CommandProcessor()
        self.speech_recognizer = speech_recognizer
        self.text_to_speech_converter = text_to_speech_converter
        self.known_face_encodings = []
        self.known_face_names = []
        self.load_known_faces()

    # Load known faces from the SQLite database
    def load_known_faces(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("SELECT name, metadata FROM facialrecognition")
        rows = cursor.fetchall()
        for name, face_encoding in rows:
            self.known_face_names.append(name)
            self.known_face_encodings.append(np.frombuffer(face_encoding))
        conn.close()


    def listen_and_process(self):
        while True:
            print("listening for wake word")
            text = self.speech_recognizer.listen()
            
            if text and "hey you" in text.lower():
                print("listening for question")
                question = self.speech_recognizer.listen()
                print("done listening for question")
                if question:
                    answer = self.answer_query(question)
                    self.text_to_speech_converter.convert(answer)
                else:
                    print("could not understand question")

    # Answer the query using GPT
    def answer_query(self, query):
        # Send the query as a message
        self.cp.send_message(query)

        # Get the response
        answer = self.cp.get_response().strip()
        return answer
    
    def play_sound(self, file_path):
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        pygame.mixer.quit()

    # Convert text to speech
    def text_to_speech(self, text):
        tts = gTTS(text, lang="en")
        with tempfile.NamedTemporaryFile(delete=True) as fp:
            tts.save(f"{fp.name}.mp3")
            self.play_sound(f"{fp.name}.mp3")

    
    # Convert speech to text
    def speech_to_text(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            audio = r.listen(source)

        try:
            print("Recognizing...")
            text = r.recognize_google(audio, language="en-US")
            return text
        except Exception as e:
            print("Error:", e)
            return None

    def run(self):
        frame_queue = multiprocessing.Queue(maxsize=10)
        result_queue = multiprocessing.Queue(maxsize=10)

        detector_thread = threading.Thread(target=self.listen_and_process)
        detector_thread.start()

        video_process = multiprocessing.Process(target=Utils.video_capture_loop, args=(self, frame_queue))
        video_process.start()

        num_procs = multiprocessing.cpu_count() - 1
        procs = []
        for i in range(num_procs):
            proc = multiprocessing.Process(target=Utils.face_recognition_loop, args=(self, frame_queue, result_queue))
            proc.start()
            procs.append(proc)

        while True:
            frame = result_queue.get()
            cv2.imshow('Video', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        for i in range(num_procs):
            frame_queue.put(None)

        for proc in procs:
            proc.join()

        detector_thread.join()

def main():
    db_file = "./users.db"

    speech_recognizer = SpeechRecognizer("en-US")
    text_to_speech_converter = TextToSpeechConverter("en")

    assistant = DigitalAssistant(db_file, speech_recognizer, text_to_speech_converter)

    try:
        assistant.run()
    except KeyboardInterrupt:
        print("Terminating child processes...")
        for proc in multiprocessing.active_children():
            proc.terminate()
            proc.join()
# def main():
#     db_file = "./users.db"

#     assistant = DigitalAssistant(db_file)

#     try:
#         assistant.run()
#     except KeyboardInterrupt:
#         print("Terminating child processes...")
#         for proc in multiprocessing.active_children():
#             proc.terminate()
#             proc.join()
   

if __name__ == "__main__":
    main()