from configparser import ConfigParser
import pathlib
from Modules.OverlappingModule import OVERMOD
from Modules.ProjectModule import PROJMOD
from Modules.SimilarityModule import SMOD

##Case 1 
def check_most_similar():
    pass


##Case 3
def check_competitor():
    pass


##Case 2
def check_loser():
    pass



def hello_agent():
    print("hello from agent")

def hello_over():
    OVERMOD.hello_over()

def hello_proj():
    PROJMOD.hello_proj()

def hello_sim():
    SMOD.hello_sim()

def generate_explanation(project_id:int) -> None:
    project = PROJMOD.get_project(project_id = project_id)
    winners = PROJMOD.get_same_district_winners(project)
    

    print(project)