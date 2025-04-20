import matplotlib
matplotlib.use('Agg')

from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from core.data_loader import read_attendees, append_attendee
from core.embeddings import make_person_embeddings
from core.analysis import reduce_to_2d, compute_graph
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO

app = FastAPI()

# Serve the main page
@app.get("/")
def index():
    return FileResponse("static/index.html")

# Serve static files under /static
app.mount("/static", StaticFiles(directory="static"), name="static")

# Handle new submissions
@app.post("/submit")
async def submit(request: Request):
    payload = await request.json()
    name = payload.get("name")
    para = payload.get("paragraph")
    hobby = payload.get("hobby")
    if not (name and para and hobby):
        raise HTTPException(400, "Missing name, paragraph, or hobby")
    append_attendee(name, para, hobby)
    return {"status": "ok"}

# Serve a static UMAP scatter as a PNG image
@app.get("/scatter.png")
def scatter_png():
    rows = read_attendees()
    if not rows:
        raise HTTPException(404, "No data yet")
    # Unpack name, paragraph, hobby but we'll only use name
    names, paras, hobbies = zip(*rows)
    embs = make_person_embeddings(rows)
    coords = reduce_to_2d(list(embs.values()))
    xs, ys = zip(*coords)

    # Create a larger figure so labels fit
    fig, ax = plt.subplots(figsize=(12, 12))
    # Plot points
    ax.scatter(xs, ys, s=200, alpha=0.8)
    # Annotate with names only
    for x, y, name in zip(xs, ys, names):
        ax.text(
            x, y, name,
            fontsize=8,
            ha="center", va="center"
        )
    ax.axis("off")

    buf = BytesIO()
    fig.savefig(buf, format="png", dpi=300, bbox_inches="tight")
    buf.seek(0)
    plt.close(fig)
    return StreamingResponse(buf, media_type="image/png")
