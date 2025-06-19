import configparser
import pathlib
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


##Case 1: high overlap, high similarity -> Redundant project displaced by a similar one
    ##If the cost was higher, probably it was because of that
##Case 2: High overlap, low similarity
##Case 3: low overlap, high similarity -> votebase split, probably people prefered to vote for one rather than the other since votes were limited
##Case 4: low overlap, low similarity -> Loser project
    ##Check the topK projects and classify as not appealing or near miss
    ##If not that check then it was just not appealing to the people of that district


def generate_explanation(project_id:int) -> None:

    project = PROJMOD.get_project(project_id = project_id)

    if project is None:
        print("The project won, no explanation needed")
        return
    

    winners = PROJMOD.get_same_district_winners(project)

    overlapping_projects = get_overlapping(project,winners)
    similar_projects = get_similar(project, winners)

    ##Get projects that are similar and highly overlap
    common_and_overlapping = list(set(overlapping_projects) & set(similar_projects))

    