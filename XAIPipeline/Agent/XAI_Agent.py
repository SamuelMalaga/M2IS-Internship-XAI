import configparser
from Models.Project import Project
from Modules.OverlappingModule import OVERMOD
from Modules.ProjectModule import PROJMOD
from Modules.SimilarityModule import SMOD
from pathlib import Path


CONFIG_FILE_PATH = f"{Path(__file__).parent.parent.absolute()}/XAIConf/XAI.ini"

CONFIG_OBJ = configparser.ConfigParser()

CONFIG_OBJ.read(CONFIG_FILE_PATH)

#Return the most similar winning projects to the target project
def get_similar(target_project: Project, district_winning_projects: list[Project]) -> list[Project]:

    ##TODO: add a check to see if the threshold value exists
    similarity_treshold = float(CONFIG_OBJ.get('SIMILARITY','similarity_treshold'))

    similar_projects = []

    for proj in district_winning_projects:

        if SMOD.compute_similarity_embedding(target_project, proj) >= similarity_treshold:
            similar_projects.append(proj)
    
    return similar_projects

#Return the most overlapping winning projects to the target project
def get_overlapping(target_project: Project, district_winning_projects: list[Project]) -> list[Project]:
    
    OVERMOD.rank_overlap(target_project,district_winning_projects)

    competitor_projects = []

    ##TODO: add a check to see the threshold value
    overlap_threshold = float(CONFIG_OBJ.get('OVERLAPPING','overlap_threshold'))
    
    for proj in district_winning_projects:
        if OVERMOD.compute_voter_overlap(target_project, proj) >= overlap_threshold:
            competitor_projects.append(proj)

    return competitor_projects

## Check if the project had enough votes to be approved but wasn't because of algorithm despriorization
def check_budget_issue(target_project: Project) -> bool:
    district_vote_threshold = PROJMOD.get_district_vote_threshold(target_project)

    if target_project.vote_count >= district_vote_threshold:
        return True
    else:
        return False

def check_top_k_loosing_projects(target_project:Project) -> bool:

    district_loosing_projects = PROJMOD.get_same_district_loosers(target_project)

    ## -1 is for the index correction on the loop, if it didn't exist, then consider top k =2 actually takes the first three projects (index base 0)
    top_k_threshold = int(CONFIG_OBJ.get('LOOSER_TOLERANCE','top_k')) -1


    for i in range(len(district_loosing_projects)):
        if district_loosing_projects[i] == target_project and i <= top_k_threshold:
            return True

    return False


##Case 1: high overlap, high similarity -> Untied by the overlap directionality
    ## If the project A(looser) supporters supported highly project B(winner) but supporters of B not that much project A
    ## (Auxiliary project)Directionality A -> B: probably project B was more central/more important than project A for the voter
    ## (Niched project) Directionality A <- B: Project B was more appealing to the general public than A, A is very niched
    #     Niched project:
    #     Project A: "Dog Park Upgrade in Neighborhood X"
    #     Project B: "Citywide Green Spaces Initiative"
    #     Voters who care about A may also vote for B (if they support green spaces in general), but not all B voters care specifically about dogs or Neighborhood X.
##Case 2: High overlap, low similarity -> Hurted because of vote dilution
    ## If A had significant fewer votes, then it simply was not as popular as B
    ## If A -> B: then A is a support project
    ## If B <- A: A auxiliary project won ??
    ## From the shared votebase, unique voters of A and unique voters of B
    ## Can help us tell where they are supported as a bundle or they had a dedicated weak base
##Case 3: low overlap, high similarity -> votebase split, probably people prefered to vote for one rather than the other since votes were limited
##Case 4: low overlap, low similarity -> Loser project
    ##Check the topK projects and classify as not appealing or near miss
    ##If not that check then it was just not appealing to the people of that district

##TODO: Find a way to calibrate the values
def generate_explanation(project_id:int) -> None | dict[str:bool]:

    result = {
        "DESPRIORITIZED BY THE ALGORITHM": False,
        "LOOSER PROJECT":False,
        "CLONE PROJECT":False,
        "COMPETITOR PROJECT":False
    }

    project = PROJMOD.get_project(project_id = project_id)

    if project is None:
        print("The project won, no explanation needed")
        return
    

    winners = PROJMOD.get_same_district_winners(project)

    overlapping_projects = get_overlapping(project,winners)
    similar_projects = get_similar(project, winners)


    ##EX proj ID 111
    ##TODO: Find a better way to display it
    if check_budget_issue(project):
        result["DESPRIORITIZED BY THE ALGORITHM"] = True
        print("DESPRIORITIZED BY THE ALGORITHM | The project was not selected because it had a cost that did not fit the budget at the selection time")

    ##EX proj ID 112
    ##TODO: Show a better way to display it (maybe show the position in which the project was)
    if not check_top_k_loosing_projects(project):
        result["LOOSER PROJECT"] = True
        print(f"LOOSER PROJECT | The project was not selected because it was just not appealing to the public, it was behind the top {int(CONFIG_OBJ.get('LOOSER_TOLERANCE','top_k'))} runner up projects")
    
    ##Example of clone projects 101(gangnant) and 103, 52(gangnant) and 51, 52(gangnant) and 53, 40 and 38(gangnant), 5(gangnant) and 8, 12(gangnant) and 8
    ##26 and 28(gangnant), 26 and 25(gangnant) -> used projects to calibrate the similairity threshold
    if len(similar_projects) > 0:
        similar_project_ids = []
        for project in similar_projects:
            similar_project_ids.append(project.id)
        result["CLONE PROJECT"] = similar_project_ids      
        print("CLONE PROJECT | The project was not selected dua to votebase split, there was another project very similar to this one that had more votes")

    ##Example of overlapping projects 129
    if len(overlapping_projects) > 0:
        overlapping_projects_ids=[]
        for project in overlapping_projects:
            overlapping_projects_ids.append(project.id)
        result["COMPETITOR PROJECT"] = overlapping_projects_ids
        print("COMPETITOR PROJECT | The project was not selected because it didn't secure enough unique support. The high Overlap shows shared interest, but the winning project attracted more committed or additional voters, leading to its success.")

    return result

def simil_bypass(project_id1, project_id2):
    project1 = PROJMOD.get_project(project_id = project_id1)
    project2 = PROJMOD.get_project(project_id = project_id2)

    print(SMOD.compute_similarity_embedding(project1, project2))

def over_bypass(project_id1, project_id2):
    project1 = PROJMOD.get_project(project_id = project_id1)
    project2 = PROJMOD.get_project(project_id = project_id2)

    print(OVERMOD.compute_voter_overlap(project1, project2))