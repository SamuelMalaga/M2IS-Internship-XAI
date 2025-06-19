##TODO: implement a vector DB for better runtime execution (no need to embbed the documents everytime)
##TODO: autocalibrate the similarity threshold
import pandas as pd
from sentence_transformers import SentenceTransformer
from Models.Project import Project

EMBEDDING_MODEL = SentenceTransformer("dangvantuan/sentence-camembert-large",device='cpu')

def compute_similarity_embedding(target_project: Project, similar_project: Project):
    embedded_target_project = EMBEDDING_MODEL.encode(target_project.description)
    embedded_similar_project = EMBEDDING_MODEL.encode(similar_project.description)

    return EMBEDDING_MODEL.similarity(embedded_target_project,embedded_similar_project).item()


def hello_sim():
    print("Hello from sim")