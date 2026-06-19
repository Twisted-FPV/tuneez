from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import tempfile, json
from tuneez.core.blackbox import load_blackbox
from tuneez.core.cli_parser import parse_cli_dump
from tuneez.core.models import BuildProfile
from tuneez.core.recommend import analyze

app = FastAPI(title="TuneEZ", version="3.0.0")
STATIC = Path(__file__).resolve().parents[3] / "frontend" / "public"
if STATIC.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC)), name="static")

@app.get("/", response_class=HTMLResponse)
def home():
    idx = STATIC / "index.html"
    return idx.read_text(encoding="utf-8") if idx.exists() else "<h1>TuneEZ API</h1>"

@app.get("/health")
def health():
    return {"ok": True, "name": "TuneEZ", "version": "3.0.0"}

@app.post("/api/analyze")
async def analyze_upload(
    blackbox: UploadFile = File(...),
    cli_dump: UploadFile = File(...),
    build_json: str = Form("{}")
):
    build = BuildProfile(**json.loads(build_json or "{}"))
    with tempfile.TemporaryDirectory() as td:
        bpath = Path(td) / (blackbox.filename or "blackbox.csv")
        cpath = Path(td) / (cli_dump.filename or "cli.txt")
        bpath.write_bytes(await blackbox.read())
        cpath.write_bytes(await cli_dump.read())
        df = load_blackbox(str(bpath))
        cfg = parse_cli_dump(cpath.read_text(encoding="utf-8", errors="ignore"))
        return JSONResponse(analyze(df, cfg, build).model_dump())

@app.post("/api/fc-mode")
def fc_mode():
    return {
        "web": "Upload files everywhere. Web Serial can pull CLI on supported HTTPS desktop browsers.",
        "android": "Use the Capacitor app. Reliable FC extraction should be added with a native USB serial plugin.",
        "status": "scaffolded"
    }
