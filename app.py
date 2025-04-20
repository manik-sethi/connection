from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from core.data_loader import read_attendees, append_attendee
from core.embeddings import make_person_embeddings
from core.analysis import reduce_to_2d, compute_graph
from core.viz_data import make_viz_json
import seaborn as sns
from fastapi.responses import FileResponse

app = FastAPI()

# serve index.html at the root
@app.get("/")
def index():
    return FileResponse("static/index.html")

# serve everything else in static/ under /static
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/graph_data")
def graph_data(n: int = 5):
    data = read_attendees()
    if not data:
        return JSONResponse({"nodes": [], "edges": []})
    # unzip
    names, paras = zip(*data)
    # embeddings
    embs = make_person_embeddings(data)
    # reduce
    coords = reduce_to_2d(list(embs.values()))
    # top matches
    _, edges = compute_graph(embs, n=n)
    # pastel palette
    colours = sns.color_palette("pastel", len(names)).as_hex()
    viz = make_viz_json(list(names), list(paras), coords, colours, edges)
    return viz

@app.post("/submit")
async def submit(request: Request):
    """
    Expect JSON: { "name": "...", "paragraph": "..." }
    """
    payload = await request.json()
    name = payload.get("name")
    para = payload.get("paragraph")
    hobby = payload.get("hobby")
    if not name or not para:
        raise HTTPException(400, "Missing name or paragraph")
    append_attendee(name, para)
    # immediate success; the next GET /graph_data will include it
    return {"status": "ok"}
