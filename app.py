import streamlit as st
import pandas as pd
import altair as alt
import numpy as np

# --- 1. LUXURY PAGE CONFIGURATION ---
st.set_page_config(page_title="Egypt Real Estate Intelligence", layout="wide", initial_sidebar_state="expanded")

# Professional CSS for Event Deployment
st.markdown("""
    <style>
    .main { background-color: #f4f7f6; }
    [data-testid="stMetricValue"] { color: #d4af37; font-weight: bold; font-size: 24px; }
    h1 { color: #1a2a6c; border-bottom: 3px solid #d4af37; padding-bottom: 10px; font-family: 'Times New Roman'; }
    .predict-card {
        background-color: #1a2a6c; padding: 25px; border-radius: 15px; color: white;
        border-left: 10px solid #d4af37; box-shadow: 0px 4px 15px rgba(0,0,0,0.2); margin-bottom: 20px;
    }
    .predict-value { font-size: 36px; font-weight: bold; color: #d4af37; }
    .stTable { background-color: white; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE MARKET INTELLIGENCE DATASET (2024/2025) ---
@st.cache_data
def get_market_data():
    return pd.DataFrame({
        'District': ['New Cairo', 'Sheikh Zayed', 'New Capital', 'Mostakbal City', 'North Coast', 'October City'],
        'Avg_PSQM': [55000, 52000, 42000, 38000, 95000, 28000],
        'Appreciation_Rate': [0.28, 0.25, 0.32, 0.30, 0.40, 0.20],
        'Maintenance_Rate': [2500, 2000, 3000, 2200, 6000, 1800]
    })

df = get_market_data()

# --- 3. ADVISOR PORTAL (SIDEBAR) ---
st.sidebar.title("🏢 Strategic Advisor Portal")
st.sidebar.markdown("*Professional Tool for Egypt Construction Market*")
st.sidebar.markdown("---")

currency = st.sidebar.radio("Display Currency", ["EGP", "USD"])
usd_rate = st.sidebar.number_input("USD/EGP Exchange Rate", value=48.5)

budget = st.sidebar.number_input(f"Maximum Budget ({currency})", 1000000, 200000000, 5000000)
# Convert budget to EGP internally for math
internal_budget = budget if currency == "EGP" else budget * usd_rate

apt_size = st.sidebar.slider("Property Size (SQM)", 50, 600, 140)
selected_district = st.sidebar.selectbox("Target Investment Zone", df['District'].unique())
years = st.sidebar.slider("Investment Horizon (Years)", 1, 10, 5)

# --- 4. FINANCIAL CORE CALCULATIONS ---
row = df[df['District'] == selected_district].iloc[0]
total_purchase_price = apt_size * row['Avg_PSQM']

# Generate Year-over-Year Data
investment_updates = []
for y in range(years + 1):
    current_psqm = row['Avg_PSQM'] * ((1 + row['Appreciation_Rate']) ** y)
    market_value = current_psqm * apt_size
    cumulative_cost = total_purchase_price + (row['Maintenance_Rate'] * apt_size * y)
    net_profit = market_value - cumulative_cost
    roi = (net_profit / total_purchase_price) * 100
    
    # Currency adjustment for the table
    conv = 1 if currency == "EGP" else 1/usd_rate
    
    investment_updates.append({
        'Year': f"Year {y}",
        'PSQM': current_psqm * conv,
        'SQM Increase': (current_psqm - row['Avg_PSQM']) * conv if y > 0 else 0,
        'Market Value': market_value * conv,
        'Total Cost': cumulative_cost * conv,
        'Net Profit': net_profit * conv,
        'ROI %': roi
    })

update_df = pd.DataFrame(investment_updates)
final_val = investment_updates[-1]['Market Value']
final_profit = investment_updates[-1]['Net Profit']

# --- 5. DASHBOARD DISPLAY ---
st.title("🏛️ Egypt Real Estate Intelligence Dashboard")
st.markdown(f"**Advisor:** Fatma Ezzat | **Market Status:** High Appreciation Cycle")

# Budget Warning
if total_purchase_price > internal_budget:
    st.error(f"⚠️ **Budget Breach:** Total cost (EGP {total_purchase_price:,.0f}) exceeds your limit by EGP {total_purchase_price - internal_budget:,.0f}")
else:
    st.success(f"✅ **Market Entry Confirmed:** {apt_size} SQM in {selected_district} is within your budget.")

# --- PREDICTION CARD ---
st.markdown(f"""
    <div class="predict-card">
        <div class="predict-label">Predicted Exit Valuation (Year {years})</div>
        <div class="predict-value">{currency} {final_val:,.0f}</div>
        <div style="font-size: 18px;">Target Asset: {apt_size} SQM in {selected_district}</div>
        <div style="margin-top: 10px; color: #27ae60; font-weight: bold;">
            ↑ Projected Net Profit: {currency} {final_profit:,.0f}
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- CHARTS & TRENDS ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📈 Linear Wealth Appreciation Trend")
    # Melt data for Altair
    viz_df = update_df.melt(id_vars='Year', value_vars=['Market Value', 'Total Cost'], var_name='Metric', value_name='Amount')
    
    line_chart = alt.Chart(viz_df).mark_line(point=True, strokeWidth=4).encode(
        x=alt.X('Year:N', sort=None),
        y=alt.Y('Amount:Q', title=f"Value ({currency})"),
        color=alt.Color('Metric:N', scale=alt.Scale(range=['#27ae60', '#e74c3c'])),
        tooltip=['Year', 'Metric', 'Amount']
    ).properties(height=400)
    st.altair_chart(line_chart, use_container_width=True)

with col2:
    st.subheader("📊 Market Share Growth (%)")
    bar_chart = alt.Chart(df).mark_bar().encode(
        x=alt.X('Appreciation_Rate:Q', axis=alt.Axis(format='%')),
        y=alt.Y('District:N', sort='-x'),
        color=alt.condition(alt.datum.District == selected_district, alt.value('#d4af37'), alt.value('#1a2a6c'))
    ).properties(height=400)
    st.altair_chart(bar_chart, use_container_width=True)

# --- 6. THE DYNAMIC WEALTH TABLE ---
st.markdown("---")
st.subheader("📅 Detailed Investment Lifecycle Update")
st.markdown(f"*Year-by-year forecast of SQM price increases and net ROI in {currency}*")

# Formatting the table for professional view
formatted_df = update_df.copy()
formatted_df['PSQM'] = formatted_df['PSQM'].map(lambda x: f"{x:,.0f}")
formatted_df['Market Value'] = formatted_df['Market Value'].map(lambda x: f"{x:,.0f}")
formatted_df['Net Profit'] = formatted_df['Net Profit'].map(lambda x: f"{x:,.0f}")
formatted_df['ROI %'] = formatted_df['ROI %'].map(lambda x: f"{x:.1f}%")
formatted_df['SQM Increase'] = formatted_df['SQM Increase'].map(lambda x: f"+ {x:,.0f}")

st.table(formatted_df[['Year', 'PSQM', 'SQM Increase', 'Market Value', 'Net Profit', 'ROI %']])

# --- 7. FINAL INSIGHTS ---
st.markdown("---")
st.subheader("💡 Advisor Strategic Insights")
c1, c2, c3 = st.columns(3)
with c1:
    st.info(f"**Entry Point:** The current SQM price in {selected_district} is {row['Avg_PSQM']:,.0f} EGP. We expect this to grow by {row['Appreciation_Rate']*100}% annually.")
with c2:
    st.success(f"**Wealth Creation:** The 'Green Gap' between value and cost widens significantly by Year {years}, creating a {final_profit/total_purchase_price:.1f}x return.")
with c3:
    st.warning(f"**Currency Hedge:** In {currency} terms, this property acts as a high-yield asset, protecting capital against inflation better than traditional savings.")
