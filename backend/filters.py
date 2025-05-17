import pandas as pd
from typing import Optional, List, Dict, Any

# Path to your cleaned data file
DATA_PATH = "/Users/vemana/Documents/CampaignMind-Interactive-Social-Ad-Intelligence-System/backend/data/cleaned_campaign_data.csv"

def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH, parse_dates=["Date"])
    if "Year_Quarter" not in df.columns:
        df["Year_Quarter"] = df["Date"].dt.to_period("Q").astype(str)
    return df

def filter_campaigns(
    channel: Optional[List[str]] = None,
    goal: Optional[str] = None,
    audience: Optional[List[str]] = None,
    segment: Optional[str] = None,
    quarter: Optional[List[str]] = None,
    location: Optional[List[str]] = None
) -> Dict[str, Any]:
    df = load_data()

    # Apply filters
    if channel:
        df = df[df["Channel_Used"].isin(channel)]
    if goal:
        df = df[df["Campaign_Goal"] == goal]
    if audience:
        df = df[df["Target_Audience"].isin(audience)]
    if segment:
        df = df[df["Customer_Segment"] == segment]
    if quarter:
        df = df[df["Year_Quarter"].isin(quarter)]
    if location:
        df = df[df["Location"].isin(location)]

    # If no matching data
    if df.empty:
        return {
            "message": "No campaigns match the selected filters.",
            "average_roi": None,
            "average_conversion_rate": None,
            "average_engagement_score": None,
            "average_ctr": None,
            "roi_by_channel": {},
            "conversion_by_channel": {},
            "engagement_by_audience": {},
            "ctr_by_quarter": {},
            "roi_by_location": {},
            "conversion_by_location": {},
            "engagement_by_location": {},
            "ctr_by_location": {}
        }

    # Compute summary stats and grouped breakdowns
    return {
        "message": "Success",
        "average_roi": round(df["ROI"].mean(), 2),
        "average_conversion_rate": round(df["Conversion_Rate"].mean(), 4),
        "average_engagement_score": round(df["Engagement_Score"].mean(), 2),
        "average_ctr": round(df["CTR"].mean(), 4),

        # Platform-based
        "roi_by_channel": df.groupby("Channel_Used")["ROI"].mean().round(2).to_dict(),
        "conversion_by_channel": df.groupby("Channel_Used")["Conversion_Rate"].mean().round(4).to_dict(),

        # Audience- and time-based
        "engagement_by_audience": df.groupby("Target_Audience")["Engagement_Score"].mean().round(2).to_dict(),
        "ctr_by_quarter": df.groupby("Year_Quarter")["CTR"].mean().round(4).to_dict(),

        # Location-based
        "roi_by_location": df.groupby("Location")["ROI"].mean().round(2).to_dict(),
        "conversion_by_location": df.groupby("Location")["Conversion_Rate"].mean().round(4).to_dict(),
        "engagement_by_location": df.groupby("Location")["Engagement_Score"].mean().round(2).to_dict(),
        "ctr_by_location": df.groupby("Location")["CTR"].mean().round(4).to_dict()
    }
