import cv2
import threading
import multiprocessing
import time
from src.SpeechRecognizer import SpeechRecognizer
from src.TextToSpeechConverter import TextToSpeechConverter
from src.CommandProcessor import CommandProcessor
from src.UserDB import UserDB
from src.Utils import Utils

class DigitalAssistant:
    def __init__(self, WAKE_WORD, speech_recognizer: SpeechRecognizer, text_to_speech_converter: TextToSpeechConverter, cmd : CommandProcessor, db : UserDB):
        self.cp = cmd
        self.db = db
        self.speech_recognizer = speech_recognizer
        self.text_to_speech_converter = text_to_speech_converter
        self.known_face_encodings, self.known_face_names = db.get_users()
        self.WAKE_WORD = WAKE_WORD.lower()
        self.PAUSE_WAKE_WORD_SECONDS = 60

    def listen_and_process(self):

        last_wake_word_time = 0  # initialize timer

        while True:
            print("listening...")
            text = self.speech_recognizer.listen()
            
            if text and self.WAKE_WORD in text.lower() and (time.time() - last_wake_word_time >= self.PAUSE_WAKE_WORD_SECONDS):

                print("listening for question")
                question = self.speech_recognizer.listen()
                print("done listening for question")

                if question:

                    #query chatgpt
                    answer = self.answer_query(question)

                    #speak audio response from chatgpt
                    self.text_to_speech_converter.convert(answer)
                    last_wake_word_time = time.time()  # update timer
                else:
                    print("could not understand question")

            elif text and (time.time() - last_wake_word_time < self.PAUSE_WAKE_WORD_SECONDS):
                print("didnt need wake word!")
                #query chatgpt
                answer = self.answer_query(text)

                #speak audio response from chatgpt
                self.text_to_speech_converter.convert(answer)
                last_wake_word_time = time.time()  # update timer



    # Answer the query using GPT
    def answer_query(self, query):
        self.cp.send_message(query)
        answer = self.cp.get_response().strip()
        return answer
    
    #main thread
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