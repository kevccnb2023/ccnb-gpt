
import multiprocessing
import argparse
from src.SpeechRecognizer import SpeechRecognizer
from src.TextToSpeechConverter import TextToSpeechConverter
from src.CommandProcessor import CommandProcessor
from src.DigitalAssistant import DigitalAssistant
from src.UserDB import UserDB
from dotenv import load_dotenv
load_dotenv()

def main():
    WAKE_WORD = "porcupine"
    db_file = "./users.db"
    db_connection = UserDB(db_file)
    speech_recognizer = SpeechRecognizer("en-US")
    text_to_speech_converter = TextToSpeechConverter("en")
    command_processor = CommandProcessor()
    parser = argparse.ArgumentParser()
    parser.add_argument('--novideo', action='store_true', help='Disable facial recognition')
    args = parser.parse_args()

    assistant = DigitalAssistant(WAKE_WORD, speech_recognizer, text_to_speech_converter, command_processor, db_connection, no_video=args.novideo)

    try:
        assistant.run()
    except KeyboardInterrupt:
        print("Terminating child processes...")
        for proc in multiprocessing.active_children():
            proc.terminate()
            proc.join()

if __name__ == "__main__":
    main()