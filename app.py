%%writefile app.py
import streamlit as st
import pandas as pd
import altair as alt

# 1. LUXURY BRANDING (Fixed CSS)
st.set_page_config(page_title="EREI Advisor", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #fcfcfc; }
    div[data-testid="stMetricValue"] { font-size: 28px; color: #d4af37; }
    .stButton>button { background-color: #d4af37; color: white; border-radius: 10px; height: 3em; width: 100%; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. REAL MARKET DATA
data = {
    'District': ['New Cairo', 'Sheikh Zayed', 'New Capital', 'Mostakbal City', 'North Coast', 'October City'],
    'Avg_PSQM': [55000, 52000, 42000, 38000, 95000, 28000],
    'Appreciation': [0.28, 0.25, 0.32, 0.30, 0.40, 0.20],
    'Rental_Yield': [0.08, 0.07, 0.09, 0.06, 0.12, 0.06],
    'Demand': [92, 88, 95, 80, 85, 70]
}
df = pd.DataFrame(data)

# 3. SIDEBAR
st.sidebar.header("Customer Profile")
budget = st.sidebar.number_input("Investment Budget (EGP)", min_value=1000000, value=5000000)
years = st.sidebar.slider("Investment Horizon (Years)", 1, 10, 5)
goal = st.sidebar.selectbox("Primary Goal", ["Capital Growth", "Monthly Rental", "Balanced"])

# 4. MAIN PAGE
st.title("🏛️ Egypt Real Estate Advisor")
st.markdown("### Data-Driven Investment Intelligence")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("#### Market Opportunity Matrix")
    chart = alt.Chart(df).mark_circle(size=1000, opacity=0.8).encode(
        x=alt.X('Avg_PSQM:Q', title="Price per SQM (EGP)"),
        y=alt.Y('Appreciation:Q', axis=alt.Axis(format='%'), title="Annual Growth"),
        size=alt.Size('Demand:Q', scale=alt.Scale(range=[500, 2000])),
        color=alt.Color('District:N', scale=alt.Scale(scheme='goldred')),
        tooltip=['District', 'Avg_PSQM', 'Appreciation']
    ).properties(height=450).interactive()
    
    text = chart.mark_text(dy=-30, fontWeight='bold').encode(text='District:N')
    st.altair_chart(chart + text, use_container_width=True)

with col2:
    st.markdown("#### Top Recommendation")
    if goal == "Capital Growth":
        best = df.sort_values('Appreciation', ascending=False).iloc[0]
    elif goal == "Monthly Rental":
        best = df.sort_values('Rental_Yield', ascending=False).iloc[0]
    else:
        best = df.sort_values('Demand', ascending=False).iloc[0]
    
    future_val = budget * ((1 + best['Appreciation']) ** years)
    rent = (budget * best['Rental_Yield']) * years
    roi = ((future_val + rent - budget) / budget) * 100

    st.success(f"**District:** {best['District']}")
    st.metric("Expected Total ROI", f"{roi:.1f}%")
    st.write(f"**Final Value:** EGP {future_val:,.0f}")
    st.write(f"**Rental Income:** EGP {rent:,.0f}")
    
    st.info("💡 **Advisor Suggestion:** Current liquidity in this zone is high. Focus on 10% downpayment units.")