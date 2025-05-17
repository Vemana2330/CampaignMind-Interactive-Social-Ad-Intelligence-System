import json
import os

INPUT_FILE = os.path.join(os.path.dirname(__file__), "../models/campaign_finetune_data.jsonl")
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "../models/campaign_finetune_data_50k.jsonl")
MAX_RECORDS = 50000

with open(INPUT_FILE, "r") as infile, open(OUTPUT_FILE, "w") as outfile:
    for i, line in enumerate(infile):
        if i >= MAX_RECORDS:
            break
        outfile.write(line)

print(f"✅ Created {OUTPUT_FILE} with {MAX_RECORDS} records.")
