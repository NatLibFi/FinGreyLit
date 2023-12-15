def test_title_not_relevant_match(evaluator):
    true_title = None
    pred_title = None
    records = [
        {
            "rowid": "1",
            "ground_truth": {
                "dc.title": true_title,
            },
            "prediction": {
                "title": pred_title,
            },
        },
    ]
    result = evaluator.evaluate_records(records)
    assert result[0]["match_type"] == "not-relevant"
    assert result[0]["score"] == 1


def test_title_exact_match(evaluator):
    true_title = "My Title"
    pred_title = "My Title"
    records = [
        {
            "rowid": "1",
            "ground_truth": {
                "dc.title": true_title,
            },
            "prediction": {
                "dc.title": pred_title,
            },
        },
    ]
    result = evaluator.evaluate_records(records)
    assert result[0]["match_type"] == "exact"
    assert result[0]["score"] == 1


def test_title_not_found(evaluator):
    true_title = "My Title"
    pred_title = None
    records = [
        {
            "rowid": "1",
            "ground_truth": {
                "dc.title": true_title,
            },
            "prediction": {
                "dc.title": pred_title,
            },
        },
    ]
    result = evaluator.evaluate_records(records)
    assert result[0]["match_type"] == "not-found"
    assert result[0]["score"] == 0


def test_title_found_nonexistent(evaluator):
    true_title = None
    pred_title = "Any Title"
    records = [
        {
            "rowid": "1",
            "ground_truth": {
                "dc.title": true_title,
            },
            "prediction": {
                "dc.title": pred_title,
            },
        },
    ]
    result = evaluator.evaluate_records(records)
    assert result[0]["match_type"] == "found-nonexistent"
    assert result[0]["score"] == 0


def test_title_superset_match(evaluator):
    true_title = "My Title"
    pred_title = "My Title and More"
    records = [
        {
            "rowid": "1",
            "ground_truth": {
                "dc.title": true_title,
            },
            "prediction": {
                "dc.title": pred_title,
            },
        },
    ]
    result = evaluator.evaluate_records(records)
    assert result[0]["match_type"] == "superset"
    assert result[0]["score"] == 1


def test_title_case_match(evaluator):
    true_title = "My Title"
    pred_title = "MY TITLE"
    records = [
        {
            "rowid": "1",
            "ground_truth": {
                "dc.title": true_title,
            },
            "prediction": {
                "dc.title": pred_title,
            },
        },
    ]
    result = evaluator.evaluate_records(records)
    assert result[0]["match_type"] == "case"
    assert result[0]["score"] == 1


def test_title_superset_case_match(evaluator):
    true_title = "My Title"
    pred_title = "MY TITLE AND MORE"
    records = [
        {
            "rowid": "1",
            "ground_truth": {
                "dc.title": true_title,
            },
            "prediction": {
                "dc.title": pred_title,
            },
        },
    ]
    result = evaluator.evaluate_records(records)
    assert result[0]["match_type"] == "superset-case"
    assert result[0]["score"] == 1


def test_title_almost_match(evaluator):
    true_title = "My Long Title"
    pred_title = "My Long Tittle"  # One character difference
    records = [
        {
            "rowid": "1",
            "ground_truth": {
                "dc.title": true_title,
            },
            "prediction": {
                "dc.title": pred_title,
            },
        },
    ]
    result = evaluator.evaluate_records(records)
    assert result[0]["match_type"] == "almost"
    assert result[0]["score"] == 1


def test_title_almost_case_match(evaluator):
    true_title = "My Long Title"
    pred_title = "MY LONG TITTLE"  # One character difference
    records = [
        {
            "rowid": "1",
            "ground_truth": {
                "dc.title": true_title,
            },
            "prediction": {
                "dc.title": pred_title,
            },
        },
    ]
    result = evaluator.evaluate_records(records)
    assert result[0]["match_type"] == "almost-case"
    assert result[0]["score"] == 1


def test_title_wrong_match(evaluator):
    true_title = "My Title"
    pred_title = "Different Title"
    records = [
        {
            "rowid": "1",
            "ground_truth": {
                "dc.title": true_title,
            },
            "prediction": {
                "dc.title": pred_title,
            },
        },
    ]
    result = evaluator.evaluate_records(records)
    assert result[0]["match_type"] == "wrong"
    assert result[0]["score"] == 0
