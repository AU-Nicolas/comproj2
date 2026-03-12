# Web UI (Flask)

Starter Flask UI scaffold in `web_ui/`, designed to match the provided dashboard mockup and keep backend logic as stubs only.

## Run

From the repo root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r src\web_ui\requirements.txt
python src\web_ui\app.py
```

Then open `http://127.0.0.1:5000/`.

## Routes (stubs only)

- `/` Dashboard
- `/live` Live Status
- `/history` Visit History
- `/sensors` Sensors
- `/settings` Settings
- `/search?q=...` Placeholder search route (no real logic yet)
