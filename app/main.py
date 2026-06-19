from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="TuneEZ")

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
      <head><title>TuneEZ</title></head>
      <body style="font-family: Arial; background:#0b1020; color:white; padding:40px;">
        <h1>TuneEZ</h1>
        <p>Free open FPV tuning for everyone.</p>
        <p>Upload Blackbox logs and CLI dumps to analyze PID, filters, noise, motors, and propwash.</p>
      </body>
    </html>
    """
