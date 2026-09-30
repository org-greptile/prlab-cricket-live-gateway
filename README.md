# cricket-live-gateway

Live fan-out. Forwards a `ScoreSnapshot` from scoring to product clients.

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest
SCORING_ORIGIN=http://127.0.0.1:8000 uvicorn gateway.app:app --port 8010
```
