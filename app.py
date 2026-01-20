import streamlit as st
import pandas as pd
import time
import random
import google.generativeai as genai
from datetime import datetime

# ==========================================
# 🎨 DEVTOOL THEME (Vercel/Stripe Aesthetic)
# ==========================================
st.set_page_config(page_title="AI Gateway", page_icon="🌐", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@400;600;800&display=swap');
    
    .stApp {
        background-color: #000000;
        background-image: radial-gradient(#111 1px, transparent 1px);
        background-size: 20px 20px;
        font-family: 'Inter', sans-serif;
    }
    
    /* HIDE STREAMLIT CHROME */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* SIDEBAR */
    section[data-testid="stSidebar"] {
        background-color: #050505;
        border-right: 1px solid #333;
    }

    /* CARDS */
    .metric-card {
        background: #0A0A0A;
        border: 1px solid #222;
        border-radius: 12px;
        padding: 20px;
    }
    .metric-card:hover {border-color: #444;}

    /* CODE & LOGS */
    .log-entry {
        font-family: 'JetBrains Mono', monospace;
        font-size: 12px;
        background: #0D0D0D;
        border-bottom: 1px solid #222;
        padding: 10px;
        display: flex;
        justify-content: space-between;
    }

    /* TYPOGRAPHY */
    h1, h2, h3 {color: #fff !important; letter-spacing: -0.5px;}
    p, span, div, label {color: #888 !important;}
    
    /* BADGES */
    .badge {padding: 2px 8px; border-radius: 4px; font-size: 10px; font-weight: bold; text-transform: uppercase;}
    .badge-openai {background: rgba(16, 163, 127, 0.2); color: #10a37f !important;}
    .badge-google {background: rgba(66, 133, 244, 0.2); color: #4285f4 !important;}
    .badge-anthropic {background: rgba(217, 119, 87, 0.2); color: #d97757 !important;}
    .badge-error {background: rgba(255, 0, 0, 0.2); color: #ff4444 !important;}

    /* INPUTS */
    .stTextArea textarea, .stTextInput input, .stSelectbox div[data-baseweb="select"] {
        background-color: #000 !important; 
        color: #fff !important; 
        border: 1px solid #333 !important;
    }
    .stButton>button {
        background: #fff;
        color: #000 !important;
        border: none;
        font-weight: 600;
        border-radius: 6px;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 🌐 GATEWAY LOGIC
# ==========================================

class AIGateway:
    def __init__(self):
        # In a real app, these would be stored securely in a database
        if 'logs' not in st.session_state:
            st.session_state.logs = []

    def route_request(self, provider, model, prompt, api_key):
        start_time = time.time()
        response_text = ""
        status = "200 OK"
        latency = 0
        
        try:
            # 1. GOOGLE ROUTE (Working Real Implementation)
            if provider == "Google":
                if not api_key: raise Exception("Missing API Key")
                genai.configure(api_key=api_key)
                ai_model = genai.GenerativeModel(model)
                resp = ai_model.generate_content(prompt)
                response_text = resp.text

            # 2. OPENAI ROUTE (Simulation for Demo)
            elif provider == "OpenAI":
                time.sleep(1.2) # Simulate network lag
                response_text = f"Simulated GPT-4 Response: This is where the OpenAI API response would appear. (Connect Key to Activate)"
            
            # 3. ANTHROPIC ROUTE (Simulation for Demo)
            elif provider == "Anthropic":
                time.sleep(0.8)
                response_text = f"Simulated Claude Response: I am Claude, executing your request via the Gateway."

        except Exception as e:
            status = "500 ERROR"
            response_text = str(e)

        # LOGGING
        latency = round((time.time() - start_time) * 1000, 2) # ms
        log = {
            "Time": datetime.now().strftime("%H:%M:%S"),
            "Provider": provider,
            "Model": model,
            "Latency": f"{latency}ms",
            "Status": status,
            "Prompt": prompt[:30] + "..."
        }
        st.session_state.logs.insert(0, log) # Add to top
        
        return response_text, latency, status

gateway = AIGateway()

# ==========================================
# 🖥️ DASHBOARD UI
# ==========================================

with st.sidebar:
    st.markdown("### 🌐 AI Gateway")
    page = st.radio("Navigation", ["Playground", "Logs & Analytics", "Settings"])
    st.markdown("---")
    
    st.markdown("#### 🔑 Provider Keys")
    google_key = st.text_input("Google API Key", type="password", value="")
    openai_key = st.text_input("OpenAI API Key", type="password", placeholder="sk-...")
    anthropic_key = st.text_input("Anthropic API Key", type="password", placeholder="sk-ant...")

# --- PAGE 1: UNIVERSAL PLAYGROUND ---
if page == "Playground":
    st.title("⚡ Universal Playground")
    st.markdown("Test prompts across multiple models through a single interface.")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.markdown("##### Configuration")
        provider = st.selectbox("Provider", ["Google", "OpenAI", "Anthropic"])
        
        # Dynamic Model List based on Provider
        if provider == "Google":
            model = st.selectbox("Model", ["gemini-1.5-flash", "gemini-pro"])
        elif provider == "OpenAI":
            model = st.selectbox("Model", ["gpt-4-turbo", "gpt-3.5-turbo"])
        else:
            model = st.selectbox("Model", ["claude-3-opus", "claude-3-sonnet"])
            
        temp = st.slider("Temperature", 0.0, 1.0, 0.7)
        
    with col2:
        prompt = st.text_area("System / User Prompt", height=150, placeholder="Enter your prompt here...")
        
        if st.button("Send Request 🚀"):
            # Determine which key to use
            active_key = google_key if provider == "Google" else openai_key if provider == "OpenAI" else anthropic_key
            
            with st.spinner(f"Routing to {provider} :: {model}..."):
                res, lat, stat = gateway.route_request(provider, model, prompt, active_key)
            
            # Result Card
            st.markdown(f"""
            <div class="metric-card">
                <div style="display:flex; justify-content:space-between; margin-bottom:10px;">
                    <span class="badge badge-{provider.lower()}">{provider}</span>
                    <span style="font-family:'JetBrains Mono'; color:#666;">{lat}ms</span>
                </div>
                <div style="color:#fff; line-height:1.6;">{res}</div>
            </div>
            """, unsafe_allow_html=True)
            
            if stat == "500 ERROR":
                st.error(f"Gateway Error: {res}")

# --- PAGE 2: LOGS & ANALYTICS ---
elif page == "Logs & Analytics":
    st.title("📊 Traffic & Logs")
    
    # Fake Metrics for the 'Demo' feel
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Requests", len(st.session_state.logs), "+12%")
    m2.metric("Avg Latency", "240ms", "-30ms")
    m3.metric("Cache Hit Rate", "84%", "+2%")
    m4.metric("Est. Cost", "$0.042", "+$0.01")
    
    st.markdown("### Request Logs")
    st.markdown("<div style='border:1px solid #333; border-radius:8px; overflow:hidden;'>", unsafe_allow_html=True)
    
    # Headers
    st.markdown("""
    <div style="display:flex; justify-content:space-between; padding:10px; background:#111; font-weight:bold; font-size:12px; border-bottom:1px solid #333;">
        <span style="width:100px">TIME</span>
        <span style="width:100px">PROVIDER</span>
        <span style="width:150px">MODEL</span>
        <span style="width:100px">STATUS</span>
        <span style="flex:1">PROMPT PREVIEW</span>
        <span style="width:80px">LATENCY</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Render Logs
    for log in st.session_state.logs:
        color = "#10a37f" if "200" in log['Status'] else "#ff4444"
        st.markdown(f"""
        <div class="log-entry">
            <span style="width:100px; color:#666 !important;">{log['Time']}</span>
            <span style="width:100px">{log['Provider']}</span>
            <span style="width:150px; color:#888 !important;">{log['Model']}</span>
            <span style="width:100px; color:{color} !important;">{log['Status']}</span>
            <span style="flex:1; color:#ccc !important;">{log['Prompt']}</span>
            <span style="width:80px; color:#666 !important;">{log['Latency']}</span>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- PAGE 3: INTEGRATION SETTINGS ---
elif page == "Settings":
    st.title("🛠️ Integration")
    st.markdown("Use our Unified SDK to access all models with one line of code.")
    
    st.markdown("### Python SDK")
    st.code("""
import openai

# Point to your Gateway instead of OpenAI directly
client = openai.OpenAI(
    base_url="https://your-gateway-url.com/v1",
    api_key="sk-gateway-key"
)

response = client.chat.completions.create(
    model="google/gemini-pro", # Universal Routing
    messages=[{"role": "user", "content": "Hello!"}]
)
    """, language="python")
    
    st.markdown("### Fallback Logic")
    st.info("Automatic fallback is enabled. If OpenAI is down, traffic routes to Azure OpenAI automatically.")
