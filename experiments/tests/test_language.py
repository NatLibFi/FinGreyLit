def test_language_not_relevant_match(evaluator):
    true_language = None
    pred_language = None  # TODO Is it correct to be mapped to string?
    records = [
        {
            "rowid": "1",
            "ground_truth": {
                "dc.language.iso": true_language,
            },
            "prediction": {
                "dc.language.iso": pred_language,
            },
        },
    ]
    result = evaluator.evaluate_records(records)
    assert result[0]["match_type"] == "not-relevant"
    assert result[0]["score"] == 1


def test_language_exact_match(evaluator):
    true_language = "en"
    pred_language = "en"
    records = [
        {
            "rowid": "1",
            "ground_truth": {
                "dc.language.iso": true_language,
            },
            "prediction": {
                "dc.language.iso": pred_language,
            },
        },
    ]
    result = evaluator.evaluate_records(records)
    assert result[0]["match_type"] == "exact"
    assert result[0]["score"] == 1


def test_language_not_found(evaluator):
    true_language = "en"
    pred_language = None
    records = [
        {
            "rowid": "1",
            "ground_truth": {
                "dc.language.iso": true_language,
            },
            "prediction": {
                "dc.language.iso": pred_language,
            },
        },
    ]
    result = evaluator.evaluate_records(records)
    assert result[0]["match_type"] == "not-found"
    assert result[0]["score"] == 0


def test_language_found_nonexistent(evaluator):
    true_language = None
    pred_language = "en"
    records = [
        {
            "rowid": "1",
            "ground_truth": {
                "dc.language.iso": true_language,
            },
            "prediction": {
                "dc.language.iso": pred_language,
            },
        },
    ]
    result = evaluator.evaluate_records(records)
    assert result[0]["match_type"] == "found-nonexistent"
    assert result[0]["score"] == 0


def test_language_wrong_match(evaluator):
    true_language = "en"
    pred_language = "fi"
    records = [
        {
            "rowid": "1",
            "ground_truth": {
                "dc.language.iso": true_language,
            },
            "prediction": {
                "dc.language.iso": pred_language,
            },
        },
    ]
    result = evaluator.evaluate_records(records)
    assert result[0]["match_type"] == "wrong"
    assert result[0]["score"] == 0
