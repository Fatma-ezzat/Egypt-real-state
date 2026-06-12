import streamlit as st
import pandas as pd
import altair as alt
import numpy as np

# 1. Page Configuration & Luxury Branding
st.set_page_config(page_title="Egypt Real Estate Intelligence", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #fcfcfc; }
    [data-testid="stMetricValue"] { color: #d4af37; font-weight: bold; }
    h1 { color: #1a2a6c; border-bottom: 3px solid #d4af37; padding-bottom: 10px; }
    
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
    'Maintenance': [2500, 2000, 3000, 2200, 6000, 1800] 
}
df = pd.DataFrame(data)

# 3. Sidebar - Advisor Portal
st.sidebar.title("🏢 Advisor Portal")
st.sidebar.markdown("---")

# NEW INPUTS
budget = st.sidebar.number_input("Client Maximum Budget (EGP)", 1000000, 100000000, 5000000)
apt_size = st.sidebar.slider("Desired Apartment Size (SQM)", 50, 500, 150)
selected_district = st.sidebar.selectbox("Select Target District", df['District'].unique())
years = st.sidebar.slider("Investment Horizon (Years)", 1, 10, 5)

# --- CALCULATIONS ---
row = df[df['District'] == selected_district].iloc[0]

# Calculate Current Purchase Price
total_purchase_price = apt_size * row['Avg_PSQM']

# Financial Projections
future_price_psqm = row['Avg_PSQM'] * ((1 + row['Appreciation']) ** years)
final_valuation = apt_size * future_price_psqm
total_maintenance = row['Maintenance'] * apt_size * years
total_cost_basis = total_purchase_price + total_maintenance
net_profit = final_valuation - total_cost_basis

# --- MAIN DASHBOARD ---
st.title("🏛️ Egypt Real Estate Intelligence")
st.markdown(f"**Senior Advisor:** Fatma Ezzat | **Market Update:** 2024-2025")

# BUDGET VALIDATION WARNING
if total_purchase_price > budget:
    st.error(f"⚠️ **Budget Alert:** A {apt_size} SQM apartment in {selected_district} costs **EGP {total_purchase_price:,.0f}**, which exceeds your client's budget by **EGP {total_purchase_price - budget:,.0f}**.")
else:
    st.success(f"✅ **Budget Match:** This {apt_size} SQM property fits within the client's EGP {budget:,.0f} budget.")

# --- PREDICTION CARD ---
st.markdown(f"""
    <div class="predict-card">
        <div class="predict-label">Estimated Future Valuation ({years} Years)</div>
        <div class="predict-value">EGP {final_valuation:,.0f}</div>
        <div style="font-size: 18px;">Target Asset: {apt_size} SQM in {selected_district}</div>
        <div style="font-size: 14px; opacity: 0.8;">Current Purchase Price: EGP {total_purchase_price:,.0f}</div>
        <div style="margin-top: 10px; color: #27ae60; font-weight: bold;">
            ↑ Projected Net Profit: EGP {net_profit:,.0f}
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- GRAPHS SECTION ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📈 Portfolio Growth Projection")
    timeline = []
    for y in range(years + 1):
        cost = total_purchase_price + (row['Maintenance'] * apt_size * y)
        val = total_purchase_price * ((1 + row['Appreciation']) ** y)
        timeline.append({'Year': y, 'Type': 'Total Investment (Cost)', 'Value': cost})
        timeline.append({'Year': y, 'Type': 'Market Value (Profit)', 'Value': val})
    
    df_time = pd.DataFrame(timeline)
    line_chart = alt.Chart(df_time).mark_line(point=True).encode(
        x=alt.X('Year:O', title="Years from Purchase"),
        y=alt.Y('Value:Q', title="Value (EGP)"),
        color=alt.Color('Type:N', scale=alt.Scale(range=['#e74c3c', '#27ae60'])),
        tooltip=['Year', 'Type', 'Value']
    ).properties(height=350)
    st.altair_chart(line_chart, use_container_width=True)

with col2:
    st.subheader("📊 Price per SQM Comparison")
    bar_chart = alt.Chart(df).mark_bar().encode(
        x=alt.X('Avg_PSQM:Q', title="EGP per SQM"),
        y=alt.Y('District:N', sort='-x', title=""),
        color=alt.condition(
            alt.datum.District == selected_district,
            alt.value('#d4af37'), alt.value('#34495e')
        )
    ).properties(height=350)
    st.altair_chart(bar_chart, use_container_width=True)

st.markdown("---")

# Row 3: Metrics
c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Total Purchase Price", f"{total_purchase_price:,.0f} EGP")
with c2:
    st.metric("Price per SQM", f"{row['Avg_PSQM']:,.0f} EGP")
with c3:
    st.metric("Total ROI Efficiency", f"{(net_profit/total_purchase_price)*100:.1f}%")

st.info(f"**Advisor Recommendation:** A {apt_size} SQM unit in {selected_district} is a strong asset. "
        f"By Year {years}, the market value is projected to be {final_valuation/total_purchase_price:.1f}x the initial cost.")
