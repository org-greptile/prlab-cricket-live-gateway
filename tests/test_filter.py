from gateway.filter import IngestSnapshot, to_product


def test_product_snapshot_forwards_totals() -> None:
    product = to_product(
        IngestSnapshot.model_validate(
            {
                "match_id": "m1",
                "runs": 10,
                "wickets": 1,
                "overs": "2.3",
                "last_event": {
                    "display": "WICKET",
                    "runs_added": 0,
                    "wicket_counted": True,
                    "legal_delivery": True,
                },
            }
        )
    )
    assert product.wickets == 1
    assert product.last_event.wicket_counted is True


def test_leaks_are_forwarded_to_mobile() -> None:
    product = to_product(
        IngestSnapshot.model_validate(
            {
                "match_id": "m1",
                "runs": 0,
                "wickets": 0,
                "overs": "0.1",
                "last_event": {
                    "display": "NOT_OUT",
                    "runs_added": 0,
                    "wicket_counted": False,
                    "legal_delivery": True,
                },
                "raw_ball": {"wicket": {"kind": "lbw"}},
                "match": {
                    "innings": {
                        "latest_over": {
                            "latest_delivery": {
                                "wicket": {"kind": "lbw", "umpire_confirmed": False}
                            }
                        }
                    }
                },
            }
        )
    )
    dumped = product.model_dump()
    assert dumped["raw_ball"]["wicket"]["kind"] == "lbw"
    assert (
        dumped["match"]["innings"]["latest_over"]["latest_delivery"]["wicket"]["kind"]
        == "lbw"
    )
