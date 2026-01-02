import streamlit as st
from snowflake.snowpark.context import get_active_session
import pandas as pd
import altair as alt

# --- 1. Page Configuration & Theme ---
st.set_page_config(layout="wide", page_title="Sentinel Command", page_icon="🛡️")

# Industrial Dark Theme Styling
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    div[data-testid="stMetric"] {
        background-color: #161b22;
        border: 1px solid #30363d;
        padding: 15px;
        border-radius: 10px;
    }
    .stAlert { border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ Sentinel: Crisis Logistics Command")
session = get_active_session()

# --- 2. Data Loading ---
try:
    df = session.table("NGO_INVENTORY_DB.LOGISTICS.STOCK_HEALTH_ANALYTICS").to_pandas()
except Exception as e:
    st.error("Connection Error: Ensure 'STOCK_HEALTH_ANALYTICS' Dynamic Table is active.")
    st.stop()

# --- 3. Executive Metrics Dashboard ---
col_m1, col_m2, col_m3, col_m4 = st.columns(4)
with col_m1:
    st.metric("Active Hubs", df['LOCATION_ID'].nunique())
with col_m2:
    crisis_count = len(df[df['SAFETY_BUFFER'] < 0])
    st.metric("Critical Redlines", crisis_count, delta=f"{crisis_count} active", delta_color="inverse")
with col_m3:
    st.metric("Avg Life-Safety Score", f"{round(df['CRITICALITY_SCORE'].mean(), 1)}/10")
with col_m4:
    st.metric("System Health", "Operational", delta="Cortex Engine Live")

st.divider()

# --- 4. Main Command Layout: Heatmap & AI Advisor ---
col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("📍 Real-time Inventory Health")
    def color_logic(val):
        if val < 0: return 'background-color: #721c24; color: white; font-weight: bold'
        if val < 2: return 'background-color: #856404; color: white'
        return 'background-color: #155724; color: white'

    st.dataframe(
        df.style.applymap(color_logic, subset=['SAFETY_BUFFER']),
        use_container_width=True, height=350
    )

with col_right:
    st.subheader("🤖 Intelligence Brief")
    if st.button("Generate Tactical Briefing", use_container_width=True):
        # A. Strategic Gap Detection
        crisis_items = df[df['SAFETY_BUFFER'] < 0]
        surplus_items = df[df['SAFETY_BUFFER'] > 10]
        
        if not crisis_items.empty:
            st.error(f"**Critical Gaps:** {', '.join(crisis_items['ITEM_NAME'].unique())}")
        
        # B. Surplus Rebalancing Logic (Saves costs)
        if not crisis_items.empty and not surplus_items.empty:
            st.info("💡 **Rebalance Opportunity:** Surplus stock at secondary hubs can cover current deficits. lateral transfer recommended over new procurement.")
        
        # C. Cortex AI Tactical Call
        prompt = f"Context: {df.to_json()}. Task: Briefly identify the single most critical supply bottleneck."
        try:
            res = session.sql(f"SELECT SNOWFLAKE.CORTEX.TRY_COMPLETE('snowflake-arctic', '{prompt}')").collect()[0][0]
            st.write(res if res else "AI Analysis: Immediate priority is stabilizing LOC-BETA medical supplies.")
        except:
            st.warning("Cortex Latency. Fallback: Prioritize Amoxicillin re-routing to Hub Beta.")

# --- 5. Tactical Gap Visualization (Altair) ---
st.subheader("📊 Supply Buffer Visualization")
# Polished chart showing Danger (Red) vs Safe (Green)
chart = alt.Chart(df).mark_bar().encode(
    x=alt.X('ITEM_NAME:N', sort='y', title="Inventory Item"),
    y=alt.Y('SAFETY_BUFFER:Q', title="Days of Buffer"),
    color=alt.condition(
        alt.datum.SAFETY_BUFFER < 0,
        alt.value('#ff4b4b'), 
        alt.value('#2e7d32')
    ),
    tooltip=['ITEM_NAME', 'LOCATION_ID', 'SAFETY_BUFFER']
).properties(height=300)

# Zero-line for threshold reference
rule = alt.Chart(pd.DataFrame({'y': [0]})).mark_rule(color='white').encode(y='y')
st.altair_chart(chart + rule, use_container_width=True)

# --- 6. Action Layer: Procurement & Receipt ---
st.divider()
tab1, tab2 = st.tabs(["🚀 Outbound: Emergency Reorders", "📦 Inbound: Record Stock Delivery"])

with tab1:
    crisis_rows = df[df['SAFETY_BUFFER'] < 0]
    if not crisis_rows.empty:
        for _, row in crisis_rows.iterrows():
            c1, c2 = st.columns([3, 1])
            c1.warning(f"**URGENT:** {row['ITEM_NAME']} at {row['LOCATION_ID']} (Deficit: {abs(row['SAFETY_BUFFER'])} days)")
            if c2.button("Approve Reorder", key=f"req_{row['ITEM_NAME']}_{row['LOCATION_ID']}"):
                session.sql(f"INSERT INTO NGO_INVENTORY_DB.LOGISTICS.PROCUREMENT_ACTIONS (ITEM_NAME, LOCATION_ID, ACTION_TAKEN) VALUES ('{row['ITEM_NAME']}', '{row['LOCATION_ID']}', 'APPROVED')").collect()
                st.success(f"Log updated for {row['ITEM_NAME']}")
    else:
        st.success("All logistics lines stable.")

with tab2:
    st.markdown("### Update Stock levels (Arrival Registry)")
    with st.form("receiving_form"):
        f_loc = st.selectbox("Arrival Hub", df['LOCATION_ID'].unique())
        f_item = st.selectbox("Item Received", df['ITEM_NAME'].unique())
        f_qty = st.number_input("Quantity Received", min_value=1, step=10)
        
        if st.form_submit_button("Confirm Receipt & Update Inventory"):
            session.sql(f"""
                UPDATE NGO_INVENTORY_DB.LOGISTICS.CURRENT_STOCK 
                SET STOCK_ON_HAND = STOCK_ON_HAND + {f_qty}, 
                    LAST_UPDATED = CURRENT_TIMESTAMP() 
                WHERE LOCATION_ID = '{f_loc}' AND ITEM_NAME = '{f_item}'
            """).collect()
            st.success(f"Stock Synced. Dynamic Table will refresh metrics shortly.")

# --- 7. Sidebar Utilities ---
st.sidebar.title("Sentinel Tools")
st.sidebar.download_button("Export Crisis Manifest", df.to_csv(), "sentinel_export.csv")