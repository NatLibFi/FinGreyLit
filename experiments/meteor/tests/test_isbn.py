from ..eval import evaluate_records


prediction_output_key = "prediction_output"


def test_isbn_not_relevant_match():
    true_isbn = None
    pred_isbn = None
    records = [
        {
            "rowid": "1",
            "dc.identifier.isbn": true_isbn,
            "dc.language.iso": "eng",
            prediction_output_key: {
                "language": {"value": "en"},
                "isbn": pred_isbn,
            },
        },
    ]
    result = evaluate_records(records, prediction_output_key)
    for res in result:
        if res["field"] == "isbn":
            assert res["match_type"] == "not-relevant"
            assert res["score"] == 1


def test_isbn_exact_match():
    true_isbn = ["123-456-789"]
    pred_isbn = "123456789"
    records = [
        {
            "rowid": "1",
            "dc.identifier.isbn": true_isbn,
            "dc.language.iso": "eng",
            prediction_output_key: {
                "language": {"value": "en"},
                "isbn": {"value": pred_isbn},
            },
        },
    ]
    result = evaluate_records(records, prediction_output_key)
    for res in result:
        if res["field"] == "isbn":
            assert res["match_type"] == "exact"
            assert res["score"] == 1


def test_isbn_not_found():
    true_isbn = ["123-456-789"]
    pred_isbn = None
    records = [
        {
            "rowid": "1",
            "dc.identifier.isbn": true_isbn,
            "dc.language.iso": "eng",
            prediction_output_key: {
                "language": {"value": "en"},
                "isbn": pred_isbn,
            },
        },
    ]
    result = evaluate_records(records, prediction_output_key)
    for res in result:
        if res["field"] == "isbn":
            assert res["match_type"] == "not-found"
            assert res["score"] == 0


def test_isbn_found_nonexistent():
    true_isbn = None
    pred_isbn = "123456789"
    records = [
        {
            "rowid": "1",
            "dc.identifier.isbn": true_isbn,
            "dc.language.iso": "eng",
            prediction_output_key: {
                "language": {"value": "en"},
                "isbn": {"value": pred_isbn},
            },
        },
    ]
    result = evaluate_records(records, prediction_output_key)
    for res in result:
        if res["field"] == "isbn":
            assert res["match_type"] == "found-nonexistent"
            assert res["score"] == 0


def test_isbn_wrong_match():
    true_isbn = ["123-456-789"]
    pred_isbn = "000000000"
    records = [
        {
            "rowid": "1",
            "dc.identifier.isbn": true_isbn,
            "dc.language.iso": "eng",
            prediction_output_key: {
                "language": {"value": "en"},
                "isbn": {"value": pred_isbn},
            },
        },
    ]
    result = evaluate_records(records, prediction_output_key)
    for res in result:
        if res["field"] == "isbn":
            assert res["match_type"] == "wrong"
            assert res["score"] == 0


def test_isbn_relation_match():
    true_isbn = ["123-456-789"]
    pred_isbn = "123456789"
    records = [
        {
            "rowid": "1",
            "dc.relation.isbn": true_isbn,  # different field for true value
            "dc.language.iso": "eng",
            prediction_output_key: {
                "language": {"value": "en"},
                "isbn": {"value": pred_isbn},
            },
        },
    ]
    result = evaluate_records(records, prediction_output_key)
    for res in result:
        if res["field"] == "isbn":
            assert res["match_type"] == "related-isbn"
            assert res["score"] == 0
