def test_isbn_not_relevant_match(evaluator):
    true_isbn = None
    pred_isbn = None
    records = [
        {
            "rowid": "1",
            "dc.identifier.isbn": true_isbn,
            "dc.language.iso": "eng",
            "prediction": {
                "dc.identifier.isbn": pred_isbn,
            },
        },
    ]
    result = evaluator.evaluate_records(records)
    for res in result:
        if res["field"] == "dc.identifier.isbn":
            assert res["match_type"] == "not-relevant"
            assert res["score"] == 1


def test_isbn_exact_match(evaluator):
    true_isbn = ["123-456-789"]
    pred_isbn = ["123456789"]
    records = [
        {
            "rowid": "1",
            "dc.identifier.isbn": true_isbn,
            "dc.language.iso": "eng",
            "prediction": {
                "dc.identifier.isbn": pred_isbn,
            },
        },
    ]
    result = evaluator.evaluate_records(records)
    for res in result:
        if res["field"] == "dc.identifier.isbn":
            assert res["match_type"] == "exact"
            assert res["score"] == 1


def test_isbn_not_found(evaluator):
    true_isbn = ["123-456-789"]
    pred_isbn = None
    records = [
        {
            "rowid": "1",
            "dc.identifier.isbn": true_isbn,
            "dc.language.iso": "eng",
            "prediction": {
                "dc.identifier.isbn": pred_isbn,
            },
        },
    ]
    result = evaluator.evaluate_records(records)
    for res in result:
        if res["field"] == "dc.identifier.isbn":
            assert res["match_type"] == "not-found"
            assert res["score"] == 0


def test_isbn_found_nonexistent(evaluator):
    true_isbn = None
    pred_isbn = ["123456789"]
    records = [
        {
            "rowid": "1",
            "dc.identifier.isbn": true_isbn,
            "dc.language.iso": "eng",
            "prediction": {
                "dc.identifier.isbn": pred_isbn,
            },
        },
    ]
    result = evaluator.evaluate_records(records)
    for res in result:
        if res["field"] == "dc.identifier.isbn":
            assert res["match_type"] == "found-nonexistent"
            assert res["score"] == 0


def test_isbn_wrong_match(evaluator):
    true_isbn = ["123-456-789"]
    pred_isbn = ["000000000"]
    records = [
        {
            "rowid": "1",
            "dc.identifier.isbn": true_isbn,
            "dc.language.iso": "eng",
            "prediction": {
                "dc.identifier.isbn": pred_isbn,
            },
        },
    ]
    result = evaluator.evaluate_records(records)
    for res in result:
        if res["field"] == "dc.identifier.isbn":
            assert res["match_type"] == "wrong"
            assert res["score"] == 0


def test_isbn_relation_match(evaluator):
    true_isbn = ["123-456-789"]
    pred_isbn = ["123456789"]
    records = [
        {
            "rowid": "1",
            "dc.relation.isbn": true_isbn,  # different field for true value
            "dc.language.iso": "eng",
            "prediction": {
                "dc.identifier.isbn": pred_isbn,
            },
        },
    ]
    result = evaluator.evaluate_records(records)
    for res in result:
        if res["field"] == "dc.identifier.isbn":
            assert res["match_type"] == "related-isbn"
            assert res["score"] == 0
