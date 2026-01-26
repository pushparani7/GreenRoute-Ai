from __future__ import annotations

import requests
import streamlit as st
import plotly.graph_objects as go

API_URL = "http://localhost:8000/route"

st.set_page_config(page_title="GreenRoute AI", layout="wide")

# Initialize session state for tracking totals
if "total_carbon_saved" not in st.session_state:
    st.session_state.total_carbon_saved = 0.0
if "total_water_saved" not in st.session_state:
    st.session_state.total_water_saved = 0.0
if "total_emissions_carbon" not in st.session_state:
    st.session_state.total_emissions_carbon = 0.0
if "total_emissions_water" not in st.session_state:
    st.session_state.total_emissions_water = 0.0
if "query_history" not in st.session_state:
    st.session_state.query_history = []

st.title("GreenRoute AI")
st.caption("Carbon-aware model routing dashboard")

# Input form
with st.form("chat_form"):
    user_query = st.text_input("Ask a question", placeholder="e.g., What is the capital of France?")
    submitted = st.form_submit_button("Route", use_container_width=True)

# Process query when submitted
if submitted and user_query:
    try:
        with st.spinner("Routing query..."):
            response = requests.post(API_URL, json={"query": user_query}, timeout=10)
            response.raise_for_status()
            payload = response.json()
        
        # Update session state with cumulative totals
        st.session_state.total_carbon_saved += payload["carbon_saved_g"]
        st.session_state.total_water_saved += payload["water_saved_ml"]
        st.session_state.total_emissions_carbon += payload["emissions_carbon_g"]
        st.session_state.total_emissions_water += payload["emissions_water_ml"]
        
        # Add to history
        st.session_state.query_history.append({
            "query": user_query,
            "route": payload["route"],
            "model": payload["model"],
            "carbon_saved": payload["carbon_saved_g"],
            "water_saved": payload["water_saved_ml"],
            "emissions_carbon": payload["emissions_carbon_g"],
            "emissions_water": payload["emissions_water_ml"],
        })
        
        # Success message with details
        st.success(
            f"✅ Routed to **{payload['model']}** via **{payload['route']}** route\n\n"
            f"**This Query:**\n"
            f"- Emissions: {payload['emissions_carbon_g']:.4f}g CO₂, {payload['emissions_water_ml']:.2f}ml water\n"
            f"- Saved: {payload['carbon_saved_g']:.4f}g CO₂, {payload['water_saved_ml']:.2f}ml water"
        )
        
    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to API. Is uvicorn running on http://localhost:8000?")
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")

# Display metrics
st.divider()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Carbon Saved",
        f"{st.session_state.total_carbon_saved:.4f}g",
        delta=f"{st.session_state.total_carbon_saved:.4f}g"
    )

with col2:
    st.metric(
        "Total Water Saved",
        f"{st.session_state.total_water_saved:.2f}ml",
        delta=f"{st.session_state.total_water_saved:.2f}ml"
    )

with col3:
    st.metric(
        "Total CO₂ Emitted",
        f"{st.session_state.total_emissions_carbon:.4f}g",
        delta=f"{st.session_state.total_emissions_carbon:.4f}g"
    )

with col4:
    st.metric(
        "Total Water Used",
        f"{st.session_state.total_emissions_water:.2f}ml",
        delta=f"{st.session_state.total_emissions_water:.2f}ml"
    )

st.divider()

# Display progress bars
st.divider()
st.subheader("📊 Environmental Impact")

col1, col2 = st.columns(2)

with col1:
    st.write("**Carbon Savings Progress**")
    # Show progress (assume 10g is a good target)
    progress = min(st.session_state.total_carbon_saved / 10, 1.0)
    st.progress(progress)
    st.caption(f"Goal: 10g CO₂ | Current: {st.session_state.total_carbon_saved:.4f}g")

with col2:
    st.write("**Water Conservation Progress**")
    # Show progress (assume 100ml is a good target)
    progress = min(st.session_state.total_water_saved / 100, 1.0)
    st.progress(progress)
    st.caption(f"Goal: 100ml | Current: {st.session_state.total_water_saved:.2f}ml")

# Display emissions breakdown with bar chart
st.divider()
st.subheader("📈 Emissions Breakdown")

if st.session_state.query_history:
    # Create bar chart data
    queries = [entry["query"][:30] + "..." if len(entry["query"]) > 30 else entry["query"] 
               for entry in st.session_state.query_history]
    emissions = [entry["emissions_carbon"] for entry in st.session_state.query_history]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=queries,
        y=emissions,
        name="CO₂ Emissions (g)",
        marker_color='indianred'
    ))
    fig.update_layout(
        title="CO₂ Emissions per Query",
        xaxis_title="Query",
        yaxis_title="CO₂ (g)",
        height=400,
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("📝 No queries yet. Ask a question to see emissions breakdown!")

# Display query history
if st.session_state.query_history:
    st.divider()
    st.subheader("📋 Query History")
    
    for i, entry in enumerate(st.session_state.query_history, 1):
        with st.expander(f"{i}. {entry['query'][:50]}..."):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Route:** {entry['route']}")
                st.write(f"**Model:** {entry['model']}")
            with col2:
                st.write(f"**Emissions:** {entry['emissions_carbon']:.4f}g CO₂, {entry['emissions_water']:.2f}ml water")
                st.write(f"**Saved:** {entry['carbon_saved']:.4f}g CO₂, {entry['water_saved']:.2f}ml water")