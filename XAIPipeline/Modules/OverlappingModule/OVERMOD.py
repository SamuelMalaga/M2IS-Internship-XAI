import pandas as pd

def compute_voter_overlap(target_project_id:int, compared_project_id:int) -> dict:

    election_details_dataset = pd.read_csv('./voter_matrix/voter_project_matrix.csv')

    result = {
        "overlapping_voters":[],
        "overlap_percentage_target_project":0,
        "overlap_percentage_compared_project":0
    }
    
    ##Get the voters per project
    target_project_votes = election_details_dataset[election_details_dataset['project_id']==target_project_id]
    compared_project_votes = election_details_dataset[election_details_dataset['project_id']==compared_project_id]


    ###Get a list of voters ID's that voted for that same project
    target_project_voters = target_project_votes['ID'].unique().tolist()
    compared_project_voters = compared_project_votes['ID'].unique().tolist()

    ##Calculate the overlapping percentage
    overlap_set = list(set(target_project_voters) & set(compared_project_voters))

    result["overlapping_voters"] = overlap_set
    result["overlap_percentage_target_project"]= len(overlap_set)/len(target_project_voters)
    result["overlap_percentage_compared_project"]= len(overlap_set)/len(compared_project_voters)    

    return result

def hello_over():
    print("Hello from over")