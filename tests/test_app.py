from fastapi.testclient import TestClient

from gateway.app import app

client = TestClient(app)

PAYLOAD = {
    "match_id": "m1",
    "runs": 1,
    "wickets": 0,
    "overs": "0.1",
    "last_event": {
        "display": "1",
        "runs_added": 1,
        "wicket_counted": False,
        "legal_delivery": True,
    },
    "raw_ball": {"extras": {"type": "wide"}},
}


def test_ingest_forwards_raw_ball() -> None:
    response = client.post("/ingest", json=PAYLOAD)
    assert response.status_code == 200
    body = response.json()
    assert body["runs"] == 1
    assert body["raw_ball"]["extras"]["type"] == "wide"
