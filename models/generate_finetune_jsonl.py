import pandas as pd
import json
import os

INPUT_CSV = os.path.join(os.path.dirname(__file__), "../backend/data/cleaned_campaign_data.csv")
OUTPUT_JSONL = os.path.join(os.path.dirname(__file__), "../models/campaign_finetune_data.jsonl")

def map_success_label(label: int) -> str:
    return {
        0: "Low",
        1: "Medium",
        2: "High"
    }.get(label, "Unknown")

def build_completion(row: pd.Series) -> str:
    recommendation = (
        f"Recommendation: In past campaigns targeting {row['Target_Audience']} in {row['Location']}, "
        f"{row['Channel_Used']} showed {'higher' if row['Engagement_Score'] >= 5 else 'lower'} engagement. "
        f"Consider evaluating Instagram or Pinterest for improved reach."
    )
    return (
        f"Predicted ROI: {round(row['ROI'], 2)}\n"
        f"Predicted Conversion Rate: {round(row['Conversion_Rate'], 4)}\n"
        f"Success Probability: {map_success_label(row['Success_Label'])}\n"
        f"{recommendation}"
    )

def main():
    if not os.path.exists(INPUT_CSV):
        raise FileNotFoundError(f"CSV not found at: {INPUT_CSV}")

    df = pd.read_csv(INPUT_CSV)
    required_cols = [
        "Campaign_Description", "ROI", "Conversion_Rate", "Success_Label",
        "Target_Audience", "Location", "Channel_Used", "Engagement_Score"
    ]

    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Missing column in dataset: {col}")

    with open(OUTPUT_JSONL, "w") as f_out:
        for _, row in df.iterrows():
            prompt = row["Campaign_Description"].strip()
            completion = build_completion(row)

            record = {
                "messages": [
                    {"role": "system", "content": "You are an AI campaign performance predictor."},
                    {"role": "user", "content": prompt},
                    {"role": "assistant", "content": completion}
                ]
            }
            f_out.write(json.dumps(record) + "\n")

    print(f"✅ JSONL file created: {OUTPUT_JSONL}")

if __name__ == "__main__":
    main()
