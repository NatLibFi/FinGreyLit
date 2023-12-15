def test_isbn_not_relevant_match(evaluator):
    true_isbn = None
    pred_isbn = None
    records = [
        {
            "rowid": "1",
            "ground_truth": {
                "dc.identifier.isbn": true_isbn,
            },
            "prediction": {
                "dc.identifier.isbn": pred_isbn,
            },
        },
    ]
    result = evaluator.evaluate_records(records)
    assert result[0]["match_type"] == "not-relevant"
    assert result[0]["score"] == 1


def test_isbn_exact_match(evaluator):
    true_isbn = ["123-456-789"]
    pred_isbn = ["123456789"]
    records = [
        {
            "rowid": "1",
            "ground_truth": {
                "dc.identifier.isbn": true_isbn,
            },
            "prediction": {
                "dc.identifier.isbn": pred_isbn,
            },
        },
    ]
    result = evaluator.evaluate_records(records)
    assert result[0]["match_type"] == "exact"
    assert result[0]["score"] == 1


def test_isbn_not_found(evaluator):
    true_isbn = ["123-456-789"]
    pred_isbn = None
    records = [
        {
            "rowid": "1",
            "ground_truth": {
                "dc.identifier.isbn": true_isbn,
            },
            "prediction": {
                "dc.identifier.isbn": pred_isbn,
            },
        },
    ]
    result = evaluator.evaluate_records(records)
    assert result[0]["match_type"] == "not-found"
    assert result[0]["score"] == 0


def test_isbn_found_nonexistent(evaluator):
    true_isbn = None
    pred_isbn = ["123456789"]
    records = [
        {
            "rowid": "1",
            "ground_truth": {
                "dc.identifier.isbn": true_isbn,
            },
            "prediction": {
                "dc.identifier.isbn": pred_isbn,
            },
        },
    ]
    result = evaluator.evaluate_records(records)
    assert result[0]["match_type"] == "found-nonexistent"
    assert result[0]["score"] == 0


def test_isbn_wrong_match(evaluator):
    true_isbn = ["123-456-789"]
    pred_isbn = ["000000000"]
    records = [
        {
            "rowid": "1",
            "ground_truth": {
                "dc.identifier.isbn": true_isbn,
            },
            "prediction": {
                "dc.identifier.isbn": pred_isbn,
            },
        },
    ]
    result = evaluator.evaluate_records(records)
    assert result[0]["match_type"] == "wrong"
    assert result[0]["score"] == 0


def test_isbn_relation_match(evaluator):
    true_isbn = ["123-456-789"]
    pred_isbn = ["123456789"]
    records = [
        {
            "rowid": "1",
            "ground_truth": {
                "dc.relation.isbn": true_isbn,  # different field for true value
            },
            "prediction": {
                "dc.identifier.isbn": pred_isbn,
            },
        },
    ]
    result = evaluator.evaluate_records(records)
    assert result[0]["match_type"] == "related-isbn"
    assert result[0]["score"] == 0
