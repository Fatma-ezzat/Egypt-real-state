import streamlit as st
import pandas as pd
import altair as alt
import numpy as np

# 1. Page Configuration
st.set_page_config(page_title="Egypt Real Estate Intelligence", layout="wide")

# Luxury Branding (CSS)
st.markdown("<style>main{background-color:#fcfcfc} [data-testid='stMetricValue']{color:#d4af37; font-weight:bold} h1{color:#1a2a6c; border-bottom:3px solid #d4af37; padding-bottom:10px}</style>", unsafe_allow_html=True)

# 2. Market Data
data = {
    'District': ['New Cairo', 'Sheikh Zayed', 'New Capital', 'Mostakbal City', 'North Coast', 'October City'],
    'Avg_PSQM': [55000, 52000, 42000, 38000, 95000, 28000],
    'Appreciation': [0.28, 0.25, 0.32, 0.30, 0.40, 0.20],
    'Annual_Maintenance_Cost': [2000, 1800, 2500, 2200, 5000, 1500] # Expenses per SQM per year
}
df = pd.DataFrame(data)

# 3. Sidebar - Advisor Portal
st.sidebar.title("🏢 Advisor Portal")
st.sidebar.info("Adjust the settings below to update the client's forecast.")
budget = st.sidebar.number_input("Investment Budget (EGP)", 1000000, 100000000, 5000000)
years = st.sidebar.slider("Investment Horizon (Years)", 1, 10, 5)

# --- CALCULATIONS ---
# Identify the "Best Area" (Highest Appreciation)
best_district_name = df.sort_values('Appreciation', ascending=False).iloc[0]['District']

# --- GRAPH 1: LINEAR TREND (Expenses vs Profits) ---
# We calculate a timeline for the "Best District"
timeline = []
best_row = df[df['District'] == best_district_name].iloc[0]

for year in range(years + 1):
    total_expenses = budget + (best_row['Annual_Maintenance_Cost'] * (budget/best_row['Avg_PSQM']) * year)
    projected_value = budget * ((1 + best_row['Appreciation']) ** year)
    timeline.append({'Year': year, 'Type': 'Total Expenses (Cost Basis)', 'Value': total_expenses})
    timeline.append({'Year': year, 'Type': 'Projected Market Value (Profit)', 'Value': projected_value})

df_timeline = pd.DataFrame(timeline)

# --- MAIN DASHBOARD ---
st.title("🏛️ Egypt Real Estate Advisor")
st.markdown(f"##### Strategic Analysis for: **{best_district_name}**")

# Row 1: The Linear Trend Graph
st.subheader(f"📈 Investment Growth vs. Expenses (Over {years} Years)")
line_chart = alt.Chart(df_timeline).mark_line(point=True).encode(
    x=alt.X('Year:O', title="Years from Purchase"),
    y=alt.Y('Value:Q', title="EGP Value"),
    color=alt.Color('Type:N', scale=alt.Scale(domain=['Total Expenses (Cost Basis)', 'Projected Market Value (Profit)'], range=['#e74c3c', '#27ae60'])),
    tooltip=['Year', 'Type', 'Value']
).properties(height=400)

st.altair_chart(line_chart, use_container_width=True)

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    # --- GRAPH 2: YEAR OVER YEAR GROWTH ---
    st.subheader("📊 Year-over-Year Growth by Area")
    growth_chart = alt.Chart(df).mark_bar().encode(
        x=alt.X('Appreciation:Q', axis=alt.Axis(format='%'), title="Annual Growth Rate"),
        y=alt.Y('District:N', sort='-x', title="District"),
        color=alt.condition(
            alt.datum.District == best_district_name,
            alt.value('#d4af37'), # Gold for the best
            alt.value('#34495e')  # Dark blue for others
        )
    ).properties(height=300)
    st.altair_chart(growth_chart, use_container_width=True)

with col2:
    # --- GRAPH 3: HIGHLIGHT BEST AREA ---
    st.subheader("🏆 Investment Recommendation")
    
    future_val = budget * ((1 + best_row['Appreciation']) ** years)
    profit = future_val - budget
    
    st.metric(label="Target Area", value=best_district_name)
    st.metric(label="Expected Pure Profit", value=f"EGP {profit:,.0f}", delta=f"{best_row['Appreciation']*100}% Yearly")
    
    st.info(f"**Advisor Strategy:** Based on current data, {best_district_name} is the top choice. The 'Green Gap' between the Red (Expenses) and Green (Market Value) lines above shows your wealth creation potential.")

# Market Table
st.markdown("#### Market Reference Data")
st.dataframe(df.style.format({'Appreciation': '{:.0%}', 'Avg_PSQM': '{:,.0f} EGP'}))
