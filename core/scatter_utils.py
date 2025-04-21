import matplotlib
matplotlib.use('Agg')  # use non-interactive backend

from io import BytesIO
from fastapi.responses import StreamingResponse
from core.db                 import read_attendees
from core.embeddings import make_person_embeddings
from core.analysis import reduce_to_2d
import matplotlib.pyplot as plt

ic = lambda *args: None  # placeholder if needed for logging

def generate_scatter_png() -> StreamingResponse:
    """
    Read attendee data, compute embeddings + UMAP 2D projection,
    render a Matplotlib scatter with names, and return as PNG.
    """
    # 1) Load and unpack data
    rows = read_attendees()
    if not rows:
        print("No data yet: returning a 1x1 transparent PNG")
        # no data yet: return a 1x1 transparent PNG
        buf = BytesIO()
        plt.figure(figsize=(1,1))
        plt.savefig(buf, format='png', transparent=True)
        buf.seek(0)
        return StreamingResponse(buf, media_type='image/png')

    names = [row["name"] for row in rows]
    paras = [row["Q1"] for row in rows]
    hobbies = [row["Q2"] for row in rows]

    # 2) Compute embeddings + 2D coords
    embs = make_person_embeddings(list(zip(names, paras, hobbies)))
    coords = reduce_to_2d(list(embs.values()))
    xs, ys = zip(*coords)

    # 3) Plot
    fig, ax = plt.subplots(figsize=(12,12))
    ax.scatter(xs, ys, s=200, alpha=0.8)
    for x, y, name in zip(xs, ys, names):
        ax.text(
            x, y, name,
            fontsize=10,
            ha='center', va='center'
        )
    ax.axis('off')
    plt.tight_layout()

    # 4) Serialize to PNG
    buf = BytesIO()
    fig.savefig(buf, format='png', dpi=300, bbox_inches='tight')
    buf.seek(0)
    plt.close(fig)

    return StreamingResponse(buf, media_type='image/png')
