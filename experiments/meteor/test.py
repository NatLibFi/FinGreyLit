from eval import evaluate_records


prediction_output_key = "prediction_output"


# def test_title_not_relevant_match():  # TODO Not passing, should it?
#     true_title = None
#     pred_title = "None"  # TODO Is it correct to be mapped to string?
#     records = [
#         {
#             "rowid": "1",
#             "dc.title": true_title,
#             "dc.language.iso": "eng",
#             prediction_output_key: {
#                 "language": {"value": "en"},
#                 "title": {"value": pred_title},
#             },
#         },
#     ]
#     result = evaluate_records(records, prediction_output_key)
#     for res in result:
#         if res["field"] == "title":
#             print(res)
#             assert res["match_type"] == "not-relevant"
#             assert res["score"] == 1


def test_title_exact_match():
    true_title = "My Title"
    pred_title = "My Title"
    records = [
        {
            "rowid": "1",
            "dc.title": true_title,
            "dc.language.iso": "eng",
            prediction_output_key: {
                "language": {"value": "en"},
                "title": {"value": pred_title},
            },
        },
    ]
    result = evaluate_records(records, prediction_output_key)
    for res in result:
        if res["field"] == "title":
            assert res["match_type"] == "exact"
            assert res["score"] == 1


def test_title_not_found():
    true_title = "My Title"
    pred_title = None
    records = [
        {
            "rowid": "1",
            "dc.title": true_title,
            "dc.language.iso": "eng",
            prediction_output_key: {
                "language": {"value": "en"},
                "title": pred_title,
            },
        },
    ]
    result = evaluate_records(records, prediction_output_key)
    for res in result:
        if res["field"] == "title":
            assert res["match_type"] == "not-found"
            assert res["score"] == 0


# def test_title_found_nonexistent():  # TODO Not passing, should it?
#     true_title = None
#     pred_title = "Any Title"
#     records = [
#         {
#             "rowid": "1",
#             "dc.title": true_title,
#             "dc.language.iso": "eng",
#             prediction_output_key: {
#                 "language": {"value": "en"},
#                 "title": pred_title,
#             },
#         },
#     ]
#     result = evaluate_records(records, prediction_output_key)
#     for res in result:
#         if res["field"] == "title":
#             print(res)
#             assert res["match_type"] == "found-nonexistent"
#             assert res["score"] == 0


def test_title_superset_match():
    true_title = "My Title"
    pred_title = "My Title and More"
    records = [
        {
            "rowid": "1",
            "dc.title": true_title,
            "dc.language.iso": "eng",
            prediction_output_key: {
                "language": {"value": "en"},
                "title": {"value": pred_title},
            },
        },
    ]
    result = evaluate_records(records, prediction_output_key)
    for res in result:
        if res["field"] == "title":
            assert res["match_type"] == "superset"
            assert res["score"] == 1


def test_title_case_match():
    true_title = "My Title"
    pred_title = "MY TITLE"
    records = [
        {
            "rowid": "1",
            "dc.title": true_title,
            "dc.language.iso": "eng",
            prediction_output_key: {
                "language": {"value": "en"},
                "title": {"value": pred_title},
            },
        },
    ]
    result = evaluate_records(records, prediction_output_key)
    for res in result:
        if res["field"] == "title":
            assert res["match_type"] == "case"
            assert res["score"] == 1


def test_title_superset_case_match():
    true_title = "My Title"
    pred_title = "MY TITLE AND MORE"
    records = [
        {
            "rowid": "1",
            "dc.title": true_title,
            "dc.language.iso": "eng",
            prediction_output_key: {
                "language": {"value": "en"},
                "title": {"value": pred_title},
            },
        },
    ]
    result = evaluate_records(records, prediction_output_key)
    for res in result:
        if res["field"] == "title":
            assert res["match_type"] == "superset-case"
            assert res["score"] == 1


def test_title_almost_match():
    true_title = "My Long Title"
    pred_title = "My Long Tittle"  # One character difference
    records = [
        {
            "rowid": "1",
            "dc.title": true_title,
            "dc.language.iso": "eng",
            prediction_output_key: {
                "language": {"value": "en"},
                "title": {"value": pred_title},
            },
        },
    ]
    result = evaluate_records(records, prediction_output_key)
    for res in result:
        if res["field"] == "title":
            assert res["match_type"] == "almost"
            assert res["score"] == 1


def test_title_almost_case_match():
    true_title = "My Long Title"
    pred_title = "MY LONG TITTLE"  # One character difference
    records = [
        {
            "rowid": "1",
            "dc.title": true_title,
            "dc.language.iso": "eng",
            prediction_output_key: {
                "language": {"value": "en"},
                "title": {"value": pred_title},
            },
        },
    ]
    result = evaluate_records(records, prediction_output_key)
    for res in result:
        if res["field"] == "title":
            assert res["match_type"] == "almost-case"
            assert res["score"] == 1


def test_title_wrong_match():
    true_title = "My Title"
    pred_title = "Different Title"
    records = [
        {
            "rowid": "1",
            "dc.title": true_title,
            "dc.language.iso": "eng",
            prediction_output_key: {
                "language": {"value": "en"},
                "title": {"value": pred_title},
            },
        },
    ]
    result = evaluate_records(records, prediction_output_key)
    for res in result:
        if res["field"] == "title":
            assert res["match_type"] == "wrong"
            assert res["score"] == 0
