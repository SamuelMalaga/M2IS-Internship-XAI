from Models.Project import Project
from Models.ProjectNotFoundException import ProjectNotFoundException
import pandas as pd
import pathlib

PROJECT_DETAILS_PATH = f"{pathlib.Path(__file__).parent.absolute()}/project_details/project_details.csv"

PROJECTS = pd.read_csv(PROJECT_DETAILS_PATH)

def hello_proj():
    print("Hello from proj")

def get_project(project_id: int) -> Project | None:

    try:
        found_project = PROJECTS.loc[PROJECTS['project_id']==project_id].iloc[0]
        proj_obj = Project(
            id=found_project['project_id'],
            title = found_project['project_name'], 
            description = found_project['description'], 
            cost = found_project['cost'], 
            category = found_project['category'],
            district=found_project['agg_quartiers'],
            district_code=found_project['src_district_code']
        )
        return proj_obj
    except IndexError:
        raise ProjectNotFoundException("The passed project ID is either out of bounds or the project ID does not exists")

def get_same_district_winners(project:Project) -> list[Project]:

    district_winners_df = PROJECTS.loc[(PROJECTS['src_district_code']==project.district_code) & (PROJECTS['approved']==True)]

    district_winners_projects = []

    for index, row in district_winners_df.iterrows():
        project = Project(
            id=row['project_id'],
            title = row['project_name'], 
            description = row['description'], 
            cost = row['cost'], 
            category = row['category'],
            district=row['agg_quartiers'],
            district_code=row['src_district_code']
        )

        district_winners_projects.append(project)

    return district_winners_projects