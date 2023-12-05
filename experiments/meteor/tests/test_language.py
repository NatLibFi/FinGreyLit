from ..eval import evaluate_records


prediction_output_key = "prediction_output"


def test_language_not_relevant_match():
    true_language = None
    pred_language = None  # TODO Is it correct to be mapped to string?
    records = [
        {
            "rowid": "1",
            "dc.language.iso": true_language,
            prediction_output_key: {
                "language": pred_language,
            },
        },
    ]
    result = evaluate_records(records, prediction_output_key)
    for res in result:
        if res["field"] == "language":
            assert res["match_type"] == "not-relevant"
            assert res["score"] == 1


def test_language_exact_match():
    true_language = "eng"
    pred_language = "en"
    records = [
        {
            "rowid": "1",
            "dc.language.iso": true_language,
            prediction_output_key: {
                "language": {"value": pred_language},
            },
        },
    ]
    result = evaluate_records(records, prediction_output_key)
    for res in result:
        if res["field"] == "language":
            assert res["match_type"] == "exact"
            assert res["score"] == 1


def test_language_not_found():
    true_language = "eng"
    pred_language = None
    records = [
        {
            "rowid": "1",
            "dc.language.iso": true_language,
            prediction_output_key: {
                "language": pred_language,
            },
        },
    ]
    result = evaluate_records(records, prediction_output_key)
    for res in result:
        if res["field"] == "language":
            assert res["match_type"] == "not-found"
            assert res["score"] == 0


def test_language_found_nonexistent():
    true_language = None
    pred_language = "en"
    records = [
        {
            "rowid": "1",
            "dc.language.iso": true_language,
            prediction_output_key: {
                "language": {"value": pred_language},
            },
        },
    ]
    result = evaluate_records(records, prediction_output_key)
    for res in result:
        if res["field"] == "language":
            assert res["match_type"] == "found-nonexistent"
            assert res["score"] == 0


def test_language_wrong_match():
    true_language = "eng"
    pred_language = "fi"
    records = [
        {
            "rowid": "1",
            "dc.language.iso": true_language,
            prediction_output_key: {
                "language": {"value": pred_language},
            },
        },
    ]
    result = evaluate_records(records, prediction_output_key)
    for res in result:
        if res["field"] == "language":
            assert res["match_type"] == "wrong"
            assert res["score"] == 0