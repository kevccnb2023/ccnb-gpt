import cv2
import os
import threading
import multiprocessing
import time
import pvporcupine
import struct
import pyaudio
from src.SpeechRecognizer import SpeechRecognizer
from src.TextToSpeechConverter import TextToSpeechConverter
from src.CommandProcessor import CommandProcessor
from src.UserDB import UserDB
from src.Utils import Utils

class DigitalAssistant:
    def __init__(self, WAKE_WORD, speech_recognizer: SpeechRecognizer, text_to_speech_converter: TextToSpeechConverter, cmd : CommandProcessor, db : UserDB, no_video=False):
        self.cp = cmd
        self.db = db
        self.speech_recognizer = speech_recognizer
        self.text_to_speech_converter = text_to_speech_converter
        self.known_face_encodings, self.known_face_names = db.get_users()
        self.visible_known_face_encodings = []
        self.visible_known_face_names = []

        self.WAKE_WORD = WAKE_WORD
        self.PAUSE_WAKE_WORD_SECONDS = 60
        self.no_video = no_video
        self.porcupine = self.init_porcupine(WAKE_WORD)

    def init_porcupine(self, wake_word):
        porcupine = None
        key = os.getenv("PICOVOICE_API_KEY")
        try:
            porcupine = pvporcupine.create(access_key=key,keywords=[wake_word])
        except Exception as e:
            print(f"Error initializing Porcupine: {e}")
        return porcupine

    def listen_and_process(self):
        if self.porcupine is None:
            print("Porcupine is not initialized. Cannot use wake word functionality.")
            return

        pa = pyaudio.PyAudio()
        audio_stream = pa.open(
            rate=self.porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=self.porcupine.frame_length,
            input_device_index=None)

        self.is_listening = True
        print("listening for wake word...")
        while self.is_listening:  # Add the while loop here
            
            pcm = audio_stream.read(self.porcupine.frame_length)
            pcm = struct.unpack_from("h" * self.porcupine.frame_length, pcm)
            keyword_index = self.porcupine.process(pcm)

            if keyword_index >= 0:
                print("Wake word detected")
                print("listening for question")
                question = self.speech_recognizer.listen()
                print("done listening for question")

                if question:
                    # Query GPT
                    answer = self.answer_query(question)

                    # Speak audio response from GPT
                    self.text_to_speech_converter.convert(answer)
                else:
                    print("could not understand question")

        # Clean up resources
        audio_stream.stop_stream()
        audio_stream.close()
        pa.terminate()
        self.porcupine.delete()


    def stop(self):
        self.is_listening = False

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

        if not self.no_video:

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

