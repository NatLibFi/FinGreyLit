def test_issn_not_relevant_match(evaluator):
    true_issn = None
    pred_issn = None
    records = [
        {
            "rowid": "1",
            "ground_truth": {
                "dc.relation.eissn": true_issn,
            },
            "prediction": {
                "dc.relation.eissn": pred_issn,
            },
        },
    ]
    result = evaluator.evaluate_records(records)
    assert result[0]["match_type"] == "not-relevant"
    assert result[0]["score"] == 1


def test_issn_exact_match(evaluator):
    true_issn = "123-456-789"
    pred_issn = "123-456-789"  # TODO Why not dash replacement as for ISBN?
    records = [
        {
            "rowid": "1",
            "ground_truth": {
                "dc.relation.eissn": true_issn,
            },
            "prediction": {
                "dc.relation.eissn": pred_issn,
            },
        },
    ]
    result = evaluator.evaluate_records(records)
    assert result[0]["match_type"] == "exact"
    assert result[0]["score"] == 1


def test_issn_not_found(evaluator):
    true_issn = "123-456-789"
    pred_issn = None
    records = [
        {
            "rowid": "1",
            "ground_truth": {
                "dc.relation.eissn": true_issn,
            },
            "prediction": {
                "dc.relation.eissn": pred_issn,
            },
        },
    ]
    result = evaluator.evaluate_records(records)
    assert result[0]["match_type"] == "not-found"
    assert result[0]["score"] == 0


def test_issn_found_nonexistent(evaluator):
    true_issn = None
    pred_issn = "123456789"
    records = [
        {
            "rowid": "1",
            "ground_truth": {
                "dc.relation.eissn": true_issn,
            },
            "prediction": {
                "dc.relation.eissn": pred_issn,
            },
        },
    ]
    result = evaluator.evaluate_records(records)
    assert result[0]["match_type"] == "found-nonexistent"
    assert result[0]["score"] == 0


def test_issn_wrong_match(evaluator):
    true_issn = "123-456-789"
    pred_issn = "000000000"
    records = [
        {
            "rowid": "1",
            "ground_truth": {
                "dc.relation.eissn": true_issn,
            },
            "prediction": {
                "dc.relation.eissn": pred_issn,
            },
        },
    ]
    result = evaluator.evaluate_records(records)
    assert result[0]["match_type"] == "wrong"
    assert result[0]["score"] == 0


def test_issn_printed_correct_match(evaluator):
    true_eissn = None  # No true eissn
    true_pissn = "123-456-789"
    pred_eissn = true_pissn
    records = [
        {
            "rowid": "1",
            "ground_truth": {
                "dc.relation.eissn": true_eissn,
                "dc.relation.pissn": true_pissn,
            },
            "prediction": {
                "dc.relation.eissn": pred_eissn,
            },
        },
    ]
    result = evaluator.evaluate_records(records)
    assert result[0]["match_type"] == "printed-issn"
    assert result[0]["score"] == 1


def test_issn_printed_wrong_match(evaluator):
    true_eissn = "000-000-000"
    true_pissn = "123-456-789"
    pred_eissn = true_pissn
    records = [
        {
            "rowid": "1",
            "ground_truth": {
                "dc.relation.eissn": true_eissn,
                "dc.relation.pissn": true_pissn,
            },
            "prediction": {
                "dc.relation.eissn": pred_eissn,
            },
        },
    ]
    result = evaluator.evaluate_records(records)
    assert result[0]["match_type"] == "printed-issn"
    assert result[0]["score"] == 0
