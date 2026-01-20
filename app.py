import streamlit as st
import feedparser
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

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

    /* GLASS CARDS */
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
    
    .stTextArea textarea {background-color: #111 !important; color: #00ff41 !important; border: 1px solid #333;}
    
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
# 🧠 AGENT LOGIC (Including AI Coder)
# ==========================================

class FounderAgent:
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0'}

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
    
    def generate_code(self, prompt, api_key=None):
        """Queries the Mistral-7B Instruct Model"""
        API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
        
        # Use user key if provided, otherwise empty (might hit rate limits)
        headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
        
        payload = {
            "inputs": f"<s>[INST] You are an expert web developer. Write clean HTML and CSS code for the following request. Do not explain, just write the code.\n\nRequest: {prompt} [/INST]",
            "parameters": {"max_new_tokens": 1000, "temperature": 0.5, "return_full_text": False}
        }
        
        try:
            response = requests.post(API_URL, headers=headers, json=payload)
            return response.json()[0]['generated_text']
        except Exception as e:
            return f"Error: {str(e)}\n\n(Tip: If this failed, the free API is busy. Get a free token at huggingface.co/settings/tokens and paste it above!)"

# ==========================================
# 🖥️ FRONTEND
# ==========================================

agent = FounderAgent()

st.markdown("<h1>⚡ Founder OS <span style='color:#7C3AED; font-size:0.6em; vertical-align:middle;'>v5.0</span></h1>", unsafe_allow_html=True)
st.markdown("---")

# 5 TABS - NOW WITH AI CODER
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🤖 AI CODER", "🧠 AI RADAR", "💸 GRANTS", "🦄 LAUNCHES", "🏷️ DEALS"])

with tab1:
    st.subheader("Generative Code Agent")
    st.caption("Powered by Mistral-7B via Hugging Face API")
    
    with st.expander("⚙️ API Settings (Optional for Speed)"):
        hf_key = st.text_input("Hugging Face Token (Free)", type="password", help="Get one at huggingface.co/settings/tokens to bypass rate limits.")
    
    prompt = st.text_area("Describe what you want (e.g., 'A login form with a glassmorphism effect')", height=100)
    
    if st.button("GENERATE CODE"):
        if prompt:
            with st.spinner("AI is writing your code..."):
                code_result = agent.generate_code(prompt, hf_key)
                st.code(code_result, language='html')
        else:
            st.warning("Please enter a prompt.")

with tab2:
    st.subheader("Trending Models")
    if st.button("REFRESH DATA"): st.rerun()
    models = agent.get_trending_ai()
    cols = st.columns(2)
    for i, m in enumerate(models):
        with cols[i % 2]:
            st.markdown(f"""<div class="glass-card">
                <span class="pro-tag tag-purple">{m['Tag']}</span><br>
                <h3 style="margin-top:5px;">{m['Name']}</h3>
                <p>{m['Stats']}</p>
                <a href="{m['Link']}" target="_blank" style="text-decoration:none; color:#a78bfa; font-weight:bold;">View Model ↗</a>
            </div>""", unsafe_allow_html=True)

with tab3:
    st.subheader("Capital & Credits")
    grants = agent.get_grants()
    cols = st.columns(2)
    for i, g in enumerate(grants):
        with cols[i % 2]:
            st.markdown(f"""<div class="glass-card">
                <span class="pro-tag tag-green">Verified</span>
                <h2 style="color:#34d399 !important; margin:0;">{g['Value']}</h2>
                <h3>{g['Name']}</h3>
                <p>{g['Desc']}</p>
                <a href="{g['Link']}" target="_blank" style="text-decoration:none; color:#34d399; font-weight:bold;">Apply Now ➜</a>
            </div>""", unsafe_allow_html=True)

with tab4:
    # Quick static Product Hunt for speed
    st.subheader("Product Hunt Top Picks")
    st.markdown("""
    <div class="glass-card"><h4>🦄 Devin (AI Engineer)</h4><p>The first fully autonomous AI software engineer.</p></div>
    <div class="glass-card"><h4>⚡ Superlist</h4><p>The new standard for to-do lists.</p></div>
    <div class="glass-card"><h4>🎨 LottieFiles</h4><p>Motion design for developers.</p></div>
    """, unsafe_allow_html=True)

with tab5:
    st.subheader("100% Off Coupons")
    if st.button("FIND DEALS"):
        deals = agent.scrape_coupons()
        for d in deals:
            st.markdown(f"""<div class="glass-card">
                <h4>{d['Title']}</h4>
                <a href="{d['Link']}" target="_blank" style="color:#60a5fa; font-weight:bold;">Claim ➜</a>
            </div>""", unsafe_allow_html=True)
