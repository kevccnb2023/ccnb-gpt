import face_recognition
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

load_dotenv()  # Load environment variables from the .env file

def process_frame(frame, known_face_encodings, known_face_names):
    frame_rgb = frame

    face_locations = face_recognition.face_locations(frame_rgb)
    face_encodings = face_recognition.face_encodings(frame_rgb, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = 'Unknown'

            if True in matches:
                index = matches.index(True)
                name = known_face_names[index]

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

    return frame

def video_capture_loop(face_recognizer, frame_queue):
    video_capture = cv2.VideoCapture(0)
    frame_count = 0
    frame_modulus = 1  # Change this to 3 if you want to add every 3rd frame

    while True:
        ret, frame = video_capture.read()
        frame_count += 1
        if not ret:
            break

        if frame_count % frame_modulus == 0:
            frame_queue.put(frame)

    video_capture.release()

def face_recognition_loop(face_recognizer, frame_queue, result_queue):
    while True:
        frame = frame_queue.get()
        if frame is None:
            break

        # Process the frame using the face_recognizer object
        process_frame(frame, face_recognizer.known_face_encodings, face_recognizer.known_face_names)

        result_queue.put(frame)

class CommandProcessor:
    def __init__(self, model="gpt-3.5-turbo", initial_message="You are a helpful assistant."):
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
    
class DigitalAssistant:
    def __init__(self, db_file):
        self.db_file = db_file

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
        r = sr.Recognizer()

        while True:
            with sr.Microphone() as source:
                print("Waiting for the wake word...")
                audio = r.listen(source)

            try:
                text = r.recognize_google(audio, language="en-US")
                print(f"Recognized: {text}")

                # Check for the wake word
                if "hey you" in text.lower():
                    print("Wake word detected, listening for a question...")
                    with sr.Microphone() as source:
                        audio = r.listen(source)

                    try:
                        question = r.recognize_google(audio, language="en-US")
                        print(f"Question: {question}")

                        # Get an answer from GPT and convert it to speech
                        answer = self.answer_query(question)
                        print(f"Answer: {answer}")
                        self.text_to_speech(answer)
                    except Exception as e:
                        print("Error recognizing the question:", e)

            except Exception as e:
                print("Error recognizing the wake word:", e)

    # Answer the query using GPT
    def answer_query(self, query):
        # Create an instance of CommandProcessor
        cp = CommandProcessor()

        # Send the query as a message
        cp.send_message(query)

        # Get the response
        answer = cp.get_response().strip()
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

        video_process = multiprocessing.Process(target=video_capture_loop, args=(self, frame_queue))
        video_process.start()

        num_procs = multiprocessing.cpu_count() - 1
        procs = []
        for i in range(num_procs):
            proc = multiprocessing.Process(target=face_recognition_loop, args=(self, frame_queue, result_queue))
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

    assistant = DigitalAssistant(db_file)

    try:
        assistant.run()
    except KeyboardInterrupt:
        print("Terminating child processes...")
        for proc in multiprocessing.active_children():
            proc.terminate()
            proc.join()
   

if __name__ == "__main__":
    main()