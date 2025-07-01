from Modules.ProjectModule import PROJMOD
from Modules.OverlappingModule import OVERMOD
import pandas as pd

PROJECT_DATAFRAME = PROJMOD.get_project_data()

VOTE_DATAFRAME = OVERMOD.get_vote_data()


#This needs to be calculated for the whole dataset but also for the people who voted for a specific district
def calculate_exclusion_ratio() -> float:

    vote_matrix  = pd.crosstab(VOTE_DATAFRAME['ID'], VOTE_DATAFRAME['project_id'])

    loosing_projects = PROJECT_DATAFRAME[PROJECT_DATAFRAME['approved']==False]

    loosing_project_ids = loosing_projects['project_id'].to_list()

    filtered_df = vote_matrix[vote_matrix[loosing_project_ids].any(axis=1)]

    unsatisfied_voters = filtered_df.shape[0]

    total_voters = VOTE_DATAFRAME.shape[0]

    return (unsatisfied_voters/total_voters)

def hello_elecmod():
    print("hello elecmod")