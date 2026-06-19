# TuneEZ v3.0.0 Web + Android Edition

Free/open FPV tuning platform.

## Includes
- FastAPI web app backend
- Browser UI for uploading Blackbox logs and CLI dumps
- Android Capacitor scaffold
- CSV/TSV Blackbox analyzer
- `.bbl/.bfl` hook through `blackbox_decode`
- Betaflight/INAV CLI dump parser
- Build profile intake
- PID/filter recommendation engine
- Confidence/risk scoring
- Explainable findings
- Copy-paste CLI export
- Docker deploy files

## Run locally

```bash
cd app/backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
set PYTHONPATH=%cd%
uvicorn tuneez.api.main:app --reload --host 0.0.0.0 --port 8000
```

Open `http://localhost:8000`.

## Android

```bash
cd app/android
npm install
npm run sync
npx cap open android
```

The Android app wraps the same TuneEZ web UI. Native USB serial extraction is planned as a Capacitor plugin.
