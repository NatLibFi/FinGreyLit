import sys
import json
import tempfile

from transformers import AutoTokenizer
from vllm import LLM, SamplingParams

sys.path.append('../../eval')

from eval import MetadataEvaluator


base_model = sys.argv[1]
test_set_path = sys.argv[2]
output_path = sys.argv[3]

MAX_MODEL_LEN = 8192
MAX_TOKENS = 2048
TEMPERATURE = 0.5
REPETITION_PENALTY = 1.1

llm = LLM(model=base_model, max_model_len=MAX_MODEL_LEN)
tokenizer = AutoTokenizer.from_pretrained(base_model)

def rec_to_messages(rec):
    return [
        {"role": msg["from"], "content": msg["value"]}
        for msg in rec["conversations"]
        if msg["from"] != "assistant"
    ]

# read the eval records from file
test_recs = []
with open(test_set_path) as testfile:
    for line in testfile:
        test_recs.append(json.loads(line))


prompts = []
for rec in test_recs:
    messages = rec_to_messages(rec)
    if not messages:
        continue
    prompt = tokenizer.apply_chat_template(messages, add_generation_prompt=True, tokenize=False)
    prompts.append(prompt)

sampling_params=SamplingParams(max_tokens=MAX_TOKENS, temperature=TEMPERATURE, repetition_penalty=REPETITION_PENALTY)
outputs = llm.generate(
	prompts=prompts,
	sampling_params=sampling_params
)

generated_texts = [output.outputs[0].text for output in outputs]

#with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete_on_close=False) as tmpf:
with open('test-data.jsonl', 'w') as tmpf:

    # write predictions into a temporary jsonl file, along with ground truth
    for rec, output in zip(test_recs, generated_texts):
        ground_truth = json.loads(rec['conversations'][-1]["value"])
        try:
            prediction = json.loads(output)
        except json.JSONDecodeError:
            prediction = {}
        record = {"ground_truth": ground_truth, "prediction": prediction, "rowid": "unknown"}
        json.dump(record, tmpf)
        tmpf.write("\n")
    tmpf.close()

    # evaluate

    # Analyze the statistics of the extracted metadata and save to file

#    evaluator = MetadataEvaluator(tmpf.name)
    evaluator = MetadataEvaluator('test-data.jsonl')
    results = evaluator.evaluate_records()
    evaluator.save_md(results, output_path)
