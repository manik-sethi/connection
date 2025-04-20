from typing import Dict, List, Tuple

def make_viz_json(
    names:      List[str],
    paragraphs: List[str],
    coords:     List[Tuple[float,float]],
    colours:    List[str],
    edges:      List[Tuple[str,str,float]],   # keep this
) -> Dict:
    """
    Builds a vis-network JSON structure containing only node information.

    This function takes lists of names, corresponding paragraphs (for tooltips),
    2D coordinates for positioning, colors for the nodes, and an (unused) list
    for edges, and formats them into a JSON structure suitable for libraries
    like vis.js. The nodes are configured to have static positions and no
    physics simulation.

    Args:
        names: A list of strings, where each string is the name (ID and label) of a node.
        paragraphs: A list of strings, where each string is the tooltip text for the corresponding node.
        coords: A list of tuples, where each tuple (x, y) represents the 2D coordinates of a node.
        colours: A list of strings, where each string is the color of the corresponding node.
        edges: A list of tuples, intended for edge information but currently unused and expected to be empty.

    Returns:
        A dictionary representing the vis-network JSON with 'nodes' and an empty 'edges' list.
    """
    coord_scale = 200
    nodes = []
    for i, name in enumerate(names):
        x, y = coords[i]
        nodes.append({
            "id":      name,
            "label":   name,
            "x":       x * coord_scale,
            "y":       y * coord_scale,
            "fixed":   {"x": True, "y": True},
            "physics": False,
            "title":   paragraphs[i],
            "color":   colours[i],
        })

    # still return an (empty) edges list as per the requirement
    return {"nodes": nodes, "edges": []}