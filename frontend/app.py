import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# FastAPI endpoints
FILTER_API_URL = "http://localhost:8000/filter-campaigns"
PREDICT_API_URL = "http://localhost:8000/predict-campaign-outcome"

st.set_page_config(page_title="Campaign Analyzer", layout="wide")

# Sidebar Navigation
st.sidebar.title("📂 Navigation")
page = st.sidebar.radio("Go to", ["🏠 Landing Page", "📊 Campaign Explorer", "🧠 Campaign Outcome Predictor"])

# ----------------------------
# 🏠 Landing Page
# ----------------------------
if page == "🏠 Landing Page":
    st.title("📢 CampaignMind-Interactive-Social-Ad-Intelligence-System")

    st.markdown("""
    Welcome to **CampaignMind**, an AI-powered campaign analytics platform designed to help businesses understand the effectiveness of their digital advertising strategies.

    ### 💡 What this project does:
    - Allows marketers to explore historical ad performance.
    - Filters campaigns by **platform, audience, goal, customer segment, and location**.
    - Returns key metrics like **ROI**, **CTR**, **Conversion Rate**, and **Engagement Score**.
    - Compares platforms visually for actionable insights.
    - (Coming Soon) Generates natural language insights using LLMs.

    ### 🚀 Tech Stack:
    - **Frontend**: Streamlit
    - **Backend**: FastAPI
    - **Visualization**: Plotly, Matplotlib, Seaborn
    - **Data**: Kaggle - Social Media Advertising Dataset
    - **Modeling**: Fine-tuned BERT for prediction + recommendations
    """)

# ----------------------------
# 📊 Campaign Explorer
# ----------------------------
elif page == "📊 Campaign Explorer":
    st.title("📊 Campaign Explorer")
    st.sidebar.header("Filter Campaigns")

    # Multiselect Filters
    channel = st.sidebar.multiselect("Platform", ["Instagram", "Facebook", "Pinterest", "Twitter"])
    goal = st.sidebar.selectbox("Campaign Goal", ["", "Product Launch", "Increase Sales", "Market Expansion", "Brand Awareness"])
    audience = st.sidebar.multiselect("Target Audience", ["Men 18-24", "Women 18-24", "Men 25-34", "Women 25-34", "Men 35-44", "Women 35-44", "Men 45-60", "Women 45-60", "All Ages"])
    segment = st.sidebar.selectbox("Customer Segment", ["", "Health", "Home", "Technology", "Food", "Fashion"])
    quarter = st.sidebar.multiselect("Quarter", ["2022Q1", "2022Q2", "2022Q3", "2022Q4"])
    location = st.sidebar.multiselect("Location", ["Las Vegas", "Los Angeles", "Austin", "Miami", "New York"])

    if st.sidebar.button("Apply Filters"):
        with st.spinner("Fetching insights..."):
            payload = {
                "channel": channel if channel else None,
                "goal": goal if goal else None,
                "audience": audience if audience else None,
                "segment": segment if segment else None,
                "quarter": quarter if quarter else None,
                "location": location if location else None,
            }

            try:
                response = requests.post(FILTER_API_URL, json=payload)
                result = response.json()

                if result["message"] == "Success":
                    st.subheader("📈 Summary KPIs")
                    k1, k2, k3, k4 = st.columns(4)
                    k1.metric("Avg ROI", result["average_roi"])
                    k2.metric("Avg Conversion Rate", result["average_conversion_rate"])
                    k3.metric("Avg Engagement Score", result["average_engagement_score"])
                    k4.metric("Avg CTR", result["average_ctr"])

                    multi_view = len(channel) > 1 or len(audience) > 1 or len(quarter) > 1 or len(location) > 1

                    def safe_plot(df, chart_fn, **kwargs):
                        if not df.empty:
                            fig = chart_fn(df, **kwargs)
                            st.plotly_chart(fig, use_container_width=True)

                    st.subheader("📊 KPI Visualizations")

                    if multi_view:
                        roi_df = pd.DataFrame({
                            "Platform": list(result["roi_by_channel"].keys()),
                            "ROI": list(result["roi_by_channel"].values())
                        })
                        safe_plot(roi_df, px.bar, x="ROI", y="Platform", orientation='h', color="Platform", title="ROI by Platform")

                        conversion_df = pd.DataFrame({
                            "Platform": list(result["conversion_by_channel"].keys()),
                            "Conversion Rate": list(result["conversion_by_channel"].values())
                        })
                        safe_plot(conversion_df, px.pie, names="Platform", values="Conversion Rate", title="Conversion Rate by Platform")

                        engagement_df = pd.DataFrame({
                            "Audience": list(result["engagement_by_audience"].keys()),
                            "Engagement Score": list(result["engagement_by_audience"].values())
                        })
                        safe_plot(engagement_df, px.box, y="Engagement Score", x="Audience", title="Engagement Score by Audience")

                        ctr_df = pd.DataFrame({
                            "Quarter": list(result["ctr_by_quarter"].keys()),
                            "CTR": list(result["ctr_by_quarter"].values())
                        }).sort_values("Quarter")
                        safe_plot(ctr_df, px.line, x="Quarter", y="CTR", markers=True, title="CTR by Quarter")

                        st.markdown("### 🗺️ KPI Comparisons by Location")

                        roi_loc_df = pd.DataFrame({
                            "Location": list(result["roi_by_location"].keys()),
                            "ROI": list(result["roi_by_location"].values())
                        })
                        safe_plot(roi_loc_df, px.bar, x="Location", y="ROI", color="Location", title="ROI by Location")

                        conv_loc_df = pd.DataFrame({
                            "Location": list(result["conversion_by_location"].keys()),
                            "Conversion Rate": list(result["conversion_by_location"].values())
                        })
                        safe_plot(conv_loc_df, px.pie, names="Location", values="Conversion Rate", title="Conversion Rate by Location")

                        eng_loc_df = pd.DataFrame({
                            "Location": list(result["engagement_by_location"].keys()),
                            "Engagement Score": list(result["engagement_by_location"].values())
                        })
                        safe_plot(eng_loc_df, px.violin, x="Location", y="Engagement Score", color="Location", box=True, title="Engagement Score by Location")

                        ctr_loc_df = pd.DataFrame({
                            "Location": list(result["ctr_by_location"].keys()),
                            "CTR": list(result["ctr_by_location"].values())
                        })
                        safe_plot(ctr_loc_df, px.treemap, path=["Location"], values="CTR", title="CTR by Location")

                    else:
                        st.markdown("### 📍 Detailed Metrics")
                        col1, col2 = st.columns(2)
                        with col1:
                            st.plotly_chart(go.Figure(go.Indicator(
                                mode="gauge+number",
                                value=result["average_roi"],
                                title={'text': f"ROI"},
                                gauge={'axis': {'range': [0, 10]}}
                            )), use_container_width=True)
                        with col2:
                            st.plotly_chart(go.Figure(go.Indicator(
                                mode="number+delta",
                                value=result["average_engagement_score"],
                                delta={"reference": 5},
                                title={"text": "Engagement Score"}
                            )), use_container_width=True)

                        pie_df = pd.DataFrame({
                            "Metric": ["Conversion Rate", "CTR"],
                            "Value": [result["average_conversion_rate"], result["average_ctr"]]
                        })
                        donut = px.pie(pie_df, values='Value', names='Metric', hole=0.4, title="CTR vs Conversion")
                        st.plotly_chart(donut, use_container_width=True)
                else:
                    st.warning(result["message"])
            except Exception as e:
                st.error(f"Backend Error: {e}")

# ----------------------------
# 🧠 Campaign Outcome Predictor
# ----------------------------
elif page == "🧠 Campaign Outcome Predictor":
    st.title("🧠 Campaign Outcome Predictor")

    st.markdown("""
    This module predicts **ROI**, **Conversion Rate**, **Success Probability**, and a **strategic recommendation** 
    for your campaign using a fine-tuned FLAN-T5 model trained on 300,000 campaign records.
    """)

    input_text = st.text_area(
        label="📬 Enter Campaign Description",
        placeholder="e.g. A 15-day Facebook campaign for a product launch targeting Women 45–60 in Austin.",
        height=150
    )

    if st.button("🔍 Predict Outcome"):
        if input_text.strip() == "":
            st.warning("Please enter a campaign description.")
        else:
            with st.spinner("Generating prediction..."):
                try:
                    res = requests.post(PREDICT_API_URL, json={"description": input_text})
                    res.raise_for_status()
                    prediction = res.json()["prediction"]

                    st.success("✅ Prediction")
                    with st.container():
                        st.markdown(
                            f"""
                            <div style='padding: 12px 18px; background-color: #111827; color: #f1f5f9; border-radius: 8px; font-family: monospace; font-size: 16px; white-space: pre-wrap; word-wrap: break-word;'>
                            {prediction}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                except Exception as e:
                    st.error(f"Error: {e}")
