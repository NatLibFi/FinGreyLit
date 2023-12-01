from ..eval import evaluate_records


prediction_output_key = "prediction_output"


# def test_publisher_not_relevant_match():  # TODO Not passing, should it?
#     true_publisher = None
#     pred_publisher = "None"  # TODO Is it correct to be mapped to string?
#     records = [
#         {
#             "rowid": "1",
#             "dc.publisher": true_publisher,
#             "dc.language.iso": "eng",
#             prediction_output_key: {
#                 "language": {"value": "en"},
#                 "publisher": {"value": pred_publisher},
#             },
#         },
#     ]
#     result = evaluate_records(records, prediction_output_key)
#     for res in result:
#         if res["field"] == "publisher":
#             print(res)
#             assert res["match_type"] == "not-relevant"
#             assert res["score"] == 1


def test_publisher_exact_match():
    true_publisher = ["My Publisher"]
    pred_publisher = "My Publisher"
    records = [
        {
            "rowid": "1",
            "dc.publisher": true_publisher,
            "dc.language.iso": "eng",
            prediction_output_key: {
                "language": {"value": "en"},
                "publisher": {"value": pred_publisher},
            },
        },
    ]
    result = evaluate_records(records, prediction_output_key)
    for res in result:
        if res["field"] == "publisher":
            assert res["match_type"] == "exact"
            assert res["score"] == 1


def test_publisher_not_found():
    true_publisher = ["My Publisher"]
    pred_publisher = None
    records = [
        {
            "rowid": "1",
            "dc.publisher": true_publisher,
            "dc.language.iso": "eng",
            prediction_output_key: {
                "language": {"value": "en"},
                "publisher": pred_publisher,
            },
        },
    ]
    result = evaluate_records(records, prediction_output_key)
    for res in result:
        if res["field"] == "publisher":
            assert res["match_type"] == "not-found"
            assert res["score"] == 0


# def test_publisher_found_nonexistent():  # TODO Not passing, should it?
#     true_publisher = None
#     pred_publisher = "Any Publisher"
#     records = [
#         {
#             "rowid": "1",
#             "dc.publisher": true_publisher,
#             "dc.language.iso": "eng",
#             prediction_output_key: {
#                 "language": {"value": "en"},
#                 "publisher": pred_publisher,
#             },
#         },
#     ]
#     result = evaluate_records(records, prediction_output_key)
#     for res in result:
#         if res["field"] == "publisher":
#             print(res)
#             assert res["match_type"] == "found-nonexistent"
#             assert res["score"] == 0


def test_publisher_superset_match():
    true_publisher = ["My Publisher"]
    pred_publisher = "My Publisher and More"
    records = [
        {
            "rowid": "1",
            "dc.publisher": true_publisher,
            "dc.language.iso": "eng",
            prediction_output_key: {
                "language": {"value": "en"},
                "publisher": {"value": pred_publisher},
            },
        },
    ]
    result = evaluate_records(records, prediction_output_key)
    for res in result:
        if res["field"] == "publisher":
            assert res["match_type"] == "superset"
            assert res["score"] == 1


def test_publisher_case_match():
    true_publisher = ["My Publisher"]
    pred_publisher = "MY PUBLISHER"
    records = [
        {
            "rowid": "1",
            "dc.publisher": true_publisher,
            "dc.language.iso": "eng",
            prediction_output_key: {
                "language": {"value": "en"},
                "publisher": {"value": pred_publisher},
            },
        },
    ]
    result = evaluate_records(records, prediction_output_key)
    for res in result:
        if res["field"] == "publisher":
            assert res["match_type"] == "case"
            assert res["score"] == 1


def test_publisher_superset_case_match():
    true_publisher = ["My Publisher"]
    pred_publisher = "MY PUBLISHER AND MORE"
    records = [
        {
            "rowid": "1",
            "dc.publisher": true_publisher,
            "dc.language.iso": "eng",
            prediction_output_key: {
                "language": {"value": "en"},
                "publisher": {"value": pred_publisher},
            },
        },
    ]
    result = evaluate_records(records, prediction_output_key)
    for res in result:
        if res["field"] == "publisher":
            assert res["match_type"] == "superset-case"
            assert res["score"] == 1


def test_publisher_almost_match():
    true_publisher = ["My Long Publisher"]
    pred_publisher = "My Long Publlisher"  # One character difference
    records = [
        {
            "rowid": "1",
            "dc.publisher": true_publisher,
            "dc.language.iso": "eng",
            prediction_output_key: {
                "language": {"value": "en"},
                "publisher": {"value": pred_publisher},
            },
        },
    ]
    result = evaluate_records(records, prediction_output_key)
    for res in result:
        if res["field"] == "publisher":
            assert res["match_type"] == "almost"
            assert res["score"] == 1


def test_publisher_almost_case_match():
    true_publisher = ["My Long Publisher"]
    pred_publisher = "MY LONG PUBLLISHER"  # One character difference
    records = [
        {
            "rowid": "1",
            "dc.publisher": true_publisher,
            "dc.language.iso": "eng",
            prediction_output_key: {
                "language": {"value": "en"},
                "publisher": {"value": pred_publisher},
            },
        },
    ]
    result = evaluate_records(records, prediction_output_key)
    for res in result:
        if res["field"] == "publisher":
            assert res["match_type"] == "almost-case"
            assert res["score"] == 1


def test_publisher_wrong_match():
    true_publisher = ["My Publisher"]
    pred_publisher = "Different Publisher"
    records = [
        {
            "rowid": "1",
            "dc.publisher": true_publisher,
            "dc.language.iso": "eng",
            prediction_output_key: {
                "language": {"value": "en"},
                "publisher": {"value": pred_publisher},
            },
        },
    ]
    result = evaluate_records(records, prediction_output_key)
    for res in result:
        if res["field"] == "publisher":
            assert res["match_type"] == "wrong"
            assert res["score"] == 0
