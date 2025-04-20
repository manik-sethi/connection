from typing import Dict, List, Tuple

def make_viz_json(
    names: List[str],
    paragraphs: List[str],
    coords: List[Tuple[float,float]],
    colours: List[str],
    edges: List[Tuple[str,str,float]]
) -> Dict:
    """
    Build the JSON structure that vis‑network expects:
    {
      nodes: [{id, label, x, y, title, color},…],
      edges: [{from, to, value},…]
    }
    """
    nodes = []
    for i, name in enumerate(names):
        x,y = coords[i]
        nodes.append({
            "id": name,
            "label": name,
            "x": x,
            "y": y,
            "title": paragraphs[i],
            "color": colours[i]
        })

    edges_json = [
        {"from": src, "to": tgt, "value": weight}
        for src, tgt, weight in edges
    ]

    return {"nodes": nodes, "edges": edges_json}
