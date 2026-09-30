import os

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from gateway.filter import IngestSnapshot, ProductSnapshot, to_product

app = FastAPI(title="cricket-live-gateway", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

SCORING_ORIGIN = os.environ.get("SCORING_ORIGIN", "http://127.0.0.1:8000")


@app.get("/matches/{match_id}/score", response_model=ProductSnapshot)
def get_score(match_id: str) -> ProductSnapshot:
    try:
        response = httpx.get(
            f"{SCORING_ORIGIN}/matches/{match_id}/score", timeout=2.0
        )
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail="scoring unreachable") from exc
    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="unknown match")
    if response.status_code != 200:
        raise HTTPException(status_code=502, detail="scoring error")
    ingest = IngestSnapshot.model_validate(response.json())
    return to_product(ingest)


@app.post("/ingest", response_model=ProductSnapshot)
def ingest_for_tests(snapshot: IngestSnapshot) -> ProductSnapshot:
    """Direct ingest so hop-2 tests do not need a live scoring process."""
    return to_product(snapshot)
