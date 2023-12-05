from ..eval import evaluate_records


prediction_output_key = "prediction_output"


def test_year_not_relevant_match():
    true_year = None
    pred_year = None
    records = [
        {
            "rowid": "1",
            "dc.date.issued": true_year,
            "dc.language.iso": "eng",
            prediction_output_key: {
                "language": {"value": "en"},
                "year": pred_year,
            },
        },
    ]
    result = evaluate_records(records, prediction_output_key)
    for res in result:
        if res["field"] == "year":
            assert res["match_type"] == "not-relevant"
            assert res["score"] == 1


def test_year_exact_match():
    true_year = "2019-02-15"
    pred_year = "2019"
    records = [
        {
            "rowid": "1",
            "dc.date.issued": true_year,
            "dc.language.iso": "eng",
            prediction_output_key: {
                "language": {"value": "en"},
                "year": {"value": pred_year},
            },
        },
    ]
    result = evaluate_records(records, prediction_output_key)
    for res in result:
        if res["field"] == "year":
            assert res["match_type"] == "exact"
            assert res["score"] == 1


def test_year_not_found():
    true_year = "2019-02-15"
    pred_year = None
    records = [
        {
            "rowid": "1",
            "dc.date.issued": true_year,
            "dc.language.iso": "eng",
            prediction_output_key: {
                "language": {"value": "en"},
                "year": pred_year,
            },
        },
    ]
    result = evaluate_records(records, prediction_output_key)
    for res in result:
        if res["field"] == "year":
            assert res["match_type"] == "not-found"
            assert res["score"] == 0


def test_year_found_nonexistent():
    true_year = None
    pred_year = "2019"
    records = [
        {
            "rowid": "1",
            "dc.date.issued": true_year,
            "dc.language.iso": "eng",
            prediction_output_key: {
                "language": {"value": "en"},
                "year": {"value": pred_year},
            },
        },
    ]
    result = evaluate_records(records, prediction_output_key)
    for res in result:
        if res["field"] == "year":
            assert res["match_type"] == "found-nonexistent"
            assert res["score"] == 0


def test_year_wrong_match():
    true_year = "2019-02-15"
    pred_year = "2020"
    records = [
        {
            "rowid": "1",
            "dc.date.issued": true_year,
            "dc.language.iso": "eng",
            prediction_output_key: {
                "language": {"value": "en"},
                "year": {"value": pred_year},
            },
        },
    ]
    result = evaluate_records(records, prediction_output_key)
    for res in result:
        if res["field"] == "year":
            assert res["match_type"] == "wrong"
            assert res["score"] == 0