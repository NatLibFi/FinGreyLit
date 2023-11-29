from eval import evaluate_records


prediction_output_key = "prediction_output"


def test_title_exact_match():
    true_title = "my title"
    pred_title = "my title"
    records = [
        {
            "rowid": "1",
            "dc.title": true_title,
            "dc.language.iso": "eng",
            "prediction_output": {
                "language": {"value": "en"},
                "title": {"value": pred_title},
            },
        },
    ]
    result = evaluate_records(records, prediction_output_key)
    assert len(result) == 7
    for res in result:
        if res["field"] == "title":
            assert res["match_type"] == "exact"
            assert res["score"] == 1
