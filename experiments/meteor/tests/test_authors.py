prediction_output_key = "prediction_output"


def test_authors_not_relevant_match(evaluator):
    true_authors = []
    pred_authors = []
    records = [
        {
            "rowid": "1",
            "dc.contributor.author": true_authors,
            "dc.language.iso": "eng",
            prediction_output_key: {
                "language": {"value": "en"},
                "authors": pred_authors,
            },
        },
    ]
    result = evaluator.evaluate_records(records)
    for res in result:
        if res["field"] == "authors":
            assert res["match_type"] == "not-relevant"
            assert res["score"] == 1


def test_authors_exact_match(evaluator):
    true_authors = ["Mylastname, Myfirstname"]
    pred_authors = [{"firstname": "Myfirstname", "lastname": "Mylastname"}]
    records = [
        {
            "rowid": "1",
            "dc.contributor.author": true_authors,
            "dc.language.iso": "eng",
            prediction_output_key: {
                "language": {"value": "en"},
                "authors": pred_authors,
            },
        },
    ]
    result = evaluator.evaluate_records(records)
    for res in result:
        if res["field"] == "authors":
            assert res["match_type"] == "exact"
            assert res["score"] == 1


def test_authors_exact_multiple_match(evaluator):
    true_authors = ["Mylastname, Myfirstname", "Myotherlastname, Myotherfirstname"]
    pred_authors = [
        {"firstname": "Myfirstname", "lastname": "Mylastname"},
        {"firstname": "Myotherfirstname", "lastname": "Myotherlastname"},
    ]
    records = [
        {
            "rowid": "1",
            "dc.contributor.author": true_authors,
            "dc.language.iso": "eng",
            prediction_output_key: {
                "language": {"value": "en"},
                "authors": pred_authors,
            },
        },
    ]
    result = evaluator.evaluate_records(records)
    for res in result:
        if res["field"] == "authors":
            assert res["match_type"] == "exact"
            assert res["score"] == 1


def test_authors_not_found(evaluator):
    true_authors = ["Mylastname, Myfirstname"]
    pred_authors = []
    records = [
        {
            "rowid": "1",
            "dc.contributor.author": true_authors,
            "dc.language.iso": "eng",
            prediction_output_key: {
                "language": {"value": "en"},
                "authors": pred_authors,
            },
        },
    ]
    result = evaluator.evaluate_records(records)
    for res in result:
        if res["field"] == "authors":
            assert res["match_type"] == "not-found"
            assert res["score"] == 0


def test_authors_found_nonexistent(evaluator):
    true_authors = []
    pred_authors = [{"firstname": "Myfirstname", "lastname": "Mylastname"}]
    records = [
        {
            "rowid": "1",
            "dc.contributor.author": true_authors,
            "dc.language.iso": "eng",
            prediction_output_key: {
                "language": {"value": "en"},
                "authors": pred_authors,
            },
        },
    ]
    result = evaluator.evaluate_records(records)
    for res in result:
        if res["field"] == "authors":
            assert res["match_type"] == "found-nonexistent"
            assert res["score"] == 0


def test_authors_superset_match(evaluator):
    true_authors = ["Mylastname, Myfirstname"]
    pred_authors = [
        {"firstname": "Myfirstname", "lastname": "Mylastname"},
        {"firstname": "Myotherfirstname", "lastname": "Myotherlastname"},
    ]
    records = [
        {
            "rowid": "1",
            "dc.contributor.author": true_authors,
            "dc.language.iso": "eng",
            prediction_output_key: {
                "language": {"value": "en"},
                "authors": pred_authors,
            },
        },
    ]
    result = evaluator.evaluate_records(records)
    for res in result:
        if res["field"] == "authors":
            assert res["match_type"] == "superset"
            assert res["score"] == 1


def test_authors_subset_match(evaluator):
    true_authors = ["Mylastname, Myfirstname", "Myotherlastname, Myotherfirstname"]
    pred_authors = [{"firstname": "Myfirstname", "lastname": "Mylastname"}]
    records = [
        {
            "rowid": "1",
            "dc.contributor.author": true_authors,
            "dc.language.iso": "eng",
            prediction_output_key: {
                "language": {"value": "en"},
                "authors": pred_authors,
            },
        },
    ]
    result = evaluator.evaluate_records(records)
    for res in result:
        if res["field"] == "authors":
            assert res["match_type"] == "subset"
            assert res["score"] == 0


def test_authors_overlap_match(evaluator):
    true_authors = ["Mylastname, Myfirstname", "Myotherfirstname, Myotherlastname"]
    pred_authors = [
        {"firstname": "Myfirstname", "lastname": "Mylastname"},
        {"firstname": "Myaltfirstname", "lastname": "Myaltlastname"},
    ]
    records = [
        {
            "rowid": "1",
            "dc.contributor.author": true_authors,
            "dc.language.iso": "eng",
            prediction_output_key: {
                "language": {"value": "en"},
                "authors": pred_authors,
            },
        },
    ]
    result = evaluator.evaluate_records(records)
    for res in result:
        if res["field"] == "authors":
            assert res["match_type"] == "overlap"
            assert res["score"] == 0


def test_authors_wrong_match(evaluator):
    true_authors = ["Mylastname, Myfirstname"]
    pred_authors = [{"firstname": "Otherfirst", "lastname": "Otherlast"}]
    records = [
        {
            "rowid": "1",
            "dc.contributor.author": true_authors,
            "dc.language.iso": "eng",
            prediction_output_key: {
                "language": {"value": "en"},
                "authors": pred_authors,
            },
        },
    ]
    result = evaluator.evaluate_records(records)
    for res in result:
        if res["field"] == "authors":
            assert res["match_type"] == "wrong"
            assert res["score"] == 0
