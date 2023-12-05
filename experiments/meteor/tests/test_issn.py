from ..eval import evaluate_records


prediction_output_key = "prediction_output"


def test_issn_not_relevant_match():
    true_issn = None
    pred_issn = None
    records = [
        {
            "rowid": "1",
            "dc.relation.eissn": true_issn,
            "dc.language.iso": "eng",
            prediction_output_key: {
                "language": {"value": "en"},
                "issn": pred_issn,
            },
        },
    ]
    result = evaluate_records(records, prediction_output_key)
    for res in result:
        if res["field"] == "issn":
            assert res["match_type"] == "not-relevant"
            assert res["score"] == 1


def test_issn_exact_match():
    true_issn = "123-456-789"
    pred_issn = "123-456-789"  # TODO Why not dash replacement as for ISBN?
    records = [
        {
            "rowid": "1",
            "dc.relation.eissn": true_issn,
            "dc.language.iso": "eng",
            prediction_output_key: {
                "language": {"value": "en"},
                "issn": {"value": pred_issn},
            },
        },
    ]
    result = evaluate_records(records, prediction_output_key)
    for res in result:
        if res["field"] == "issn":
            assert res["match_type"] == "exact"
            assert res["score"] == 1


def test_issn_not_found():
    true_issn = "123-456-789"
    pred_issn = None
    records = [
        {
            "rowid": "1",
            "dc.relation.eissn": true_issn,
            "dc.language.iso": "eng",
            prediction_output_key: {
                "language": {"value": "en"},
                "issn": pred_issn,
            },
        },
    ]
    result = evaluate_records(records, prediction_output_key)
    for res in result:
        if res["field"] == "issn":
            assert res["match_type"] == "not-found"
            assert res["score"] == 0


def test_issn_found_nonexistent():
    true_issn = None
    pred_issn = "123456789"
    records = [
        {
            "rowid": "1",
            "dc.relation.eissn": true_issn,
            "dc.language.iso": "eng",
            prediction_output_key: {
                "language": {"value": "en"},
                "issn": {"value": pred_issn},
            },
        },
    ]
    result = evaluate_records(records, prediction_output_key)
    for res in result:
        if res["field"] == "issn":
            assert res["match_type"] == "found-nonexistent"
            assert res["score"] == 0


def test_issn_wrong_match():
    true_issn = "123-456-789"
    pred_issn = "000000000"
    records = [
        {
            "rowid": "1",
            "dc.relation.eissn": true_issn,
            "dc.language.iso": "eng",
            prediction_output_key: {
                "language": {"value": "en"},
                "issn": {"value": pred_issn},
            },
        },
    ]
    result = evaluate_records(records, prediction_output_key)
    for res in result:
        if res["field"] == "issn":
            assert res["match_type"] == "wrong"
            assert res["score"] == 0


def test_issn_printed_correct_match():
    true_pissn = "123-456-789"
    pred_issn = "123-456-789"
    records = [
        {
            "rowid": "1",
            "dc.relation.pissn": true_pissn,  # different field for true value
            "dc.language.iso": "eng",
            prediction_output_key: {
                "language": {"value": "en"},
                "issn": {"value": pred_issn},
            },
        },
    ]
    result = evaluate_records(records, prediction_output_key)
    for res in result:
        if res["field"] == "issn":
            assert res["match_type"] == "printed-issn"
            assert res["score"] == 1


def test_issn_printed_wrong_match():
    true_eissn = "000-000-000"
    true_pissn = "123-456-789"
    pred_issn = "123-456-789"
    records = [
        {
            "rowid": "1",
            "dc.relation.eissn": true_eissn,
            "dc.relation.pissn": true_pissn,
            "dc.language.iso": "eng",
            prediction_output_key: {
                "language": {"value": "en"},
                "issn": {"value": pred_issn},
            },
        },
    ]
    result = evaluate_records(records, prediction_output_key)
    for res in result:
        if res["field"] == "issn":
            assert res["match_type"] == "printed-issn"
            assert res["score"] == 0
