from Models.Project import Project
from Models.ProjectNotFoundException import ProjectNotFoundException
import pandas as pd
import pathlib

PROJECT_DETAILS_PATH = f"{pathlib.Path(__file__).parent.absolute()}/project_details/project_details.csv"

PROJECTS = pd.read_csv(PROJECT_DETAILS_PATH)


def get_project(project_id: int) -> Project:

    """
        This returns a project object based on a specific project ID

        Parameters
        ----------
        target_project : int
            the project_id that you want to convert to Project object

        Returns
        -------
        Project

    """

    try:
        found_project = PROJECTS.loc[PROJECTS['project_id']==project_id].iloc[0]
        proj_obj = Project(
            id=found_project['project_id'],
            title = found_project['project_name'], 
            description = found_project['description'], 
            cost = found_project['cost'], 
            category = found_project['category'],
            district=found_project['agg_quartiers'],
            district_code=found_project['src_district_code'],
            vote_count=found_project['votes']
        )
        approved_project = bool(found_project['approved'])

        return proj_obj
    except IndexError:
        raise ProjectNotFoundException("The passed project ID is either out of bounds or the project ID does not exists")

def get_same_district_winners(project:Project) -> list[Project]:

    """
        This function retrieves the winners of the same district as the target project

        Parameters
        ----------
        project : Project
            project of which you want tot get the same district winners

        Returns
        -------
        list[Projects]

    """

    district_winners_df = PROJECTS.loc[(PROJECTS['src_district_code']==project.district_code) & (PROJECTS['approved']==True)]

    district_winners_df = district_winners_df.sort_values(by='votes', ascending=True)

    district_winners_projects = []

    for index, row in district_winners_df.iterrows():
        project = Project(
            id=row['project_id'],
            title = row['project_name'], 
            description = row['description'], 
            cost = row['cost'], 
            category = row['category'],
            district=row['agg_quartiers'],
            district_code=row['src_district_code'],
            vote_count=row['votes']
        )

        district_winners_projects.append(project)

    return district_winners_projects

def get_same_district_loosers(project:Project) -> list[Project]:

    """
        This function retrieves the loosers of the same district as the target project

        Parameters
        ----------
        project : Project
            project of which you want tot get the same district loosers

        Returns
        -------
        list[Projects]

    """

    district_loosers_df = PROJECTS.loc[(PROJECTS['src_district_code']==project.district_code) & (PROJECTS['approved']==False)]

    district_loosers_df = district_loosers_df.sort_values(by='votes', ascending=False)

    district_loosers_projects = []

    for index, row in district_loosers_df.iterrows():
        project = Project(
            id=row['project_id'],
            title = row['project_name'], 
            description = row['description'], 
            cost = row['cost'], 
            category = row['category'],
            district=row['agg_quartiers'],
            district_code=row['src_district_code'],
            vote_count=row['votes']
        )

        district_loosers_projects.append(project)

    return district_loosers_projects

def get_district_vote_threshold(project:Project) -> int:

    """
        This function retrieves the vote threshold for a project to be approved in a specific district

        Parameters
        ----------
        project : Project
            project of which you want to get the same district vote threshold

        Returns
        -------
        int

    """

    district_winners_df = PROJECTS.loc[(PROJECTS['src_district_code']==project.district_code) & (PROJECTS['approved']==True)]

    return district_winners_df.min(axis=0)['votes']

def get_all_projects()->list[Project]:

    """
        This function converts all projects in the dataset to project objects

        Parameters
        ----------
        

        Returns
        -------
        list[Projects]

    """

    all_projects = []

    for index, row in PROJECTS.iterrows():
        found_project = get_project(row['project_id'])
        all_projects.append(found_project)

    return all_projects

def get_project_data() -> pd.DataFrame:

    """
        This function returns a dataframe of the project data

        Parameters
        ----------
       

        Returns
        -------
        pd.DataFrame

    """

    project_data = PROJECTS.copy()
    
    return PROJECTS

