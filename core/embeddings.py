from sentence_transformers import SentenceTransformer
from typing import Dict, List, Tuple

MODEL = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def embed(texts: List[str]) -> List[List[float]]:
    """Encode a list of strings into Python‑float vectors."""
    embs = MODEL.encode(texts)
    return [[float(x) for x in vec] for vec in embs]

def make_person_embeddings(
    data: List[Tuple[str, str, str]]
) -> Dict[str, List[float]]:
    """
    data: a list of (name, paragraph, hobby)
    Returns a dict: name -> embedding of "paragraph + hobby"
    """
    names, paras, hobbies = zip(*data)

    # Combine each paragraph and hobby into one text
    texts = [
        f"{para.strip()} Hobby: {hobby.strip()}."
        for para, hobby in zip(paras, hobbies)
    ]

    vecs = embed(texts)
    return dict(zip(names, vecs))
