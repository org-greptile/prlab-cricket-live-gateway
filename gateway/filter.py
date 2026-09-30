"""Strip protocol leaks before hop 3 (mobile) sees the snapshot."""

from pydantic import BaseModel


class LastEvent(BaseModel):
    display: str
    runs_added: int
    wicket_counted: bool
    legal_delivery: bool


class ProductSnapshot(BaseModel):
    match_id: str
    runs: int
    wickets: int
    overs: str
    last_event: LastEvent


class IngestSnapshot(BaseModel):
    match_id: str
    runs: int
    wickets: int
    overs: str
    last_event: LastEvent
    model_config = {"extra": "ignore"}


def to_product(payload: IngestSnapshot) -> ProductSnapshot:
    return ProductSnapshot(
        match_id=payload.match_id,
        runs=payload.runs,
        wickets=payload.wickets,
        overs=payload.overs,
        last_event=payload.last_event,
    )
