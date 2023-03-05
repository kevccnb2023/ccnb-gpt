from chatbotv2.VoiceChatBot import VoiceChatbot
from constants import WAKE_WORD, PAUSE_WAKE_WORD_SECONDS
import time

bot = VoiceChatbot()

def remove_wake_word_from_question(question):
    return question.replace(WAKE_WORD.lower(), "").strip()

def contains_wake_word(speech):
    return speech and WAKE_WORD.lower() in speech.lower()

if __name__ == "__main__":
    print("Initialisation de l'Assistant Pascal v0.1")
    last_wake_word_time = 0  # initialize timer
    while True:
        speech = bot.get_audio_input()

        if contains_wake_word(speech) and time.time() - last_wake_word_time >= PAUSE_WAKE_WORD_SECONDS:
            last_wake_word_time = time.time()  # update timer
            question = remove_wake_word_from_question(speech.lower())
            bot.send_message(question)
            response = bot.get_response()
            print(response)
        elif speech and time.time() - last_wake_word_time < PAUSE_WAKE_WORD_SECONDS:
            bot.send_message(speech)
            response = bot.get_response()
            print(response)
