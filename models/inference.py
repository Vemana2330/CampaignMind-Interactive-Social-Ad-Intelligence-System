from peft import PeftModel
from transformers import T5Tokenizer, T5ForConditionalGeneration

# ✅ Point to your saved LoRA model directory
MODEL_DIR = "models/flan-t5-lora-campaignmind-300k"

# Load base model
base_model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-small")
tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-small")

# Load LoRA adapter and merge it with the base model
model = PeftModel.from_pretrained(base_model, MODEL_DIR)
model = model.merge_and_unload()  # ✅ Enables .generate()
model.eval()

# Inference
def generate_campaign_prediction(description: str, max_tokens: int = 128):
    input_ids = tokenizer(description, return_tensors="pt").input_ids
    outputs = model.generate(input_ids=input_ids, max_new_tokens=max_tokens)
    result = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return result
