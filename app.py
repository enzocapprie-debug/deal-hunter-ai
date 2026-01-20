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

    /* BACKGROUND & FONT */
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
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        border-color: rgba(255, 255, 255, 0.3);
    }

    /* TYPOGRAPHY */
    h1, h2, h3, h4 {color: #fff !important; font-weight: 800 !important; letter-spacing: -0.5px;}
    p, span, div {color: #a0a0b0;}

    /* BUTTONS */
    .stButton>button {
        background: linear-gradient(90deg, #4F46E5 0%, #7C3AED 100%);
        color: white !important;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        width: 100%;
    }
    
    /* TAGS */
    .pro-tag {
        display: inline-block; padding: 4px 12px; border-radius: 20px;
        font-size: 11px; font-weight: 800; text-transform: uppercase; letter-spacing: 1px;
    }
    .tag-blue {background: rgba(59, 130, 246, 0.2); color: #60a5fa;}
    .tag-purple {background: rgba(139, 92, 246, 0.2); color: #a78bfa;}
    .tag-green {background: rgba(16, 185, 129, 0.2); color: #34d399;}
    .tag-orange {background: rgba(245, 158, 11, 0.2); color: #fbbf24;}
    
    /* SPACING */
    .block-container {padding-top: 2rem; padding-bottom: 5rem;}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 🧠 AGENT LOGIC
# ==========================================

class FounderAgent:
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36'}

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
                {"Name": "Llama-3-70B", "Stats": "👑 META", "Link": "https://huggingface.co/meta-llama/Meta-Llama-3-70B", "Tag": "TEXT GEN"},
                {"Name": "Flux.1-Dev", "Stats": "🎨 SOTA", "Link": "https://huggingface.co/black-forest-labs/FLUX.1-dev", "Tag": "IMAGE"}
            ]
        return models

    def get_grants(self):
        return [
            {"Name": "Microsoft Founders", "Value": "$150,000", "Desc": "Azure + OpenAI Keys", "Link": "https://www.microsoft.com/en-us/startups", "Tag": "TOP PICK"},
            {"Name": "Google Cloud", "Value": "$350,000", "Desc": "AI Compute Credits", "Link": "https://startup.google.com/cloud/", "Tag": "HIGH VALUE"},
            {"Name": "AWS Activate", "Value": "$100,000", "Desc": "Server Credits", "Link": "https://aws.amazon.com/activate/", "Tag": "STANDARD"},
            {"Name": "NVIDIA Inception", "Value": "HARDWARE", "Desc": "GPU Access", "Link": "https://www.nvidia.com/en-us/startups/", "Tag": "HARDWARE"}
        ]

    def get_crypto_loot(self):
        return [
            {"Name": "Binance Labs", "Type": "INVESTMENT", "Link": "https://labs.binance.com/", "Tag": "VC FUND"},
            {"Name": "Solana Foundation", "Type": "GRANTS", "Link": "https://solana.org/grants", "Tag": "L1 CHAIN"},
            {"Name": "Ethereum ESP", "Type": "FUNDING", "Link": "https://esp.ethereum.foundation/applicants", "Tag": "ECOSYSTEM"},
            {"Name": "Web3 Grants Info", "Type": "DATABASE", "Link": "https://www.web3grants.info/", "Tag": "AGGREGATOR"}
        ]

    def scrape_coupons(self):
        url = "https://www.discudemy.com/all"
        deals = []
        try:
            resp = requests.get(url, headers=self.headers, timeout=8)
            soup = BeautifulSoup(resp.text, 'html.parser')
            items = soup.find_all('section', class_='card')
            for item in items[:12]:
                link = item.find('a', class_='card-header')
                if link: deals.append({"Title": link.get_text(strip=True), "Link": link['href']})
        except: pass
        return deals

    def get_product_hunt(self):
        try:
            feed = feedparser.parse("https://www.producthunt.com/feed")
            return [{"Title": x.title, "Link": x.link} for x in feed.entries[:10]]
        except: return []

# ==========================================
# 🖥️ FRONTEND
# ==========================================

agent = FounderAgent()

st.markdown("<h1>⚡ Founder OS <span style='color:#7C3AED; font-size:0.6em; vertical-align:middle;'>v4.1</span></h1>", unsafe_allow_html=True)
st.markdown("<p style='font-size: 1.1em; opacity: 0.8;'>Command Center: AI, Web3, Grants & Deals</p>", unsafe_allow_html=True)
st.markdown("---")

# 5 TABS - RESTORED & COMPLETE
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🧠 AI RADAR", "💸 GRANTS", "🪙 CRYPTO", "🦄 LAUNCHES", "🏷️ DEALS"])

with tab1:
    col1, col2 = st.columns([3, 1])
    with col1: st.subheader("Trending Models")
    with col2: 
        if st.button("REFRESH DATA"): st.rerun()
    models = agent.get_trending_ai()
    cols = st.columns(2)
    for i, m in enumerate(models):
        with cols[i % 2]:
            st.markdown(f"""
            <div class="glass-card">
                <div style="display:flex; justify-content:space-between; margin-bottom:10px;">
                    <span class="pro-tag tag-purple">{m['Tag']}</span>
                    <span style="font-size:0.8em; opacity:0.6;">{m['Stats']}</span>
                </div>
                <h3 style="font-size:1.2em; margin:0 0 10px 0;">{m['Name']}</h3>
                <a href="{m['Link']}" target="_blank" style="text-decoration:none;">
                    <div style="background:rgba(255,255,255,0.1); text-align:center; padding:8px; border-radius:6px; color:white; font-size:0.9em; font-weight:600;">View Model ↗</div>
                </a>
            </div>""", unsafe_allow_html=True)

with tab2:
    st.subheader("Capital & Credits")
    grants = agent.get_grants()
    cols = st.columns(2)
    for i, g in enumerate(grants):
        with cols[i % 2]:
            st.markdown(f"""
            <div class="glass-card">
                <div style="margin-bottom:10px;"><span class="pro-tag tag-green">{g['Tag']}</span></div>
                <h2 style="color:#34d399 !important; font-size:1.8em; margin:0;">{g['Value']}</h2>
                <h3 style="font-size:1.1em; margin-top:5px;">{g['Name']}</h3>
                <p style="font-size:0.9em;">{g['Desc']}</p>
                <a href="{g['Link']}" target="_blank" style="text-decoration:none;">
                    <div style="background:linear-gradient(90deg, #059669, #10B981); text-align:center; padding:10px; border-radius:6px; color:white; font-weight:bold;">Apply Now ➜</div>
                </a>
            </div>""", unsafe_allow_html=True)

with tab3:
    st.subheader("Web3 & Crypto Opportunities")
    loot = agent.get_crypto_loot()
    cols = st.columns(2)
    for i, l in enumerate(loot):
        with cols[i % 2]:
            st.markdown(f"""
            <div class="glass-card">
                <div style="margin-bottom:10px;"><span class="pro-tag tag-orange">{l['Tag']}</span></div>
                <h3 style="font-size:1.3em; margin:0 0 5px 0;">{l['Name']}</h3>
                <p style="font-size:0.9em; margin-bottom:15px;">Focus: {l['Type']}</p>
                <a href="{l['Link']}" target="_blank" style="text-decoration:none;">
                    <div style="border:1px solid #fbbf24; text-align:center; padding:8px; border-radius:6px; color:#fbbf24; font-weight:bold;">Access Portal ➜</div>
                </a>
            </div>""", unsafe_allow_html=True)

with tab4:
    st.subheader("Product Hunt Live")
    if st.button("SCAN FEED"):
        products = agent.get_product_hunt()
        for p in products:
            st.markdown(f"""
            <div class="glass-card" style="padding:15px; display:flex; justify-content:space-between; align-items:center;">
                <div style="font-weight:600; font-size:1.1em; color:#fff;">{p['Title']}</div>
                <a href="{p['Link']}" target="_blank" style="color:#7C3AED; text-decoration:none; font-weight:bold;">Check it out ➜</a>
            </div>""", unsafe_allow_html=True)

with tab5:
    st.subheader("100% Off Coupons")
    if st.button("FIND DEALS"):
        deals = agent.scrape_coupons()
        if deals:
            for d in deals:
                st.markdown(f"""
                <div class="glass-card">
                    <h4 style="color:#fff; margin:0 0 10px 0;">{d['Title']}</h4>
                    <a href="{d['Link']}" target="_blank" style="text-decoration:none; color:#60a5fa; font-weight:bold; font-size:0.9em;">CLAIM OFFER ➜</a>
                </div>""", unsafe_allow_html=True)
        else:
            st.info("No coupons found. Try again later.")
