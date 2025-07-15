import pathlib
import os


PROJECT_FILE = f"{pathlib.Path(__file__).parent.parent.parent.absolute()}"

VOTER_MATRIX_FILE_PATH = f"{pathlib.Path(__file__).parent.parent.parent.absolute()}/Modules/OverlappingModule/voter_matrix"

PROJECT_DETAILS_FILE_PATH =f"{pathlib.Path(__file__).parent.parent.parent.absolute()}/Modules/ProjectModule/project_details"

def check_voter_matrix():
    
    for file in os.listdir(VOTER_MATRIX_FILE_PATH):
        if file == 'voter_project_matrix.csv':
            return True
    
    return False

def check_project_details():

    for file in os.listdir(PROJECT_DETAILS_FILE_PATH):
        if file == 'project_details.csv':
            return True

    return False



def check_preexisting_files():
    print("Checking for essential analysis files")
    voter_matrix_exists = check_voter_matrix()
    project_details_exists = check_project_details()


    if voter_matrix_exists:
        print("voter matrix file OK!")
    else:
        print("voter matrix file not found")

    if project_details_exists:
        print("project details file OK!")
    else:
        print("project details file not found")
