
import multiprocessing

from src.SpeechRecognizer import SpeechRecognizer
from src.TextToSpeechConverter import TextToSpeechConverter
from src.CommandProcessor import CommandProcessor
from src.DigitalAssistant import DigitalAssistant
from src.UserDB import UserDB

def main():
    db_file = "./users.db"
    db_connection = UserDB(db_file)
    speech_recognizer = SpeechRecognizer("en-US")
    text_to_speech_converter = TextToSpeechConverter("en")
    command_processor = CommandProcessor()

    assistant = DigitalAssistant(db_file, speech_recognizer, text_to_speech_converter, command_processor, db_connection)

    try:
        assistant.run()
    except KeyboardInterrupt:
        print("Terminating child processes...")
        for proc in multiprocessing.active_children():
            proc.terminate()
            proc.join()

if __name__ == "__main__":
    main()