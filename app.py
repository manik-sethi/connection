import matplotlib
matplotlib.use('Agg')

from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from core.db          import read_attendees, append_attendee
from core.embeddings import make_person_embeddings
from core.analysis import reduce_to_2d, compute_graph
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO

from core.scatter_utils import generate_scatter_png


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
    Q1   = payload.get("Q1")
    Q2 = payload.get("Q2")
    if not (name and Q1 and Q2):
        raise HTTPException(400, "Missing name, Q1, or Q2")
    append_attendee(name, Q1, Q2)
    return {"status": "ok"}

@app.get("/scatter.png")
def scatter_png():
    return generate_scatter_png()