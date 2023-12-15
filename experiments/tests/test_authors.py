def test_authors_not_relevant_match(evaluator):
    true_authors = []
    pred_authors = []
    records = [
        {
            "rowid": "1",
            "ground_truth": {
                "dc.contributor.author": true_authors,
            },
            "prediction": {
                "dc.contributor.author": pred_authors,
            },
        },
    ]
    result = evaluator.evaluate_records(records)
    assert result[0]["match_type"] == "not-relevant"
    assert result[0]["score"] == 1


def test_authors_exact_match(evaluator):
    true_authors = ["Mylastname, Myfirstname"]
    pred_authors = ["Mylastname, Myfirstname"]
    records = [
        {
            "rowid": "1",
            "ground_truth": {
                "dc.contributor.author": true_authors,
            },
            "prediction": {
                "dc.contributor.author": pred_authors,
            },
        },
    ]
    result = evaluator.evaluate_records(records)
    assert result[0]["match_type"] == "exact"
    assert result[0]["score"] == 1


def test_authors_exact_multiple_match(evaluator):
    true_authors = ["Mylastname, Myfirstname", "Myotherlastname, Myotherfirstname"]
    pred_authors = ["Mylastname, Myfirstname", "Myotherlastname, Myotherfirstname"]
    records = [
        {
            "rowid": "1",
            "ground_truth": {
                "dc.contributor.author": true_authors,
            },
            "prediction": {
                "dc.contributor.author": pred_authors,
            },
        },
    ]
    result = evaluator.evaluate_records(records)
    assert result[0]["match_type"] == "exact"
    assert result[0]["score"] == 1


def test_authors_not_found(evaluator):
    true_authors = ["Mylastname, Myfirstname"]
    pred_authors = []
    records = [
        {
            "rowid": "1",
            "ground_truth": {
                "dc.contributor.author": true_authors,
            },
            "prediction": {
                "dc.contributor.author": pred_authors,
            },
        },
    ]
    result = evaluator.evaluate_records(records)
    assert result[0]["match_type"] == "not-found"
    assert result[0]["score"] == 0


def test_authors_found_nonexistent(evaluator):
    true_authors = []
    pred_authors = ["Mylastname, Myfirstname"]
    records = [
        {
            "rowid": "1",
            "ground_truth": {
                "dc.contributor.author": true_authors,
            },
            "prediction": {
                "dc.contributor.author": pred_authors,
            },
        },
    ]
    result = evaluator.evaluate_records(records)
    assert result[0]["match_type"] == "found-nonexistent"
    assert result[0]["score"] == 0


def test_authors_superset_match(evaluator):
    true_authors = ["Mylastname, Myfirstname"]
    pred_authors = [
        "Mylastname, Myfirstname",
        "Myotherlastname, Myotherfirstname",
    ]
    records = [
        {
            "rowid": "1",
            "ground_truth": {
                "dc.contributor.author": true_authors,
            },
            "prediction": {
                "dc.contributor.author": pred_authors,
            },
        },
    ]
    result = evaluator.evaluate_records(records)
    assert result[0]["match_type"] == "superset"
    assert result[0]["score"] == 1


def test_authors_subset_match(evaluator):
    true_authors = ["Mylastname, Myfirstname", "Myotherlastname, Myotherfirstname"]
    pred_authors = ["Mylastname, Myfirstname"]
    records = [
        {
            "rowid": "1",
            "ground_truth": {
                "dc.contributor.author": true_authors,
            },
            "prediction": {
                "dc.contributor.author": pred_authors,
            },
        },
    ]
    result = evaluator.evaluate_records(records)
    assert result[0]["match_type"] == "subset"
    assert result[0]["score"] == 0


def test_authors_overlap_match(evaluator):
    true_authors = ["Mylastname, Myfirstname", "Myotherfirstname, Myotherlastname"]
    pred_authors = [
        "Mylastname, Myfirstname",
        "Myaltlastname, Myaltfirstname",
    ]
    records = [
        {
            "rowid": "1",
            "ground_truth": {
                "dc.contributor.author": true_authors,
            },
            "prediction": {
                "dc.contributor.author": pred_authors,
            },
        },
    ]
    result = evaluator.evaluate_records(records)
    assert result[0]["match_type"] == "overlap"
    assert result[0]["score"] == 0


def test_authors_wrong_match(evaluator):
    true_authors = ["Mylastname, Myfirstname"]
    pred_authors = ["Otherlast, Otherfirst"]
    records = [
        {
            "rowid": "1",
            "ground_truth": {
                "dc.contributor.author": true_authors,
            },
            "prediction": {
                "dc.contributor.author": pred_authors,
            },
        },
    ]
    result = evaluator.evaluate_records(records)
    assert result[0]["match_type"] == "wrong"
    assert result[0]["score"] == 0
