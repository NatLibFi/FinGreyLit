#!/usr/bin/env python
# coding: utf-8

# # Fine tune Nous Hermes 2 Mistral 7B DPO model using Axolotl framework
# 



# Check if GPU is available
import torch
print('GPU available?', torch.cuda.is_available())
print('BF16 is supported?', torch.cuda.is_bf16_supported())


# In[2]:


# set model name etc.

import sys

MODEL_NAME = "NousResearch/Nous-Hermes-2-Mistral-7B-DPO"
MODEL_SHORT_NAME = MODEL_NAME.split('/')[-1]

if len(sys.argv) == 3:
    TRAIN_SAMPLE = sys.argv[1]
    EPOCHS = sys.argv[2]
else:
    TRAIN_SAMPLE = 0.25
    EPOCHS = 1

print(f"""
MODEL_NAME="{MODEL_NAME}"
TRAIN_SAMPLE="{TRAIN_SAMPLE}"
EPOCHS="{EPOCHS}"
""")

# In[4]:


# Create Axolotl configuration file

CONFIG_FILE = f"config-{MODEL_SHORT_NAME}-{TRAIN_SAMPLE}-{EPOCHS}.yml"


CONFIG = f"""
base_model: {MODEL_NAME}
model_type: AutoModelForCausalLM
tokenizer_type: AutoTokenizer

load_in_8bit: true
load_in_4bit: false
strict: false

dataset_prepared_path: last_run_prepared-{TRAIN_SAMPLE}-{EPOCHS}

datasets:
  - path: train-{TRAIN_SAMPLE}.jsonl
    ds_type: json
    split: train
    type: sharegpt
    conversation: chatml

output_dir: ./out-{MODEL_SHORT_NAME}-{TRAIN_SAMPLE}-{EPOCHS}

#chat_template: chatml

adapter: lora
lora_r: 16
lora_alpha: 32
lora_dropout: 0.05
lora_target_linear: true

sequence_len: 4096
sample_packing: true
eval_sample_packing: false
pad_to_sequence_len: true

wandb_project:
wandb_entity:
wandb_watch:
wandb_name:
wandb_log_model:

gradient_accumulation_steps: 4
micro_batch_size: 2
eval_batch_size: 2
num_epochs: {EPOCHS}
optimizer: adamw_bnb_8bit
lr_scheduler: cosine
learning_rate: 0.0002

train_on_inputs: false
group_by_length: false
bf16: true
fp16: false
tf32: false

gradient_checkpointing: true  # true: saves VRAM but is slower to train
early_stopping_patience:
resume_from_checkpoint:
local_rank:
logging_steps: 1
xformers_attention:
flash_attention: true

warmup_steps: 10
evals_per_epoch: 0
eval_table_size:
eval_table_max_new_tokens: 128
saves_per_epoch: 1
debug:
weight_decay: 0.0
fsdp:
fsdp_config:
special_tokens:

""".strip()

with open(CONFIG_FILE, 'w') as outfile:
    print(CONFIG, file=outfile)


# In[ ]:

import os
os.system(f'../venv/bin/accelerate launch -m axolotl.cli.train {CONFIG_FILE}')



# # Use the fine-tuned model

# In[ ]:


import torch
from peft import PeftModel
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

qlora_model = f"./out-{MODEL_SHORT_NAME}-{TRAIN_SAMPLE}-{EPOCHS}"
base_model = MODEL_NAME
tokenizer = AutoTokenizer.from_pretrained(base_model, use_fast=False)
base_model = AutoModelForCausalLM.from_pretrained(base_model, device_map="auto", torch_dtype=torch.float16, attn_implementation="flash_attention_2").eval()
model = PeftModel.from_pretrained(base_model, qlora_model)



# In[ ]:


# merge the LoRA into the base model for inference
model = model.merge_and_unload()


# In[ ]:


def generate(messages):
    input_ids = tokenizer.apply_chat_template(messages, return_tensors="pt", add_generation_prompt=True)
    output_ids = model.generate(
        torch.as_tensor(input_ids).cuda(),
        #input_ids,
        max_new_tokens=512,
        pad_token_id=tokenizer.pad_token_id,
        eos_token_id=tokenizer.eos_token_id
    )
    output_ids = output_ids[0][len(input_ids[0]):]
    return tokenizer.decode(output_ids, skip_special_tokens=True).strip()


# In[ ]:


import json

test_recs = []
with open('test.jsonl') as infile:
    for line in infile:
        rec = json.loads(line)
        test_recs.append(rec)


with open(f'test-records-{MODEL_SHORT_NAME}-{TRAIN_SAMPLE}-{EPOCHS}.jsonl', 'w') as outfile:
    for rec in test_recs:
        messages = [
            {"role": msg["from"], "content": msg["value"]}
            for msg in rec["conversations"]
            if msg["from"] != "gpt"
        ]
        response = generate(messages)

        ground_truth = rec['conversations'][-1]["value"]

        print(100 * "-")
        print("Ground Truth:")
        print(ground_truth)
        print("Prediction:")
        print(response)

        ground_truth = json.loads(ground_truth)

        try:
            prediction = json.loads(response)
        except json.JSONDecodeError:
            prediction = {}

        # rowid is set to unknown as we've lost it somewhere along the way...
        record = {"ground_truth": ground_truth, "prediction": prediction, "rowid": "unknown"}
        json.dump(record, outfile)
        outfile.write("\n")

# In[ ]:


# Analyze the statistics of the extracted metadata and save to file

import sys
sys.path.append('../..')

from eval import MetadataEvaluator

evaluator = MetadataEvaluator(f'test-records-{MODEL_SHORT_NAME}-{TRAIN_SAMPLE}-{EPOCHS}.jsonl')
results = evaluator.evaluate_records() #prediction_records[:9])

ts_underscore = TRAIN_SAMPLE.replace('.', '_')  # need to avoid . due to how merge-result-tables.py works
statistics_filename = f'lcft-{ts_underscore}-{EPOCHS}.md'
evaluator.save_md(results, statistics_filename)
