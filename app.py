import streamlit as st
import feedparser
import requests
from bs4 import BeautifulSoup
import pandas as pd

# ==========================================
# 🎨 UI OVERRIDE (Midnight Glass Theme)
# ==========================================
st.set_page_config(page_title="Founder OS", page_icon="⚡", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    /* BACKGROUND */
    .stApp {
        background: radial-gradient(circle at 50% 10%, #1a1c2e 0%, #000000 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* HIDE STREAMLIT UI */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* WORKSTATION CONTAINER (The Top Part) */
    .workstation {
        background: rgba(0, 0, 0, 0.4);
        border: 1px solid #333;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 30px;
        box-shadow: 0 0 50px rgba(124, 58, 237, 0.1);
    }

    /* GLASS CARDS (The Bottom Part) */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 15px;
    }
    .glass-card:hover {border-color: rgba(255, 255, 255, 0.3); transform: translateY(-2px); transition: all 0.2s;}

    /* TEXT & BUTTONS */
    h1, h2, h3, h4 {color: #fff !important; font-weight: 800 !important; letter-spacing: -0.5px;}
    p, span, div, label {color: #a0a0b0 !important;}
    
    .stTextArea textarea {background-color: #0d0d0d !important; color: #00ff41 !important; border: 1px solid #333;}
    
    .stButton>button {
        background: linear-gradient(90deg, #4F46E5 0%, #7C3AED 100%);
        color: white !important;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        width: 100%;
    }
    
    /* TAGS */
    .pro-tag {display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 11px; font-weight: 800; text-transform: uppercase;}
    .tag-purple {background: rgba(139, 92, 246, 0.2); color: #a78bfa !important;}
    .tag-green {background: rgba(16, 185, 129, 0.2); color: #34d399 !important;}
    
    .block-container {padding-top: 2rem; padding-bottom: 5rem;}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 🧠 AGENT LOGIC
# ==========================================

class FounderAgent:
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0'}

    def generate_code(self, prompt, api_key=None):
        API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
        headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
        payload = {
            "inputs": f"<s>[INST] You are an expert web developer. Write clean HTML and CSS code for the following request. Do not explain, just write the code.\n\nRequest: {prompt} [/INST]",
            "parameters": {"max_new_tokens": 1000, "temperature": 0.5, "return_full_text": False}
        }
        try:
            response = requests.post(API_URL, headers=headers, json=payload)
            return response.json()[0]['generated_text']
        except:
            return "Error: API Busy. Use a free Hugging Face token in settings to fix this."

    def get_trending_ai(self):
        url = "https://huggingface.co/api/trending?limit=10&type=model"
        models = []
        try:
            resp = requests.get(url, headers=self.headers, timeout=5).json()
            for item in resp:
                repo = item.get('repoData', {})
                models.append({
                    "Name": repo.get('id', 'Unknown'),
                    "Stats": f"⬇ {repo.get('downloads', 0):,}",
                    "Link": f"https://huggingface.co/{repo.get('id', '')}",
                    "Tag": repo.get('pipeline_tag', 'AI')
                })
        except: pass
        if not models:
            models = [
                {"Name": "DeepSeek-R1", "Stats": "🔥 VIRAL", "Link": "https://huggingface.co/deepseek-ai/DeepSeek-R1", "Tag": "REASONING"},
                {"Name": "Llama-3-70B", "Stats": "👑 META", "Link": "https://huggingface.co/meta-llama/Meta-Llama-3-70B", "Tag": "TEXT GEN"}
            ]
        return models

    def get_grants(self):
        return [
            {"Name": "Microsoft Founders", "Value": "$150,000", "Desc": "Azure + OpenAI Keys", "Link": "https://www.microsoft.com/en-us/startups"},
            {"Name": "Google Cloud", "Value": "$350,000", "Desc": "AI Compute Credits", "Link": "https://startup.google.com/cloud/"},
            {"Name": "AWS Activate", "Value": "$100,000", "Desc": "Server Credits", "Link": "https://aws.amazon.com/activate/"},
            {"Name": "NVIDIA Inception", "Value": "HARDWARE", "Desc": "GPU Access", "Link": "https://www.nvidia.com/en-us/startups/"}
        ]

    def scrape_coupons(self):
        deals = []
        try:
            resp = requests.get("https://www.discudemy.com/all", headers=self.headers, timeout=8)
            soup = BeautifulSoup(resp.text, 'html.parser')
            items = soup.find_all('section', class_='card')
            for item in items[:12]:
                link = item.find('a', class_='card-header')
                if link: deals.append({"Title": link.get_text(strip=True), "Link": link['href']})
        except: pass
        return deals

# ==========================================
# 🖥️ FRONTEND
# ==========================================

agent = FounderAgent()

st.markdown("<h1>⚡ Founder OS <span style='color:#7C3AED; font-size:0.6em; vertical-align:middle;'>v5.1</span></h1>", unsafe_allow_html=True)

# ----------------------------------
# 1. AI WORKSTATION (Standalone)
# ----------------------------------
st.markdown("### 🤖 AI Coder Workstation")
st.markdown('<div class="workstation">', unsafe_allow_html=True)

col_input, col_settings = st.columns([3, 1])
with col_input:
    prompt = st.text_area("What do you want to build?", height=100, placeholder="e.g. A responsive pricing table with 3 tiers and hover effects...")
with col_settings:
    st.markdown("##### ⚙️ Engine")
    hf_key = st.text_input("HF Token (Optional)", type="password")
    if st.button("GENERATE CODE ⚡"):
        if prompt:
            with st.spinner("Coding..."):
                code = agent.generate_code(prompt, hf_key)
                st.code(code, language='html')
        else:
            st.warning("Enter a prompt first.")

st.markdown('</div>', unsafe_allow_html=True)
st.markdown("---")


# ----------------------------------
# 2. INTELLIGENCE HUB (Tabs)
# ----------------------------------
st.markdown("### 📡 Intelligence Hub")
tab1, tab2, tab3, tab4 = st.tabs(["🧠 AI RADAR", "💸 GRANTS", "🦄 LAUNCHES", "🏷️ DEALS"])

with tab1:
    if st.button("REFRESH RADAR"): st.rerun()
    models = agent.get_trending_ai()
    cols = st.columns(2)
    for i, m in enumerate(models):
        with cols[i % 2]:
            st.markdown(f"""<div class="glass-card">
                <span class="pro-tag tag-purple">{m['Tag']}</span>
                <h3>{m['Name']}</h3>
                <p>{m['Stats']}</p>
                <a href="{m['Link']}" target="_blank" style="color:#a78bfa; font-weight:bold;">View Model ↗</a>
            </div>""", unsafe_allow_html=True)

with tab2:
    grants = agent.get_grants()
    cols = st.columns(2)
    for i, g in enumerate(grants):
        with cols[i % 2]:
            st.markdown(f"""<div class="glass-card">
                <span class="pro-tag tag-green">Verified</span>
                <h2 style="color:#34d399 !important; margin:0;">{g['Value']}</h2>
                <h3>{g['Name']}</h3>
                <a href="{g['Link']}" target="_blank" style="color:#34d399; font-weight:bold;">Apply Now ➜</a>
            </div>""", unsafe_allow_html=True)

with tab3:
    st.markdown("""
    <div class="glass-card"><h4>🦄 Devin (AI Engineer)</h4><p>The first fully autonomous AI software engineer.</p></div>
    <div class="glass-card"><h4>⚡ Superlist</h4><p>The new standard for to-do lists.</p></div>
    """, unsafe_allow_html=True)

with tab4:
    if st.button("FIND DEALS"):
        deals = agent.scrape_coupons()
        for d in deals:
            st.markdown(f"""<div class="glass-card">
                <h4>{d['Title']}</h4>
                <a href="{d['Link']}" target="_blank" style="color:#60a5fa; font-weight:bold;">Claim ➜</a>
            </div>""", unsafe_allow_html=True)
