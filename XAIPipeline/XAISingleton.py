import torch
import pandas as pd


from ollama import chat
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from sentence_transformers import SentenceTransformer

def compute_voter_overlap(target_project_id:int, compared_project_id:int, election_details_dataset) -> float:
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
    result["overlap_percentage_target_project"]= round(len(overlap_set)/len(target_project_voters),4)
    result["overlap_percentage_compared_project"]= round(len(overlap_set)/len(compared_project_voters),4) 

    return result



if __name__ == '__main__':

    # Projects aggregated dataframe
    projects_dataframe = pd.read_csv("../projectsAggWResults.csv")

    projects_dataframe[['description','avis_technique']] = projects_dataframe['description'].str.split('Modalités de réalisation - Avis technique :', expand=True)

    # projects_dataframe['avis_technique'] = projects_dataframe['description'].str.extract(r"- Avis technique\s*:\s*(.*)")

    # projects_dataframe.to_csv("TEST.csv")

    # Voters dataframe
    voters_dataframe = pd.read_csv("../projectDetails.csv", sep=";")

    #Initialize the model to compare embeddings sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 Alibaba-NLP/gte-Qwen2-1.5B-instruct
    model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2', device='cpu')

    ## Limit to the range of projects in the dataframe
    try: 
        given_project_id = int(input("Enter a project ID \n"))
    except:
        print("given project ID should be a valid INT")
    
    target_project = projects_dataframe[projects_dataframe['project_id']==given_project_id].iloc[0]

    encoded_target_project_descritpion = model.encode(target_project['description'])
    
    district_projects = projects_dataframe[projects_dataframe['district']==target_project['district']].sort_values(by=['votes'])

    district_winner_projects = district_projects[district_projects['approved_binary']==1]
    
    print(
        f"""
        PROJECT INFO ----------
            Project Name: {target_project['project_id']}
            Project Name: {target_project['project_name']}
            Project Category: {target_project['category']}
            Project District (src): {target_project['district']}
        """
    )

    print(
        f"""
        DISTRICT INFO ----------
            Total number of projects: {len(district_projects)}
            Number of approved projects: {len(district_projects[district_projects['approved_binary']==1])}
            Number of rejected projects: {len(district_projects[district_projects['approved_binary']==0])}
            Approval threshold for the district: {district_winner_projects['votes'].min()}
            Most expensive approved project: {district_winner_projects['cost'].max()}
            Cheapest approved project: {district_winner_projects['cost'].min()}
            Approved budget for the district: {district_winner_projects['cost'].sum()}
        """
    )

    output_list =[]

    for index, row in district_winner_projects.iterrows():
        overlapping_score = compute_voter_overlap(target_project['project_id'], row['project_id'],voters_dataframe)
        encoded_project_description = model.encode(row['description'])
        similarity_score = model.similarity(encoded_target_project_descritpion, encoded_project_description)
        result = {
            "ID":row['project_id'],
            "similarity":similarity_score,
            "Overlapping":overlapping_score['overlap_percentage_target_project']
        }
        output_list.append(result)
        # print(f"""
        #         Project ID -> {row['project_id']} | Title -> {row['project_name']} | vote count -> {row['votes']}:
        #             overlapping score ->{overlapping_score['overlap_percentage_target_project']}
        #             similarity score -> {similarity_score}
        # """)

    output_list.sort(key=lambda x: x['similarity'].item(), reverse=True)

    print(output_list)

