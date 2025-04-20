from sentence_transformers import SentenceTransformer
from typing import Dict, List, Tuple

MODEL = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def embed(paragraphs: List[str]) -> List[List[float]]:
    """Return a list of 1D embedding vectors (plain Python floats)."""
    embs = MODEL.encode(paragraphs)
    # cast numpy floats to Python floats
    return [[float(x) for x in vec] for vec in embs]

def make_person_embeddings(data: List[Tuple[str,str]]) -> Dict[str, List[float]]:
    """Map name → embedding."""
    names, paras = zip(*data)
    vecs = embed(list(paras))
    return dict(zip(names, vecs))
