from Agent import XAI_Agent
from Modules.ElectionModule import ELECMOD
from Modules.FileProcessingModule import FPMOD
import sys

def launch_menu():

    if not FPMOD.check_preexisting_files():
        sys.exit()


    while True:

        print("""
Select one option from the menu below:
1- Get overall stats of the election
2- Get explanation from project ID
        """)
        try:
            option_input = int(input("Enter your option\n"))
            print("\n")
        except:
            print("Given option is not a number")
            break

        if(option_input == 1):
            print(ELECMOD.calculate_exclusion_ratio())
            continue

        if(option_input == 2):
            # project_id = int(input("Enter a project ID: \n"))
            # XAI_Agent.generate_explanation(project_id)
            try:
                project_id = int(input("Enter a project ID: \n"))
                XAI_Agent.generate_explanation(project_id)
            except:
                print("The project ID should be a integer")
                break



if __name__ == '__main__':
    launch_menu()