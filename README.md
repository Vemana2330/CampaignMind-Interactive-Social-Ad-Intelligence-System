# CampaignMind-Interactive-Social-Ad-Intelligence-System

## Technologies Used
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![FastAPI](https://img.shields.io/badge/fastapi-109989?style=for-the-badge&logo=FASTAPI&logoColor=white)](https://fastapi.tiangolo.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)](https://openai.com/)
[![Hugging Face](https://img.shields.io/badge/HuggingFace-FFD21F?style=for-the-badge&logo=huggingface&logoColor=black)](https://huggingface.co/)
[![T5 Model](https://img.shields.io/badge/FLAN--T5--small-20B2AA?style=for-the-badge&logo=google&logoColor=white)](https://huggingface.co/google/flan-t5-small)
[![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com/python/)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-000000?style=for-the-badge&logo=matplotlib&logoColor=white)](https://matplotlib.org/)
[![Scikit-learn](https://img.shields.io/badge/Scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![Pydantic](https://img.shields.io/badge/Pydantic-008000?style=for-the-badge&logo=python&logoColor=white)](https://docs.pydantic.dev/)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/)
[![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)](https://www.python.org/)
[![Seaborn](https://img.shields.io/badge/Seaborn-005571?style=for-the-badge&logo=python&logoColor=white)](https://seaborn.pydata.org/)
[![Google Colab](https://img.shields.io/badge/Google_Colab-F9AB00?style=for-the-badge&logo=googlecolab&logoColor=white)](https://colab.research.google.com/)

## Overview

**CampaignMind** is an AI-powered interactive analytics system that enables businesses to explore, simulate, and predict the outcomes of social media advertising campaigns. With modular pages like **Campaign Explorer**, **Campaign Simulator**, and an AI-driven **Campaign Outcome Predictor**, the platform empowers marketers with actionable insights derived from historical ad data and fine-tuned language models.

It combines real-time visualizations, NLP-powered campaign understanding, and model-based ROI prediction to assist in strategic marketing decisions. Users can either filter campaigns by platform, audience, and objective or describe a campaign in natural language to get predicted KPIs such as ROI, CTR, conversion rate, and success probability—backed by recommendations grounded in prior patterns.


## Problem Statement

In the dynamic world of digital marketing, businesses often struggle to understand which ad campaigns will yield the highest return on investment (ROI) and engagement. While historical campaign data exists, it is rarely leveraged in an intelligent, predictive manner. 

Marketers lack tools that can translate past performance across different platforms, audiences, and regions into actionable predictions and recommendations. Existing dashboards are typically static, offering only descriptive analytics without the ability to simulate or forecast outcomes. This leads to inefficient budget allocation, missed opportunities, and lower campaign effectiveness.

There is a clear need for an intelligent system that not only visualizes campaign KPIs but also predicts future performance and suggests optimizations based on patterns in large-scale advertising data.


## Project Goals

- Build an interactive dashboard for marketers to explore and filter historical social media ad campaign performance.
- Enable multi-criteria filtering by platform, audience, campaign goal, customer segment, location, and quarter.
- Visualize key performance indicators including ROI, CTR, Conversion Rate, and Engagement Score across dimensions.
- Train a fine-tuned BERT model on 50K rows to predict ROI, Conversion Rate, and success likelihood.
- Design a Campaign Outcome Predictor to accept free-text campaign descriptions and return AI-generated KPI estimates.
- Generate personalized recommendations for campaign strategy improvements based on historical patterns and performance gaps.
- Deploy the system using Streamlit (UI) and FastAPI (backend), and allow real-time communication between both services.
- Ensure low-latency response for campaign predictions and integrate confidence scoring for generated outputs.


## Architecture Diagram

<img width="1375" alt="image" src="https://github.com/user-attachments/assets/70c3659c-2c45-4d1c-a3ab-6e61ae7a4866" />

## Application UI

![campaign](https://github.com/user-attachments/assets/4b4583ef-454d-4b65-91c6-0a625497d1be)

## Directory Structure
```
CAMPAIGNMIND-INTERACTIVE-SOCIAL-AD-INTELLIGENCE-SYSTEM/
├── backend/
│   ├── data/
│   │   └── cleaned_campaign_data.csv
│   ├── __init__.py
│   ├── filters.py                   # Filtering logic for Campaign Explorer
│   ├── main.py                      # FastAPI entrypoint
│   └── requirements.txt
├── frontend/
│   ├── .streamlit/
│   │   └── config.toml              # Streamlit configuration
│   ├── app.py                       # Streamlit frontend with 3 pages
│   └── requirements.txt
├── models/
│   ├── flan-t5-lora-campaignmind-300k/
│   │   ├── adapter_config.json
│   │   ├── adapter_model.safetensors
│   │   ├── README.md
│   │   ├── special_tokens_map.json
│   │   ├── spiece.model
│   │   ├── tokenizer_config.json
│   │   └── tokenizer.json
│   ├── campaign_finetune_data_50k.jsonl
│   ├── campaign_finetune_data.jsonl
│   ├── campaign_finetune_data.py
│   ├── check_finetune_status.py
│   ├── finetune_gpt.py
│   ├── generate_finetune_jsonl.py
│   └── inference.py                 # LoRA + FLAN-T5 model loading & inference logic
├── .gitignore
├── LICENSE
└── README.md

```

## Application Workflow

1. Landing Page
   - The user starts at the homepage where the platform overview, features, and tech stack are displayed. Navigation options are presented on the sidebar to explore campaign analytics or AI predictions.

2. Campaign Explorer
  - The user selects campaign filters from dropdown menus:
    - Platform (Instagram, Facebook, Pinterest, Twitter)
    - Campaign Goal (e.g., Product Launch, Increase Sales)
    - Target Audience (e.g., Men 35–44, Women 45–60)
    - Customer Segment (e.g., Health, Home, Technology)
    - Location (e.g., Austin, Las Vegas)
    - Time Period (e.g., Quarter) 
  - Upon applying filters, a request is sent to the FastAPI backend, which processes data using pandas and returns:
    - Summary KPIs (ROI, Conversion Rate, CTR, Engagement Score)
    - Platform-wise and location-based visual comparisons
    - Charts such as bar graphs, line graphs, and pie charts

3. Campaign Outcome Predictor
  - The user can either:
    - Select structured filters (platform, goal, audience), or
    - Enter a free-text campaign description
      - Example: “A 15-day Facebook campaign for a product launch targeting Women 45–60 in Austin.”
  - The input is passed to a fine-tuned FLAN-T5/BERT model via FastAPI.
  - The backend returns a detailed insight that includes:
    - Predicted ROI
    - Predicted Conversion Rate
    - Success Probability (Low, Medium, High)
    - Recommendation sentence comparing platform performance for the given demographic

4. Visualization Output
  - Results from both modules are rendered on the Streamlit UI as:
    - KPI tiles for quick summary
    - Interactive graphs (using Plotly) comparing performance across platforms, locations, and audiences

7. Model Training in Colab
  - The campaign dataset is uploaded to Google Colab.
  - A T5 model is trained on 50,000+ records and downloaded locally.
  - FastAPI loads the model to serve real-time predictions in the app.

## How to run this application locally

1. Clone the Repository
```
git clone https://github.com/your-username/ChronicCare.AI-Multi-Agent-Health-Management-System.git
cd ChronicCare.AI-Multi-Agent-Health-Management-System
```

2. Create and Activate a Virtual Environment
```
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```

3. Install Dependencies
```
pip install -r backend/requirements.txt
pip install -r frontend/requirements.txt
```
4. Start the FastAPI backend(run it from root)
```
uvicorn backend.main:app --reload
```
5. Launch the Streamlit Frontend(In a separate terminal window)
```
cd frontend
streamlit run app.py
```
6. Use the Application
  - 📊 Campaign Explorer – Select filters to explore campaign KPIs.
  - 🧠 Campaign Outcome Predictor – Enter a description to get AI predictions.
  - Visuals and responses will update in real-time between Streamlit and FastAPI.


## References

- https://docs.streamlit.io/
- https://fastapi.tiangolo.com/
- https://huggingface.co/google/flan-t5-small
- https://huggingface.co/docs/transformers/index
- https://arxiv.org/abs/2106.09685
- https://github.com/huggingface/peft
- https://colab.research.google.com/
- https://plotly.com/python/
- https://pandas.pydata.org/docs/
- https://scikit-learn.org/stable/documentation.html
- https://matplotlib.org/stable/contents.html
- https://docs.pydantic.dev/
- https://github.com/google/sentencepiece
- https://www.uvicorn.org/
- https://www.kaggle.com/datasets/fayomi/social-media-ads-performance

