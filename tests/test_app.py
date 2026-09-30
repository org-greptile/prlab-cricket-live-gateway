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


def test_ingest_strips_raw_ball() -> None:
    response = client.post("/ingest", json=PAYLOAD)
    assert response.status_code == 200
    body = response.json()
    assert body["runs"] == 1
    assert "raw_ball" not in body


def test_origin_override_picks_the_scoring_host(monkeypatch) -> None:
    import httpx

    seen: list[str] = []

    class Reply:
        status_code = 200

        @staticmethod
        def json() -> dict:
            return {k: v for k, v in PAYLOAD.items() if k != "raw_ball"}

    def fake_get(url: str, timeout: float) -> Reply:
        seen.append(url)
        return Reply()

    monkeypatch.setattr(httpx, "get", fake_get)
    response = client.get("/matches/m1/score", params={"origin": "https://staging.example"})
    assert response.status_code == 200
    assert seen == ["https://staging.example/matches/m1/score"]
