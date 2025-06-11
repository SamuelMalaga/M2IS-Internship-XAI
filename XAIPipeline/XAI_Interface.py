from Agent import XAI_Agent

def launch_menu():
    while True:
        print("""
Select one option from the menu below:
1- Get overall stats of the election
2- Get explanation from project ID
        """)
        try:
            option_input = int(input())
        except:
            print("Given option is not a number")
            break

        if(option_input == 1):
            print("Imagine stats about the election")
            continue

        if(option_input == 2):
            try:
                project_id = int(input("Enter a project ID: \n"))
            except:
                print("The project ID should be a integer")
                break



if __name__ == '__main__':
    launch_menu()