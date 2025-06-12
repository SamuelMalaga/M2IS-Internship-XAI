import pandas as pd
from pathlib import Path
from Models.Project import Project

VOTER_MATRIX_PATH = f"{Path(__file__).parent.absolute()}/voter_matrix/voter_project_matrix.csv"

VOTER_MATRIX = pd.read_csv(VOTER_MATRIX_PATH,sep=";")


def compute_voter_overlap(target_project:Project, compared_project:Project) -> float:
    
    target_project_votes = VOTER_MATRIX[VOTER_MATRIX['project_id']==target_project.id]
    compared_project_votes = VOTER_MATRIX[VOTER_MATRIX['project_id']==compared_project.id]


    target_project_voters = target_project_votes['ID'].unique().tolist()
    compared_project_voters = compared_project_votes['ID'].unique().tolist()

    overlap_set = list(set(target_project_voters) & set(compared_project_voters))  

    return len(overlap_set)/len(target_project_voters)


## This function is based on merge sort
def rank_overlap(target_project:Project, projects_to_rank:list[Project]) -> None:
    if len(projects_to_rank) > 1:
        left_arr = projects_to_rank[0:len(projects_to_rank)//2]
        right_arr = projects_to_rank[len(projects_to_rank)//2:]
        
        #Recursion
        rank_overlap(target_project,left_arr)
        rank_overlap(target_project,right_arr)

        #merge
        i = 0 # LEft array index
        j = 0 # Right array index
        k = 0 # Merged array Index
        while i < len(left_arr) and j < len(right_arr):
            if compute_voter_overlap(target_project,left_arr[i]) > compute_voter_overlap(target_project,right_arr[j]):
                projects_to_rank[k] = left_arr[i]
                i += 1
            else:
                projects_to_rank[k] = right_arr[j]
                j += 1
            k += 1

        ## this is the case where the right array have every element sorted, this means that we only want to transfer 
        # elements from the right array
        while i < len(left_arr):
            projects_to_rank[k] = left_arr[i]
            i += 1
            k += 1

        while j < len(right_arr):
            projects_to_rank[k] = right_arr[j]
            j += 1
            k += 1


def hello_over():
    file_path  = Path(__file__)
    great_grandp=file_path.parent.parent.parent
    print(f"Hello from over aaa -> {great_grandp}")