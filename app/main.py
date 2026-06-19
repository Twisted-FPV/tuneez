from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse

app = FastAPI(title="TuneEZ")

@app.get("/", response_class=HTMLResponse)
def home():
    return """
<!DOCTYPE html>
<html>
<head>
  <title>TuneEZ</title>
  <style>
    body { background:#07111f; color:white; font-family:Arial; margin:0; padding:40px; }
    .card { background:#101b2f; padding:24px; border-radius:16px; margin-bottom:20px; }
    input, textarea, select { width:100%; padding:12px; margin:8px 0; border-radius:8px; }
    button { background:#7c3aed; color:white; padding:14px 22px; border:0; border-radius:10px; cursor:pointer; }
  </style>
</head>
<body>
  <h1>TuneEZ</h1>
  <p>Free open FPV tuning for everyone.</p>

  <div class="card">
    <h2>New Tune Analysis</h2>
    <form action="/analyze" method="post" enctype="multipart/form-data">
      <label>Blackbox log (.bbl, .bfl, .csv)</label>
      <input type="file" name="blackbox">

      <label>CLI dump / diff all</label>
      <input type="file" name="cli_dump">

      <label>Craft type</label>
      <select name="craft_type">
        <option>5 inch freestyle</option>
        <option>Racing quad</option>
        <option>Cinewhoop</option>
        <option>Long range</option>
        <option>Tinywhoop</option>
        <option>Fixed wing</option>
      </select>

      <label>Build info / symptoms</label>
      <textarea name="notes" rows="6" placeholder="Frame, motors, KV, props, ESC firmware, gyro, battery, symptoms..."></textarea>

      <button type="submit">Analyze Tune</button>
    </form>
  </div>
</body>
</html>
"""

@app.post("/analyze", response_class=HTMLResponse)
async def analyze(
    blackbox: UploadFile = File(None),
    cli_dump: UploadFile = File(None),
    craft_type: str = Form("Unknown"),
    notes: str = Form("")
):
    blackbox_name = blackbox.filename if blackbox else "No Blackbox uploaded"
    cli_name = cli_dump.filename if cli_dump else "No CLI dump uploaded"

    return f"""
<!DOCTYPE html>
<html>
<head>
  <title>TuneEZ Report</title>
  <style>
    body {{ background:#07111f; color:white; font-family:Arial; margin:0; padding:40px; }}
    .card {{ background:#101b2f; padding:24px; border-radius:16px; margin-bottom:20px; }}
    pre {{ background:#020617; padding:18px; border-radius:12px; color:#9ef7c1; }}
    a {{ color:#9ef7c1; }}
  </style>
</head>
<body>
  <h1>TuneEZ Analysis Report</h1>

  <div class="card">
    <h2>Uploaded Files</h2>
    <p><b>Blackbox:</b> {blackbox_name}</p>
    <p><b>CLI Dump:</b> {cli_name}</p>
    <p><b>Craft Type:</b> {craft_type}</p>
    <p><b>Notes:</b> {notes}</p>
  </div>

  <div class="card">
    <h2>Preliminary Recommendations</h2>
    <ul>
      <li>Verify RPM filtering is enabled if using bidirectional DShot.</li>
      <li>Check motor temperature after applying any D-term changes.</li>
      <li>Use a 2–3 minute Blackbox log with hover, cruise, flips, rolls, and descents.</li>
      <li>Set Blackbox debug mode to GYRO_SCALED for best noise analysis.</li>
    </ul>
  </div>

  <div class="card">
    <h2>Copy-Paste CLI Template</h2>
    <pre>
# TuneEZ starter safety profile
set dyn_notch_count = 1
set dyn_notch_q = 500
set dterm_lpf1_dyn_min_hz = 70
set dterm_lpf1_dyn_max_hz = 170
set gyro_lpf1_dyn_min_hz = 80
set gyro_lpf1_dyn_max_hz = 450

save
    </pre>
  </div>

  <a href="/">Run another tune</a>
</body>
</html>
"""
