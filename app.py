import streamlit as st
import requests
import google.generativeai as genai
import time
import pandas as pd

# ==========================================
# ⚙️ CONFIG & THEME
# ==========================================
st.set_page_config(page_title="Omni-Gateway", page_icon="⛩️", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;600&display=swap');
    
    .stApp {
        background-color: #050505;
        font-family: 'Space Grotesk', sans-serif;
    }
    
    /* NEON BORDERS */
    .model-card {
        border: 1px solid #333;
        background: #111;
        border-radius: 12px;
        padding: 20px;
        height: 100%;
    }
    .model-card.winner {border-color: #00ff41; box-shadow: 0 0 20px rgba(0, 255, 65, 0.2);}
    
    /* INPUTS */
    .stTextInput input, .stTextArea textarea {
        background: #000 !important; 
        border: 1px solid #333 !important; 
        color: #00ff41 !important;
    }
    
    /* HEADERS */
    h1, h2, h3 {color: #fff !important; text-transform: uppercase; letter-spacing: 2px;}
    
    /* LOGS */
    .log-console {
        font-family: monospace;
        font-size: 12px;
        color: #888;
        background: #000;
        padding: 10px;
        border-top: 1px solid #222;
        height: 150px;
        overflow-y: scroll;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 🔌 GATEWAY ENGINE
# ==========================================

class GatewayEngine:
    def __init__(self):
        self.hf_token = None
        self.gemini_key = None
        
        # THE ARSENAL: Real Open Source Models
        self.models = {
            "Meta: Llama-3-70B": "meta-llama/Meta-Llama-3-70B-Instruct",
            "Mistral: 7B-v0.3": "mistralai/Mistral-7B-Instruct-v0.3",
            "Google: Gemma-7B": "google/gemma-7b-it",
            "Microsoft: Phi-3-Mini": "microsoft/Phi-3-mini-4k-instruct",
            "Nous: Hermes-2-Pro": "NousResearch/Hermes-2-Pro-Llama-3-8B",
            "Qwen: 2-72B": "Qwen/Qwen2-72B-Instruct",
            "TII: Falcon-11B": "tiiuae/falcon-11b",
            "Google: Gemini-1.5-Flash": "gemini-1.5-flash" # Special Route
        }

    def set_keys(self, hf, gemini):
        self.hf_token = hf
        self.gemini_key = gemini

    def query(self, model_name, prompt):
        start = time.time()
        
        # ROUTE 1: GOOGLE GEMINI
        if "Gemini" in model_name:
            if not self.gemini_key: return "⚠️ Error: Missing Gemini Key", 0
            try:
                genai.configure(api_key=self.gemini_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(prompt)
                return response.text, time.time() - start
            except Exception as e:
                return f"Gemini Error: {str(e)}", 0

        # ROUTE 2: HUGGING FACE INFERENCE (The Open Source Army)
        else:
            if not self.hf_token: return "⚠️ Error: Missing HF Token", 0
            api_url = f"https://api-inference.huggingface.co/models/{self.models[model_name]}"
            headers = {"Authorization": f"Bearer {self.hf_token}"}
            
            try:
                response = requests.post(api_url, headers=headers, json={"inputs": prompt, "parameters": {"max_new_tokens": 512}})
                data = response.json()
                
                # Error Handling for loading models
                if isinstance(data, dict) and "error" in data:
                    return f"HF Error: {data['error']} (Model loading... try again in 30s)", 0
                
                # Text Extraction
                if isinstance(data, list) and 'generated_text' in data[0]:
                    # Some models repeat the prompt, we clean it
                    full_text = data[0]['generated_text']
                    return full_text.replace(prompt, "").strip(), time.time() - start
                else:
                    return str(data), 0
            except Exception as e:
                return f"Gateway Error: {str(e)}", 0

engine = GatewayEngine()

# ==========================================
# 🖥️ DASHBOARD
# ==========================================

with st.sidebar:
    st.markdown("### ⛩️ API KEYS")
    hf_key = st.text_input("Hugging Face Token", type="password", help="Get free at huggingface.co/settings/tokens")
    gem_key = st.text_input("Gemini API Key", type="password")
    engine.set_keys(hf_key, gem_key)
    
    st.markdown("---")
    st.markdown("### 📡 MODEL STATUS")
    # Quick visual check of what's available
    st.markdown("🟢 **Gemini Flash**")
    st.markdown("🟢 **Llama-3** (Meta)")
    st.markdown("🟡 **Falcon** (Loading...)")

# HEADER
st.title("⛩️ OMNI-GATEWAY")
st.markdown("Unified Interface for **Meta, Google, Microsoft, Mistral, & Qwen** models.")

# TABS
tab_single, tab_battle = st.tabs(["🚀 SINGLE PROMPT", "⚔️ BATTLE ARENA"])

# --- TAB 1: SINGLE MODEL ---
with tab_single:
    col1, col2 = st.columns([1, 3])
    with col1:
        selected_model = st.selectbox("Select Model", list(engine.models.keys()))
    with col2:
        prompt = st.text_area("Input Prompt", height=100)
    
    if st.button("EXECUTE REQUEST", key="btn1"):
        with st.spinner(f"Routing to {selected_model}..."):
            res, lat = engine.query(selected_model, prompt)
            
        st.markdown(f"""
        <div class="model-card">
            <div style="display:flex; justify-content:space-between; margin-bottom:15px;">
                <span style="color:#00ff41; font-weight:bold;">{selected_model}</span>
                <span style="color:#666;">Latency: {lat:.2f}s</span>
            </div>
            <div style="color:#ddd; line-height:1.6; white-space: pre-wrap;">{res}</div>
        </div>
        """, unsafe_allow_htm
