from Modules.OverlappingModule import OVERMOD
from Modules.ProjectModule import PROJMOD
from Modules.SimilarityModule import SMOD

def hello_agent():
    print("hello from agent")

def hello_over():
    OVERMOD.hello_over()

def hello_proj():
    PROJMOD.hello_proj()

def hello_sim():
    SMOD.hello_sim()