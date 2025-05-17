import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Replace this with your job ID
job_id = "ftjob-e1E4P6VQmM9Jom234wPS5FA9"

response = openai.fine_tuning.jobs.retrieve(job_id)
print("🔍 Fine-tune Job Status:")
print(f"Status: {response.status}")
print(f"Model ID: {response.fine_tuned_model if response.fine_tuned_model else 'N/A'}")
print(f"Created At: {response.created_at}")
