import streamlit as st
import feedparser
import requests
from bs4 import BeautifulSoup
import pandas as pd
import random

# ==========================================
# 🧠 THE FOUNDER AGENT (Best & Latest)
# ==========================================

class FounderAgent:
    def __init__(self):
        # Stealthe headers to look like a real Chrome user
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

    def get_trending_ai_models(self):
        """Fetches the actual trending models, with hardcoded fallbacks for the best ones."""
        # 1. Try the live API first
        url = "https://huggingface.co/api/trending?limit=10&type=model"
        models = []
        try:
            response = requests.get(url, headers=self.headers, timeout=5)
            if response.status_code == 200:
                data_list = response.json()
                for item in data_list[:10]:
                    repo = item.get('repoData', {})
                    models.append({
                        "Name": repo.get('id', 'Unknown'),
                        "Downloads": f"{repo.get('downloads', 0):,}",
                        "Link": f"https://huggingface.co/{repo.get('id', '')}",
                        "Task": repo.get('pipeline_tag', 'AI Model')
                    })
        except:
            pass

        # 2. If API is empty or fails, ensure we show the KINGS of AI right now
        if not models:
            models = [
                {"Name": "DeepSeek-R1 (The King)", "Downloads": "🔥 Viral", "Link": "https://huggingface.co/deepseek-ai/DeepSeek-R1", "Task": "Reasoning"},
                {"Name": "Llama-3-70B-Instruct", "Downloads": "Top Tier", "Link": "https://huggingface.co/meta-llama/Meta-Llama-3-70B-Instruct", "Task": "Text Gen"},
                {"Name": "Mistral-Large", "Downloads": "New", "Link": "https://huggingface.co/mistralai/Mistral-Large-Instruct-2407", "Task": "Text Gen"},
                {"Name": "Flux.1-Dev", "Downloads": "Best Image", "Link": "https://huggingface.co/black-forest-labs/FLUX.1-dev", "Task": "Image Gen"}
            ]
        return models

    def get_grants(self):
        """The FIXED links that won't give you 'It's not you, it's us' errors."""
        return [
            {
                "Company": "Microsoft for Startups", 
                "Benefit": "$150,000 Azure Credits + Free OpenAI API Access.", 
                # CHANGED: Main landing page (Stable) instead of deep-link (Buggy)
                "Link": "https://www.microsoft.com/en-us/startups" 
            },
            {
                "Company": "AWS Activate", 
                "Benefit": "$1,000 - $100,000 in Credits.", 
                "Link": "https://aws.amazon.com/activate/"
            },
            {
                "Company": "Google for Startups", 
                "Benefit": "$350,000 Cloud Credits (AI First).", 
                "Link": "https://startup.google.com/cloud/"
            },
            {
                "Company": "NVIDIA Inception", 
                "Benefit": "Hardware Discounts & DLI Training.", 
                "Link": "https://www.nvidia.com/en-us/startups/"
            }
        ]

    def scrape_coupons(self):
        """Robust scraper for 100% off coupons."""
        url = "https://www.discudemy.com/all" 
        deals = []
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            items = soup.find_all('section', class_='card')
            for item in items[:15]:
                link = item.find('a', class_='card-header')
                if link:
                    deals.append({
                        "Title": link.get_text(strip=True),
                        "Source": "Discudemy",
                        "Link": link['href'] # User clicks this, then 'Take Course'
                    })
        except:
            pass
        return deals

    def get_product_hunt(self):
        url = "https://www.producthunt.com/feed"
        products = []
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:8]:
                products.append({"Title": entry.title, "Link": entry.link, "Desc": entry.summary[:100]+"..."})
        except:
            pass
        return products

# ==========================================
# 🖥️ THE DASHBOARD (Frontend)
# ==========================================

st.set_page_config(page_title="Founder's Hub Pro", page_icon="🚀", layout="wide")

st.markdown("""
<style>
    .stApp {background-color: #0E1117;}
    .card {background-color: #161b22; padding: 20px; border-radius: 12px; border: 1px solid #30363d; margin-bottom: 15px;}
    .card h3 {color: #fff; margin-top:0;}
    .card p {color: #ccc;}
    .btn {display: inline-block; padding: 8px 16px; background-color: #238636; color: white; border-radius: 6px; text-decoration: none; font-weight: bold;}
    .btn:hover {background-color: #2ea043;}
</style>
""", unsafe_allow_html=True)

st.title("🚀 Founder's Deal Hunter (Stable Edition)")
st.caption("Updated Links: Microsoft, AWS, Hugging Face, Product Hunt")

agent = FounderAgent()

tab1, tab2, tab3, tab4 = st.tabs(["🔥 AI Models", "💸 Startup Grants", "🦄 Product Hunt", "🏷️ Free Coupons"])

with tab1:
    st.header("Trending AI Models")
    if st.button("Refresh Trends"):
        models = agent.get_trending_ai_models()
        for m in models:
            st.markdown(f"""
            <div class="card">
                <h3>{m['Name']}</h3>
                <p>Task: {m['Task']} | ⬇ {m['Downloads']}</p>
                <a href="{m['Link']}" target="_blank" class="btn">View Model ➜</a>
            </div>""", unsafe_allow_html=True)

with tab2:
    st.header("Free Cloud Credits (Corrected Links)")
    grants = agent.get_grants()
    for g in grants:
        st.markdown(f"""
        <div class="card" style="border-left: 5px solid #a371f7;">
            <h3>{g['Company']}</h3>
            <p>{g['Benefit']}</p>
            <a href="{g['Link']}" target="_blank" class="btn">Apply Here ➜</a>
        </div>""", unsafe_allow_html=True)

with tab3:
    st.header("Product Hunt Today")
    if st.button("Scan Products"):
        products = agent.get_product_hunt()
        for p in products:
            st.markdown(f"""
            <div class="card">
                <h3>{p['Title']}</h3>
                <p>{p['Desc']}</p>
                <a href="{p['Link']}" target="_blank" class="btn" style="background-color: #d29922; color: black;">Check it out ➜</a>
            </div>""", unsafe_allow_html=True)

with tab4:
    st.header("100% Off Coupons")
    if st.button("Find Deals"):
        deals = agent.scrape_coupons()
        if deals:
            for d in deals:
                st.markdown(f"""
                <div class="card">
                    <h3>{d['Title']}</h3>
                    <p>Source: {d['Source']}</p>
                    <a href="{d['Link']}" target="_blank" class="btn" style="background-color: #1f6feb;">Get Deal ➜</a>
                </div>""", unsafe_allow_html=True)
        else:
            st.warning("No coupons found right now.")
