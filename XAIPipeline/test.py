from Modules.ProjectModule import PROJMOD
from Agent import XAI_Agent
import json

if __name__ == '__main__':

    explanation_cases = {}

    loosing_projects_df = PROJMOD.get_project_data()

    loosing_projects_df = loosing_projects_df[loosing_projects_df['approved']==False]

    loosing_projects_list = loosing_projects_df['project_id'].to_list()

    for project_id in loosing_projects_list:
        result = XAI_Agent.generate_explanation(project_id)
        explanation_cases[project_id] = result

    with open("explanations.json", "w") as file:
        json.dump(explanation_cases, file)