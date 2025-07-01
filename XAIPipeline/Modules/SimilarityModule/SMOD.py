##TODO: implement a vector DB for better runtime execution (no need to embbed the documents everytime)
##TODO: autocalibrate the similarity threshold
import pandas as pd
from sentence_transformers import SentenceTransformer
from Models.Project import Project

EMBEDDING_MODEL = SentenceTransformer("dangvantuan/sentence-camembert-large",device='cpu')


##TODO: automatic handling of bigger inputs --> Testing case (150, 151) || Truncation works but there is a loss of information
##It would be nice to have a more intelligent way to do that -> Summarization models (another one plugged here)
def compute_similarity_embedding(target_project: Project, similar_project: Project):

    # embedded_target_project = EMBEDDING_MODEL.encode(target_project.description)
    # embedded_similar_project = EMBEDDING_MODEL.encode(similar_project.description)

    embedded_target_project = safe_encode(target_project.description)
    embedded_similar_project = safe_encode(similar_project.description)

    return EMBEDDING_MODEL.similarity(embedded_target_project,embedded_similar_project).item()

def safe_encode(text, max_tokens = 512):
    tokens = EMBEDDING_MODEL.tokenizer.encode(text, truncation=True, max_length=max_tokens)
    return EMBEDDING_MODEL.encode(EMBEDDING_MODEL.tokenizer.decode(tokens, skip_special_tokens=True))

def hello_sim():
    print("Hello from sim")