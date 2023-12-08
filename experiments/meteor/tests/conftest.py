import pytest
from ..eval import MetadataEvaluator


@pytest.fixture
def evaluator():
    return MetadataEvaluator("dummy_filename.jsonl", 'prediction')
