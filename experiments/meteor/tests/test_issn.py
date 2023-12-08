def test_issn_not_relevant_match(evaluator):
    true_issn = None
    pred_issn = None
    records = [
        {
            "rowid": "1",
            "dc.relation.eissn": true_issn,
            "dc.language.iso": "eng",
            "prediction": {
                "dc.relation.eissn": pred_issn,
            },
        },
    ]
    result = evaluator.evaluate_records(records)
    for res in result:
        if res["field"] == "issn":
            assert res["match_type"] == "not-relevant"
            assert res["score"] == 1


def test_issn_exact_match(evaluator):
    true_issn = "123-456-789"
    pred_issn = "123-456-789"  # TODO Why not dash replacement as for ISBN?
    records = [
        {
            "rowid": "1",
            "dc.relation.eissn": true_issn,
            "dc.language.iso": "eng",
            "prediction": {
                "dc.relation.eissn": pred_issn,
            },
        },
    ]
    result = evaluator.evaluate_records(records)
    for res in result:
        if res["field"] == "issn":
            assert res["match_type"] == "exact"
            assert res["score"] == 1


def test_issn_not_found(evaluator):
    true_issn = "123-456-789"
    pred_issn = None
    records = [
        {
            "rowid": "1",
            "dc.relation.eissn": true_issn,
            "dc.language.iso": "eng",
            "prediction": {
                "dc.relation.eissn": pred_issn,
            },
        },
    ]
    result = evaluator.evaluate_records(records)
    for res in result:
        if res["field"] == "issn":
            assert res["match_type"] == "not-found"
            assert res["score"] == 0


def test_issn_found_nonexistent(evaluator):
    true_issn = None
    pred_issn = "123456789"
    records = [
        {
            "rowid": "1",
            "dc.relation.eissn": true_issn,
            "dc.language.iso": "eng",
            "prediction": {
                "dc.relation.eissn": pred_issn,
            },
        },
    ]
    result = evaluator.evaluate_records(records)
    for res in result:
        if res["field"] == "issn":
            assert res["match_type"] == "found-nonexistent"
            assert res["score"] == 0


def test_issn_wrong_match(evaluator):
    true_issn = "123-456-789"
    pred_issn = "000000000"
    records = [
        {
            "rowid": "1",
            "dc.relation.eissn": true_issn,
            "dc.language.iso": "eng",
            "prediction": {
                "dc.relation.eissn": pred_issn,
            },
        },
    ]
    result = evaluator.evaluate_records(records)
    for res in result:
        if res["field"] == "issn":
            assert res["match_type"] == "wrong"
            assert res["score"] == 0


def test_issn_printed_correct_match(evaluator):
    true_pissn = "123-456-789"
    pred_issn = "123-456-789"
    records = [
        {
            "rowid": "1",
            "dc.relation.pissn": true_pissn,  # different field for true value
            "dc.language.iso": "eng",
            "prediction": {
                "dc.relation.eissn": pred_issn,
            },
        },
    ]
    result = evaluator.evaluate_records(records)
    for res in result:
        if res["field"] == "issn":
            assert res["match_type"] == "printed-issn"
            assert res["score"] == 1


def test_issn_printed_wrong_match(evaluator):
    true_eissn = "000-000-000"
    true_pissn = "123-456-789"
    pred_issn = "123-456-789"
    records = [
        {
            "rowid": "1",
            "dc.relation.eissn": true_eissn,
            "dc.relation.pissn": true_pissn,
            "dc.language.iso": "eng",
            "prediction": {
                "dc.relation.eissn": pred_issn,
            },
        },
    ]
    result = evaluator.evaluate_records(records)
    for res in result:
        if res["field"] == "issn":
            assert res["match_type"] == "printed-issn"
            assert res["score"] == 0
