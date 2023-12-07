import pytest
from ..eval import MetadataEvaluator

prediction_output_key = "prediction_output"


@pytest.fixture
def evaluator():
    return MetadataEvaluator("dummy_filename.jsonl", prediction_output_key)
