def test_year_not_relevant_match(evaluator):
    true_year = None
    pred_year = None
    records = [
        {
            "rowid": "1",
            "ground_truth": {
                "dc.date.issued": true_year,
            },
            "prediction": {
                "dc.date.issued": pred_year,
            },
        },
    ]
    result = evaluator.evaluate_records(records)
    assert result[0]["match_type"] == "not-relevant"
    assert result[0]["score"] == 1


def test_year_exact_match(evaluator):
    true_year = "2019-02-15"
    pred_year = "2019"
    records = [
        {
            "rowid": "1",
            "ground_truth": {
                "dc.date.issued": true_year,
            },
            "prediction": {
                "dc.date.issued": pred_year,
            },
        },
    ]
    result = evaluator.evaluate_records(records)
    assert result[0]["match_type"] == "exact"
    assert result[0]["score"] == 1


def test_year_not_found(evaluator):
    true_year = "2019-02-15"
    pred_year = None
    records = [
        {
            "rowid": "1",
            "ground_truth": {
                "dc.date.issued": true_year,
            },
            "prediction": {
                "dc.date.issued": pred_year,
            },
        },
    ]
    result = evaluator.evaluate_records(records)
    assert result[0]["match_type"] == "not-found"
    assert result[0]["score"] == 0


def test_year_found_nonexistent(evaluator):
    true_year = None
    pred_year = "2019"
    records = [
        {
            "rowid": "1",
            "ground_truth": {
                "dc.date.issued": true_year,
            },
            "prediction": {
                "dc.date.issued": pred_year,
            },
        },
    ]
    result = evaluator.evaluate_records(records)
    assert result[0]["match_type"] == "found-nonexistent"
    assert result[0]["score"] == 0


def test_year_wrong_match(evaluator):
    true_year = "2019-02-15"
    pred_year = "2020"
    records = [
        {
            "rowid": "1",
            "ground_truth": {
                "dc.date.issued": true_year,
            },
            "prediction": {
                "dc.date.issued": pred_year,
            },
        },
    ]
    result = evaluator.evaluate_records(records)
    assert result[0]["match_type"] == "wrong"
    assert result[0]["score"] == 0
