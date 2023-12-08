def test_language_not_relevant_match(evaluator):
    true_language = None
    pred_language = None  # TODO Is it correct to be mapped to string?
    records = [
        {
            "rowid": "1",
            "dc.language.iso": true_language,
            "prediction": {
                "dc.language.iso": pred_language,
            },
        },
    ]
    result = evaluator.evaluate_records(records)
    for res in result:
        if res["field"] == "dc.language.iso":
            assert res["match_type"] == "not-relevant"
            assert res["score"] == 1


def test_language_exact_match(evaluator):
    true_language = "en"
    pred_language = "en"
    records = [
        {
            "rowid": "1",
            "dc.language.iso": true_language,
            "prediction": {
                "dc.language.iso": pred_language,
            },
        },
    ]
    result = evaluator.evaluate_records(records)
    for res in result:
        if res["field"] == "dc.language.iso":
            assert res["match_type"] == "exact"
            assert res["score"] == 1


def test_language_not_found(evaluator):
    true_language = "en"
    pred_language = None
    records = [
        {
            "rowid": "1",
            "dc.language.iso": true_language,
            "prediction": {
                "dc.language.iso": pred_language,
            },
        },
    ]
    result = evaluator.evaluate_records(records)
    for res in result:
        if res["field"] == "dc.language.iso":
            assert res["match_type"] == "not-found"
            assert res["score"] == 0


def test_language_found_nonexistent(evaluator):
    true_language = None
    pred_language = "en"
    records = [
        {
            "rowid": "1",
            "dc.language.iso": true_language,
            "prediction": {
                "dc.language.iso": pred_language,
            },
        },
    ]
    result = evaluator.evaluate_records(records)
    for res in result:
        if res["field"] == "dc.language.iso":
            assert res["match_type"] == "found-nonexistent"
            assert res["score"] == 0


def test_language_wrong_match(evaluator):
    true_language = "en"
    pred_language = "fi"
    records = [
        {
            "rowid": "1",
            "dc.language.iso": true_language,
            "prediction": {
                "dc.language.iso": pred_language,
            },
        },
    ]
    result = evaluator.evaluate_records(records)
    for res in result:
        if res["field"] == "dc.language.iso":
            assert res["match_type"] == "wrong"
            assert res["score"] == 0
