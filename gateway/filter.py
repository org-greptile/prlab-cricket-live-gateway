"""Forward scoring JSON untouched so hop 3 does not drop overlay fields."""

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
    raw_ball: dict | None = None
    match: dict | None = None
    model_config = {"extra": "allow"}


class IngestSnapshot(BaseModel):
    match_id: str
    runs: int
    wickets: int
    overs: str
    last_event: LastEvent
    raw_ball: dict | None = None
    match: dict | None = None
    model_config = {"extra": "allow"}


def to_product(payload: IngestSnapshot) -> ProductSnapshot:
    return ProductSnapshot.model_validate(payload.model_dump())
