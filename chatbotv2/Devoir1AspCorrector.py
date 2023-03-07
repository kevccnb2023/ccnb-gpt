from typing import List
from chatbotv2.ChatBot import ChatBot
import os

VIEWS_FOLDER_NAME = "Views"
CONTROLLERS_FOLDER_NAME = "Controllers"
MODELS_FOLDER_NAME = "Models"
ENCODING = "utf-8"
ROOT_STUDENT_FOLDER_PATH = "test_data/code_etudiants_devoir_1/"

def read_file(filename):
    with open(filename, "r", encoding=ENCODING) as f:
        content = f.read()
    return content

class Devoir1AspCorrector:
    def __init__(self, controller_prompt_path: str, view_prompt_path: str, model_prompt_path: str):

        self.bot = ChatBot("gpt-3.5-turbo", "vous etes un enseignant qui corrige des devoirs. repondez seulement en format csv selon la grille de correction. ")
        self.temperature = 0
    
        #I have a correction matrix and a prompt for each file I want to grade
        self.controller_prompt = read_file(controller_prompt_path)
        self.view_prompt = read_file(view_prompt_path)
        self.model_prompt = read_file(model_prompt_path)



    def correct(self, folder) -> List[str]:
        responses = []

        #I have 3 files from students I want to correct
        controller_file = self.get_student_controller(folder)
        view_file = self.get_student_view(folder)
        model_file = self.get_student_model(folder)

        self.bot.send_message(controller_file)
        self.bot.send_message(view_file)
        self.bot.send_message(model_file)

        self.bot.send_message(self.controller_prompt)
        responses.append(self.bot.get_response(temperature=self.temperature))

        self.bot.send_message(self.view_prompt)
        responses.append(self.bot.get_response(temperature=self.temperature))

        self.bot.send_message(self.model_prompt)
        responses.append(self.bot.get_response(temperature=self.temperature))

        self.bot.send_message("combine those 3 correction matrix in a single csv with headers on top called 'question', 'points' that contains the result from the evaluation. you must only answer in csv format")
        response = self.bot.get_response(temperature=self.temperature)
        responses.append("\n".join([line for line in response.split("\n") if line.strip()]))

        self.bot.send_message(f"can you give me the final score on a maximum of 16 points from student in csv with headers 'student name', 'total score' where student_name is : {folder.name}")
        responses.append(self.bot.get_response(temperature=self.temperature))

        return responses
    
    def get_code_from_folder(self, folder_path, folder_name ):

        file_names = []
        file_contents = []
        for dirpath, dirnames, filenames in os.walk(folder_path):
            if folder_name in dirnames:
                views_folder = os.path.join(dirpath, folder_name)
                for views_dirpath, views_dirnames, views_filenames in os.walk(views_folder):
                    for filename in views_filenames:
                        file_path = os.path.join(views_dirpath, filename)
                        with open(file_path, "r", encoding=ENCODING) as f:
                            content = f.read()
                        file_names.append(file_path)
                        file_contents.append(content)
        return file_names, file_contents
    
    def get_student_controller(self, folder):
        controller_names, student_controller = self.get_code_from_folder(folder, CONTROLLERS_FOLDER_NAME)
        try:
            return student_controller[0]
        except Exception as e:
            return ""


    def get_student_model(self, folder):
        model_names, student_model = self.get_code_from_folder(folder, MODELS_FOLDER_NAME)
        try:
            return student_model[0]
        except Exception as e:
            return ""


    def get_student_view(self, folder):
        view_names, student_view = self.get_code_from_folder(folder, VIEWS_FOLDER_NAME)
        try:
            return student_view[0]
        except Exception as e:
            return ""


    def get_student_file(self, folder_path: str, file_type: str) -> str:
        file_names, files = self.get_code_from_folder(folder_path, file_type)
        if files:
            return files[0]
        else:
            return ""

    def set_temperature(self, temperature: float) -> None:
        self.temperature = temperature

