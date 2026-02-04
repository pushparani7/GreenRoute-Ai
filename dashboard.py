from __future__ import annotations

import requests
import streamlit as st
import plotly.graph_objects as go
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="GreenRoute AI",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
    <style>
    :root {
        --primary: #1a472a;
        --secondary: #2d6a4f;
        --accent: #52b788;
        --text-dark: #1a1a1a;
        --text-light: #666666;
        --border-color: #e0e0e0;
    }
    
    * { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }
    
    .header-section {
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        color: white;
        padding: 3rem 2rem;
        margin: -1rem -1rem 2rem -1rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    }
    
    .header-section h1 {
        font-size: 2.8rem;
        font-weight: 700;
        margin: 0;
    }
    
    .header-section p {
        font-size: 1.1rem;
        margin: 0.5rem 0 0 0;
        opacity: 0.95;
    }
    
    .section-header {
        font-size: 1.8rem;
        font-weight: 700;
        color: var(--primary);
        margin: 2.5rem 0 1.5rem 0;
        border-bottom: 2px solid var(--accent);
        padding-bottom: 0.5rem;
    }
    
    .metric-container {
        background: white;
        border: 1px solid var(--border-color);
        border-radius: 8px;
        padding: 1.75rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
    }
    
    .metric-container:hover {
        box-shadow: 0 8px 24px rgba(82, 183, 136, 0.15);
        transform: translateY(-4px);
    }
    
    .metric-label {
        font-size: 0.85rem;
        font-weight: 600;
        color: var(--text-light);
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.75rem;
    }
    
    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: var(--primary);
    }
    
    .badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.9rem;
        margin-right: 0.5rem;
    }
    
    .badge-auto {
        background-color: #e8f5e9;
        color: #1b5e20;
    }
    
    .badge-override {
        background-color: #fff3e0;
        color: #e65100;
    }
    
    .badge-tinyllama {
        background-color: #e3f2fd;
        color: #01579b;
    }
    
    .badge-mixtral {
        background-color: #fff3e0;
        color: #e65100;
    }
    
    .input-card {
        background: white;
        border: 2px solid var(--border-color);
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    }
    
    .mode-info {
        padding: 1rem;
        background: #f5f5f5;
        border-radius: 6px;
        margin-top: 0.5rem;
        font-size: 0.85rem;
        color: var(--text-light);
    }
    </style>
""", unsafe_allow_html=True)

API_URL = "http://localhost:8000/query"

# Initialize session state
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

# Header
st.markdown("""
    <div class="header-section">
        <h1>🌱 GreenRoute AI</h1>
        <p>Intelligent Query Routing with User Control — AUTO + MANUAL OVERRIDE</p>
    </div>
""", unsafe_allow_html=True)

# Info Section
col_info1, col_info2 = st.columns(2)

with col_info1:
    st.info(
        "**🤖 Automatic Mode (DEFAULT)**\n\n"
        "• System analyzes complexity\n"
        "• Routes intelligently\n"
        "• You just ask!\n\n"
        "✅ Simple query → TinyLlama (fast)\n"
        "✅ Complex query → Mixtral (powerful)"
    )

with col_info2:
    st.info(
        "**🎮 Manual Override (OPTIONAL)**\n\n"
        "• Force specific model\n"
        "• Override auto-routing\n"
        "• For power users!\n\n"
        "⚡ Force SLM: Fast & cheap\n"
        "🧠 Force LLM: Powerful & accurate"
    )

st.divider()

# Main Query Section
st.markdown('<h2 class="section-header">❓ Ask Your Question</h2>', unsafe_allow_html=True)

# Create input with model selector
col_query, col_mode = st.columns([3, 1])

with col_query:
    user_query = st.text_input(
        "Enter your question",
        placeholder="Type your question here...",
        label_visibility="collapsed"
    )

with col_mode:
    mode_option = st.selectbox(
        "Model Mode",
        ["AUTO (Recommended)", "Force LLM", "Force SLM"],
        label_visibility="collapsed"
    )

# Map UI selection to API mode
mode_map = {
    "AUTO (Recommended)": "AUTO",
    "Force LLM": "LLM",
    "Force SLM": "SLM"
}
selected_mode = mode_map[mode_option]

# Show mode explanation
if selected_mode == "AUTO":
    st.markdown(
        """
        <div class="mode-info">
        ✅ <strong>Automatic Mode (Default)</strong><br>
        System will intelligently decide between TinyLlama and Mixtral based on your query complexity.
        </div>
        """,
        unsafe_allow_html=True
    )
elif selected_mode == "LLM":
    st.markdown(
        """
        <div class="mode-info">
        🧠 <strong>Force LLM (Mixtral 8x7B)</strong><br>
        You're forcing the powerful model. Use for complex reasoning, code generation, analysis.
        </div>
        """,
        unsafe_allow_html=True
    )
else:  # SLM
    st.markdown(
        """
        <div class="mode-info">
        ⚡ <strong>Force SLM (TinyLlama 1.1B)</strong><br>
        You're forcing the fast model. Use for simple questions and quick lookups.
        </div>
        """,
        unsafe_allow_html=True
    )

# Submit button
submit_button = st.button("🚀 Send Query", use_container_width=True)

# Process query
if submit_button and user_query:
    try:
        with st.spinner("🔍 Processing your query... (First query may take 30-60 seconds as model loads)"):
            payload = {
                "query": user_query,
                "mode": selected_mode
            }
            response = requests.post(API_URL, json=payload, timeout=180)  # Increased to 3 minutes
            response.raise_for_status()
            result = response.json()
        
        # Update metrics
        st.session_state.total_carbon_saved += result["carbon_saved_g"]
        st.session_state.total_water_saved += result["water_saved_ml"]
        st.session_state.total_emissions_carbon += result["emissions_carbon_g"]
        st.session_state.total_emissions_water += result["emissions_water_ml"]
        
        # Add to history
        st.session_state.query_history.append({
            "query": user_query,
            "mode": result["mode"],
            "model": result["model_used"],
            "reason": result["routing_reason"],
            "complexity_score": result["complexity_score"],
            "carbon_saved": result["carbon_saved_g"],
            "water_saved": result["water_saved_ml"],
            "emissions_carbon": result["emissions_carbon_g"],
            "emissions_water": result["emissions_water_ml"],
            "latency_ms": result["latency_ms"],
            "timestamp": datetime.now()
        })
        
        # Display result
        st.success("✅ Query Processed Successfully!")
        
        # Result breakdown
        result_col1, result_col2, result_col3 = st.columns(3)
        
        with result_col1:
            mode_badge = f'<span class="badge badge-auto" style="background: #d4edda; color: #155724;">🤖 {result["mode"]}</span>' if result["mode"] == "Automatic" else f'<span class="badge badge-override">⚙️ {result["mode"]}</span>'
            st.write("**Routing Mode:**")
            st.markdown(mode_badge, unsafe_allow_html=True)
        
        with result_col2:
            model_badge = f'<span class="badge badge-tinyllama">⚡ TinyLlama</span>' if result["model_used"] == "TinyLlama" else f'<span class="badge badge-mixtral">🧠 Mixtral</span>'
            st.write("**Model Used:**")
            st.markdown(model_badge, unsafe_allow_html=True)
        
        with result_col3:
            st.write("**Complexity:**")
            st.write(f"**{result['complexity_score']}/25**")
        
        st.divider()
        
        # Routing reason
        st.info(f"**Why this model?** {result['routing_reason']}")
        
        st.divider()

        # -------------------- ANSWER DISPLAY (NEW) --------------------

        st.markdown("### 🧠 Answer")

        st.markdown(
            f"""
            <div style="
                background-color: #0f172a;
                color: #ffffff;
                padding: 18px;
                border-radius: 10px;
                font-size: 1.05rem;
                line-height: 1.6;
                border-left: 5px solid #52b788;
            ">
                {result['response']}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.divider()

        # -------------------------------------------------------------
        
        # Impact metrics
        impact_col1, impact_col2, impact_col3 = st.columns(3)
        
        with impact_col1:
            st.write("**⏱️ Performance:**")
            st.write(f"Latency: `{result['latency_ms']:.0f}ms`")
            st.write(f"Tokens: `{result['tokens']['input']} → {result['tokens']['output']}`")
        
        with impact_col2:
            st.write("**💚 Emissions:**")
            st.write(f"CO₂: `{result['emissions_carbon_g']:.4f}g`")
            st.write(f"Water: `{result['emissions_water_ml']:.2f}ml`")
        
        with impact_col3:
            st.write("**✅ Savings:**")
            st.write(f"CO₂ saved: `{result['carbon_saved_g']:.4f}g`")
            st.write(f"Water saved: `{result['water_saved_ml']:.2f}ml`")
        
    except requests.exceptions.Timeout:
        st.error("⏱️ Request timeout. TinyLlama might be loading for the first time (takes 30-60 seconds). Try again!")
    except requests.exceptions.ConnectionError:
        st.error("❌ Backend not running. Start with: `.\\venv\\Scripts\\uvicorn app.main:app --reload`")
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")

st.divider()

# Metrics Dashboard
st.markdown('<h2 class="section-header">📈 Environmental Impact</h2>', unsafe_allow_html=True)

metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

with metric_col1:
    st.markdown(f"""
        <div class="metric-container">
            <div class="metric-label">💚 Carbon Saved</div>
            <div class="metric-value">{st.session_state.total_carbon_saved:.4f}g</div>
        </div>
    """, unsafe_allow_html=True)

with metric_col2:
    st.markdown(f"""
        <div class="metric-container">
            <div class="metric-label">💧 Water Saved</div>
            <div class="metric-value">{st.session_state.total_water_saved:.2f}ml</div>
        </div>
    """, unsafe_allow_html=True)

with metric_col3:
    st.markdown(f"""
        <div class="metric-container">
            <div class="metric-label">⚡ CO₂ Emitted</div>
            <div class="metric-value">{st.session_state.total_emissions_carbon:.4f}g</div>
        </div>
    """, unsafe_allow_html=True)

with metric_col4:
    st.markdown(f"""
        <div class="metric-container">
            <div class="metric-label">🌊 Water Used</div>
            <div class="metric-value">{st.session_state.total_emissions_water:.2f}ml</div>
        </div>
    """, unsafe_allow_html=True)

st.divider()

# Query History
st.markdown('<h2 class="section-header">📋 Query History & Routing Decisions</h2>', unsafe_allow_html=True)

if st.session_state.query_history:
    for i, entry in enumerate(st.session_state.query_history[::-1], 1):
        with st.expander(f"**{i}. {entry['query'][:50]}{'...' if len(entry['query']) > 50 else ''}**"):
            hist_col1, hist_col2, hist_col3, hist_col4 = st.columns(4)
            
            with hist_col1:
                mode_badge = f'<span class="badge badge-auto" style="background: #d4edda; color: #155724;">Auto</span>' if entry["mode"] == "Automatic" else f'<span class="badge badge-override">Override</span>'
                st.write("**Mode:**")
                st.markdown(mode_badge, unsafe_allow_html=True)
            
            with hist_col2:
                model_badge = f'<span class="badge badge-tinyllama">TinyLlama</span>' if entry["model"] == "TinyLlama" else f'<span class="badge badge-mixtral">Mixtral</span>'
                st.write("**Model:**")
                st.markdown(model_badge, unsafe_allow_html=True)
            
            with hist_col3:
                st.write("**Complexity:**")
                st.write(f"{entry['complexity_score']}/25")
            
            with hist_col4:
                st.write("**Time:**")
                st.write(entry['timestamp'].strftime('%H:%M:%S'))
            
            st.divider()
            
            st.write(f"**Routing Reason:** {entry['reason']}")
            
            col_left, col_right = st.columns(2)
            with col_left:
                st.write("**Emissions:**")
                st.write(f"• CO₂: {entry['emissions_carbon']:.4f}g")
                st.write(f"• Water: {entry['emissions_water']:.2f}ml")
                st.write(f"• Latency: {entry['latency_ms']:.0f}ms")
            
            with col_right:
                st.write("**Saved:**")
                st.write(f"• CO₂: {entry['carbon_saved']:.4f}g ✅")
                st.write(f"• Water: {entry['water_saved']:.2f}ml ✅")
else:
    st.info("📝 No queries yet. Ask a question above!")

st.divider()

# Footer
st.markdown("""
    <div style="text-align: center; color: #999; padding: 2rem 0; font-size: 0.9rem;">
        <p><strong>🌱 GreenRoute AI</strong> — Professional Query Routing with User Control</p>
        <p>Automatic Intelligence + Manual Override = Perfect UX</p>
    </div>
""", unsafe_allow_html=True)

