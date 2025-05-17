import openai
import os
import time
from dotenv import load_dotenv

# Load OpenAI API key from .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Path to the training file (must be JSONL)
TRAINING_FILE = "/Users/vemana/Documents/CampaignMind-Interactive-Social-Ad-Intelligence-System/models/campaign_finetune_data_50k.jsonl"

def upload_file():
    print("🔼 Uploading training file...")
    file = openai.files.create(
        file=open(TRAINING_FILE, "rb"),
        purpose="fine-tune"
    )
    print(f"✅ File uploaded with ID: {file.id}")
    return file.id

def fine_tune(file_id):
    print("🚀 Starting fine-tuning...")
    response = openai.fine_tuning.jobs.create(
        training_file=file_id,
        model="gpt-3.5-turbo"
        # ⛔ GPT-4o and GPT-4o-mini are not fine-tuneable (yet)
    )
    print("🎯 Fine-tune job created!")
    print(f"Job ID: {response.id}")
    return response.id

def monitor_job(job_id):
    print("⏱ Monitoring fine-tune job...")
    while True:
        job = openai.fine_tuning.jobs.retrieve(job_id)
        status = job.status
        print(f"Status: {status}")
        if status in ["succeeded", "failed", "cancelled"]:
            print("✅ Job finished.")
            print("📘 Model ID:", job.fine_tuned_model or "N/A")
            break
        time.sleep(30)

def main():
    file_id = upload_file()
    job_id = fine_tune(file_id)
    monitor_job(job_id)

if __name__ == "__main__":
    main()
