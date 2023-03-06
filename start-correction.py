from chatbotv2.Devoir1AspCorrector import Devoir1AspCorrector
import os
from pathlib import Path
import pandas as pd
import io
import glob
import random

ROOT_STUDENT_FOLDER_PATH = "test_data/code_etudiants_devoir_1/"
PROMPT_FOLDER_PATH = "./prompts"

def check_folder(folder):
    if os.path.isdir(folder) and len([f for f in os.scandir(folder) if not f.name.startswith('.')]) == 0:
        # print(f"No files found in folder {folder.name}")
        print(f"{folder.name},0")
        return False
    # if glob.glob(os.path.join(folder, "*.xlsx")):
    #     print(f".xlsx files found in folder {folder.name}")
    #     return False
    return True

def create_excel(csv_final, folder):
    # print(f"creating excel file for folder {folder.name}")
    try:
        df = pd.read_csv(io.StringIO(csv_final))
        filename = f"{folder.name}_{random.randint(1000, 9999)}.xlsx"
        df.to_excel(ROOT_STUDENT_FOLDER_PATH + filename, index=False)
    except Exception as e:
        return
        # print(csv_final)
        # print(e)

def get_student_folder_names():
    path = Path(ROOT_STUDENT_FOLDER_PATH)
    return sorted([folder for folder in path.iterdir() if folder.is_dir()])

def get_second_line(text):
    lines = text.split('\n')
    if len(lines) > 1:
        return lines[1]
    else:
        return ''
#If your first attempts fail, don't be afraid to experiment with different ways of priming or conditioning the model.
def main():
    
    student_folders = get_student_folder_names()

    for folder in student_folders:
        asp_corrector = Devoir1AspCorrector(
                f"{PROMPT_FOLDER_PATH}/asp-devoir-1[controller].prompt",
                f"{PROMPT_FOLDER_PATH}/asp-devoir-1[view].prompt",
                f"{PROMPT_FOLDER_PATH}/asp-devoir-1[model].prompt"
            )
        asp_corrector.set_temperature(0)
        # print(f"correcting folder name : {folder.name}")

        if not check_folder(folder):
            continue

        grille_de_correction = asp_corrector.correct(folder)
        
        create_excel(grille_de_correction[3], folder)

        print(get_second_line(grille_de_correction[4]))
    
if __name__ == "__main__":
    main()