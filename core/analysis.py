import umap
from sklearn.preprocessing import StandardScaler
from scipy.spatial.distance import cosine
from typing import Dict, List, Tuple
from collections import defaultdict

def reduce_to_2d(
    embeddings: List[List[float]]
) -> List[Tuple[float,float]]:
    """Standardize + UMAP → list of (x,y)."""
    scaler = StandardScaler()
    scaled = scaler.fit_transform(embeddings)
    reducer = umap.UMAP()
    two_d = reducer.fit_transform(scaled)
    # cast to Python floats
    return [(float(x), float(y)) for x,y in two_d]

def compute_graph(
    person_embs: Dict[str, List[float]],
    n: int = 5
) -> Tuple[Dict[str,List[Tuple[float,str]]], List[Tuple[str,str,float]]]:
    """
    Returns:
      top_matches: name → list of (distance, other_name)
      edges:       list of (source, target, weight)
    """
    all_pairs = defaultdict(list)
    for src, emb1 in person_embs.items():
        for tgt, emb2 in person_embs.items():
            d = float(cosine(emb1, emb2))
            all_pairs[src].append((d, tgt))

    top_matches = {}
    edges = []
    for src, pairs in all_pairs.items():
        neighbors = sorted(pairs, key=lambda x: x[0])[1:n+1]
        top_matches[src] = neighbors
        for weight, tgt in neighbors:
            edges.append((src, tgt, weight))

    return top_matches, edges
