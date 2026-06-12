import streamlit as st
import pandas as pd
import altair as alt

# 1. Page Configuration
st.set_page_config(page_title="Egypt Real Estate Intelligence", layout="wide")

# 2. Luxury Branding (CSS)
st.markdown("<style>main{background-color:#fcfcfc} div[data-testid='stMetricValue']{font-size:32px;color:#d4af37;font-weight:bold} h1{color:#1a2a6c;border-bottom:3px solid #d4af37;padding-bottom:10px} .stAlert{border:1px solid #d4af37;background-color:#fffcf5}</style>", unsafe_allow_html=True)

# 3. Market Data
data = {
    'District': ['New Cairo', 'Sheikh Zayed', 'New Capital', 'Mostakbal City', 'North Coast', 'October City'],
    'Avg_PSQM': [55000, 52000, 42000, 38000, 95000, 28000],
    'Appreciation': [0.28, 0.25, 0.32, 0.30, 0.40, 0.20],
    'Rental_Yield': [0.08, 0.07, 0.09, 0.06, 0.12, 0.06],
    'Demand': [90, 85, 95, 75, 80, 65]
}
df = pd.DataFrame(data)

# 4. Sidebar
st.sidebar.title("🏢 Advisor Portal")
budget = st.sidebar.number_input("Budget (EGP)", 1000000, 100000000, 5000000)
years = st.sidebar.slider("Years", 1, 10, 5)
goal = st.sidebar.selectbox("Goal", ["Balanced", "Capital Growth", "Rental Yield"])

# 5. Main Dashboard
st.title("🏛️ Egypt Real Estate Advisor")
st.markdown("##### Strategic Intelligence for Property Investment")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("#### Market Opportunity Matrix")
    chart = alt.Chart(df).mark_circle(opacity=0.8, stroke='white', strokeWidth=2).encode(
        x=alt.X('Avg_PSQM:Q', title="Price (EGP/sqm)"),
        y=alt.Y('Appreciation:Q', axis=alt.Axis(format='%'), title="Annual Growth"),
        size=alt.Size('Demand:Q', scale=alt.Scale(range=[200, 1000]), legend=None),
        color=alt.Color('District:N', scale=alt.Scale(scheme='goldred')),
        tooltip=['District', 'Avg_PSQM', 'Appreciation']
    ).properties(height=450)
    
    text = chart.mark_text(dy=-30, fontWeight='bold').encode(text='District:N')
    st.altair_chart(chart + text, use_container_width=True)

with col2:
    st.markdown("#### Top Recommendation")
    if goal == "Capital Growth":
        best = df.sort_values('Appreciation', ascending=False).iloc[0]
    elif goal == "Rental Yield":
        best = df.sort_values('Rental_Yield', ascending=False).iloc[0]
    else:
        best = df.sort_values('Demand', ascending=False).iloc[0]
    
    future_val = budget * ((1 + best['Appreciation']) ** years)
    rent = (budget * best['Rental_Yield']) * years
    roi = ((future_val + rent - budget) / budget) * 100

    st.success(f"**Target Zone:** {best['District']}")
    st.metric("Expected Total ROI", f"{roi:.1f}%")
    st.write(f"**Est. Future Value:** EGP {future_val:,.0f}")
    st.write(f"**Total Rental Income:** EGP {rent:,.0f}")
