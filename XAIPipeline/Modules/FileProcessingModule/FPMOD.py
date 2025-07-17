import pathlib
import os
import sys

PROJECT_FILE = f"{pathlib.Path(__file__).parent.parent.parent.absolute()}"

VOTER_MATRIX_FILE_PATH = f"{pathlib.Path(__file__).parent.parent.parent.absolute()}/Modules/OverlappingModule/voter_matrix"

PROJECT_DETAILS_FILE_PATH =f"{pathlib.Path(__file__).parent.parent.parent.absolute()}/Modules/ProjectModule/project_details"

INI_FILE_PATH =f"{pathlib.Path(__file__).parent.parent.parent.absolute()}/XAIConf"

def check_voter_matrix():
    
    for file in os.listdir(VOTER_MATRIX_FILE_PATH):
        if file == 'voter_project_matrix.csv':
            print("voter matrix file: OK!\n")
            return True
        
    print("voter matrix file: NOT FOUND\n")
    return False

def check_project_details():

    for file in os.listdir(PROJECT_DETAILS_FILE_PATH):
        if file == 'project_details.csv':
            print("project details file: OK!\n")
            return True

    print("project details file: NOT FOUND\n")
    return False

def check_ini_file():

    for file in os.listdir(INI_FILE_PATH):
        if file == 'XAI.ini':
            print("XAI.INI file: OK!\n")
            return True
        
    print("XAI.INI file: NOT FOUND\n")
    return False
        



def check_preexisting_files():
    print("Checking for essential analysis files\n")

    voter_matrix_exists = check_voter_matrix()
    project_details_exists = check_project_details()
    ini_file_exists = check_ini_file()

    if voter_matrix_exists and project_details_exists and ini_file_exists:
        return True
    else:
        print("Some structural files are not present, please check the documentation and generate those files before running the application\n")
        return False    

    
