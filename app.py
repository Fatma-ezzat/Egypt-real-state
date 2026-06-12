import streamlit as st
import pandas as pd
import altair as alt
import numpy as np

# 1. Page Configuration & Luxury Branding
st.set_page_config(page_title="Egypt Real Estate Intelligence", layout="wide")

# Professional CSS for the Prediction Card
st.markdown("""
    <style>
    .main { background-color: #fcfcfc; }
    [data-testid="stMetricValue"] { color: #d4af37; font-weight: bold; }
    h1 { color: #1a2a6c; border-bottom: 3px solid #d4af37; padding-bottom: 10px; }
    
    /* Prediction Card Styling */
    .predict-card {
        background-color: #1a2a6c;
        padding: 30px;
        border-radius: 15px;
        color: white;
        border-left: 10px solid #d4af37;
        box-shadow: 5px 5px 15px rgba(0,0,0,0.1);
        margin-bottom: 25px;
    }
    .predict-value {
        font-size: 40px;
        font-weight: bold;
        color: #d4af37;
        margin: 10px 0;
    }
    .predict-label {
        font-size: 16px;
        text-transform: uppercase;
        letter-spacing: 2px;
        opacity: 0.8;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Market Data (2024/2025 EGP Estimates)
data = {
    'District': ['New Cairo', 'Sheikh Zayed', 'New Capital', 'Mostakbal City', 'North Coast', 'October City'],
    'Avg_PSQM': [55000, 52000, 42000, 38000, 95000, 28000],
    'Appreciation': [0.28, 0.25, 0.32, 0.30, 0.40, 0.20],
    'Maintenance': [2500, 2000, 3000, 2200, 6000, 1800] # Annual EGP per SQM
}
df = pd.DataFrame(data)

# 3. Sidebar - Advisor Portal
st.sidebar.title("🏢 Advisor Portal")
st.sidebar.markdown("---")
budget = st.sidebar.number_input("Client Investment Budget (EGP)", 1000000, 100000000, 5000000)
years = st.sidebar.slider("Investment Horizon (Years)", 1, 10, 5)
selected_district = st.sidebar.selectbox("Select Target District", df['District'].unique())

# --- CALCULATIONS ---
row = df[df['District'] == selected_district].iloc[0]
sqm_purchased = budget / row['Avg_PSQM']
future_price_psqm = row['Avg_PSQM'] * ((1 + row['Appreciation']) ** years)
final_valuation = sqm_purchased * future_price_psqm
total_expenses = budget + (row['Maintenance'] * sqm_purchased * years)
net_profit = final_valuation - total_expenses

# --- MAIN DASHBOARD ---
st.title("🏛️ Egypt Real Estate Intelligence")
st.markdown(f"**Senior Advisor:** Fatma Ezzat | **Market Cycle:** 2024-2025 Update")

# --- NEW: PREDICTION CARD ---
st.markdown(f"""
    <div class="predict-card">
        <div class="predict-label">Future Market Valuation Prediction</div>
        <div class="predict-value">EGP {final_valuation:,.0f}</div>
        <div style="font-size: 18px;">Target Asset: {sqm_purchased:.1f} SQM in {selected_district}</div>
        <div style="margin-top: 10px; color: #27ae60; font-weight: bold;">
            ↑ Expected Net Profit: EGP {net_profit:,.0f}
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- GRAPHS SECTION ---
col1, col2 = st.columns([2, 1])

with col1:
    # GRAPH 1: LINEAR TREND (Profit vs Cost)
    st.subheader("📈 Wealth Creation Projection")
    timeline = []
    for y in range(years + 1):
        cost = budget + (row['Maintenance'] * sqm_purchased * y)
        val = budget * ((1 + row['Appreciation']) ** y)
        timeline.append({'Year': y, 'Type': 'Cost Basis (Initial + Maint.)', 'Value': cost})
        timeline.append({'Year': y, 'Type': 'Market Value (Portfolio)', 'Value': val})
    
    df_time = pd.DataFrame(timeline)
    line_chart = alt.Chart(df_time).mark_line(point=True).encode(
        x=alt.X('Year:O', title="Years from Purchase"),
        y=alt.Y('Value:Q', title="Value (EGP)"),
        color=alt.Color('Type:N', scale=alt.Scale(range=['#e74c3c', '#27ae60'])),
        tooltip=['Year', 'Type', 'Value']
    ).properties(height=350)
    st.altair_chart(line_chart, use_container_width=True)

with col2:
    # GRAPH 2: YoY GROWTH COMPARISON
    st.subheader("📊 Regional Growth Rates")
    bar_chart = alt.Chart(df).mark_bar().encode(
        x=alt.X('Appreciation:Q', axis=alt.Axis(format='%'), title="Annual Gain"),
        y=alt.Y('District:N', sort='-x', title=""),
        color=alt.condition(
            alt.datum.District == selected_district,
            alt.value('#d4af37'), alt.value('#34495e')
        )
    ).properties(height=350)
    st.altair_chart(bar_chart, use_container_width=True)

st.markdown("---")

# Row 3: Investment Insights
st.subheader("💡 Strategic Insights")
c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Avg Entry Price", f"{row['Avg_PSQM']:,.0f} EGP/sqm")
with c2:
    st.metric("Annual Growth", f"{row['Appreciation']*100}%")
with c3:
    st.metric("ROI Efficiency", f"{(net_profit/budget)*100:.1f}%")

st.info(f"**Advisor Recommendation:** Investing in {selected_district} provides a strong hedge against inflation. "
        f"The 'Green Gap' in the trend chart shows that by year {years}, your asset value significantly exceeds your cost basis.")

# Data Table
st.dataframe(df.style.format({'Appreciation': '{:.0%}', 'Avg_PSQM': '{:,.0f} EGP'}))
