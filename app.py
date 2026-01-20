import streamlit as st
import feedparser
import cloudscraper
from bs4 import BeautifulSoup
import pandas as pd
import random
import time
import json

# ==========================================
# 🧠 THE FOUNDER AGENT (Backend Logic)
# ==========================================

class FounderAgent:
    def __init__(self):
        # cloudscraper pretends to be a real browser to bypass Cloudflare
        self.scraper = cloudscraper.create_scraper(
            browser={'browser': 'chrome', 'platform': 'windows', 'mobile': False}
        )

       def get_trending_ai_models(self):
        """Fetches the hottest AI models trending on Hugging Face right now."""
        # OFFICIAL API ENDPOINT (Much more stable)
        url = "https://huggingface.co/api/trending?limit=10&type=model"
        models = []
        try:
            # We use the scraper to be safe, but standard requests would likely work too
            response = self.scraper.get(url).json()
            
            # The official API returns a list, not a dict with 'models' key
            # We iterate through the list directly
            for item in response[:10]:
                # The actual model data is inside 'repoData'
                data = item.get('repoData', {})
                
                models.append({
                    "Name": data.get('id', 'Unknown Model'),
                    "Downloads": f"{data.get('downloads', 0):,}",
                    "Likes": data.get('likes', 0),
                    "Link": f"https://huggingface.co/{data.get('id', '')}",
                    "Task": data.get('pipeline_tag', 'General AI')
                })
        except Exception as e:
            print(f"Hugging Face Error: {e}")
            # FALLBACK: If trending fails, get most downloaded in last 24h
            try:
                fallback_url = "https://huggingface.co/api/models?sort=downloads&direction=-1&limit=10"
                fallback_resp = self.scraper.get(fallback_url).json()
                for data in fallback_resp[:10]:
                    models.append({
                        "Name": data.get('id', 'Unknown Model'),
                        "Downloads": f"{data.get('downloads', 0):,}",
                        "Likes": data.get('likes', 0),
                        "Link": f"https://huggingface.co/{data.get('id', '')}",
                        "Task": data.get('pipeline_tag', 'General AI')
                    })
            except:
                pass
                
        return models


    def get_product_hunt_hot(self):
        """Gets the top products launching TODAY on Product Hunt."""
        url = "https://www.producthunt.com/feed"
        feed = feedparser.parse(url)
        products = []
        for entry in feed.entries[:8]:
            products.append({
                "Title": entry.title,
                "Link": entry.link,
                "Desc": BeautifulSoup(entry.summary, 'html.parser').get_text()[:200] + "..."
            })
        return products

    def scrape_coupons_pro(self):
        """Uses CloudScraper to bypass protection on coupon sites."""
        sources = [
            ("Discudemy", "https://www.discudemy.com/all"),
            ("Real.Discount", "https://www.real.discount/udemy-coupon-code/")
        ]
        
        all_deals = []
        
        for name, url in sources:
            try:
                response = self.scraper.get(url)
                soup = BeautifulSoup(response.text, 'html.parser')
                
                if name == "Discudemy":
                    items = soup.find_all('section', class_='card')
                    for item in items[:8]:
                        title = item.find('a', class_='card-header')
                        if title:
                            all_deals.append({
                                "Title": title.get_text(strip=True),
                                "Source": "Discudemy",
                                "Link": title['href'],
                                "Type": "Education"
                            })
                            
                elif name == "Real.Discount":
                    items = soup.find_all('div', class_='col-sm-12')
                    for item in items[:8]:
                        link_tag = item.find('a', href=True)
                        title_tag = item.find('h3')
                        if link_tag and title_tag:
                            full_link = link_tag['href']
                            if not full_link.startswith('http'):
                                full_link = "https://www.real.discount" + full_link
                                
                            all_deals.append({
                                "Title": title_tag.get_text(strip=True),
                                "Source": "Real.Discount",
                                "Link": full_link,
                                "Type": "Education"
                            })
            except Exception as e:
                print(f"Error scraping {name}: {e}")
                
        return all_deals

    def get_tech_giant_grants(self):
        """The 'Secret' list of massive credits for Startups/Founders."""
        return [
            {
                "Company": "Microsoft for Startups",
                "Benefit": "Up to $150,000 Azure Credits + Free OpenAI API + GitHub Enterprise.",
                "Req": "Open to anyone with an idea (no VC funding needed).",
                "Link": "https://foundershub.startups.microsoft.com/signup"
            },
            {
                "Company": "Google for Startups",
                "Benefit": "Up to $350,000 credits for AI startups (or $2k for general).",
                "Req": "Must have a domain and a working prototype.",
                "Link": "https://startup.google.com/cloud/"
            },
            {
                "Company": "AWS Activate Founders",
                "Benefit": "$1,000 to $100,000 in AWS Credits.",
                "Req": "Self-funded startups get $1k easily. VC-backed get $100k.",
                "Link": "https://aws.amazon.com/activate/founders/"
            },
            {
                "Company": "NVIDIA Inception",
                "Benefit": "Discounts on GPUs, DLI Training, and Cloud Credits.",
                "Req": "Must be an AI/Data Science startup.",
                "Link": "https://www.nvidia.com/en-us/startups/"
            }
        ]

# ==========================================
# 🖥️ THE DASHBOARD (Frontend)
# ==========================================

st.set_page_config(page_title="Founder's Deal Hunter", page_icon="🚀", layout="wide")

# Modern Dark UI
st.markdown("""
<style>
    .stApp {background-color: #0E1117;}
    .big-card {
        background-color: #161b22;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #30363d;
        margin-bottom: 15px;
    }
    .big-card:hover {border-color: #8b949e;}
    .metric-value {font-size: 24px; font-weight: bold; color: #58a6ff;}
    .metric-label {font-size: 14px; color: #8b949e;}
    .tag {
        display: inline-block;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: bold;
        margin-right: 5px;
    }
    .tag-ai {background-color: #1f6feb; color: white;}
    .tag-deal {background-color: #238636; color: white;}
    .tag-hot {background-color: #d29922; color: black;}
    a {text-decoration: none !important;}
</style>
""", unsafe_allow_html=True)

st.title("🚀 Founder's Deal Hunter")
st.caption("Tracking: $500k+ in Grants | Hugging Face Trending | Product Hunt | 100% Off Coupons")

agent = FounderAgent()

# The Tabs
tab_ai, tab_grants, tab_ph, tab_coupons = st.tabs([
    "🔥 Trending AI Models", 
    "💸 Tech Giant Grants", 
    "🦄 Product Hunt Hot", 
    "🏷️ 100% Off Scraper"
])

# --- TAB 1: AI MODELS ---
with tab_ai:
    st.header("What's Blowing Up on Hugging Face?")
    if st.button("Refresh AI Trends"):
        with st.spinner("Fetching data from Hugging Face API..."):
            models = agent.get_trending_ai_models()
            
            # Display in a grid
            cols = st.columns(2)
            for idx, m in enumerate(models):
                with cols[idx % 2]:
                    st.markdown(f"""
                    <div class="big-card">
                        <span class="tag tag-ai">{m['Task']}</span>
                        <h3>{m['Name']}</h3>
                        <p>
                            <span class="metric-value">⬇ {m['Downloads']}</span> <span class="metric-label">downloads</span>
                            &nbsp;&nbsp;|&nbsp;&nbsp;
                            <span class="metric-value">❤ {m['Likes']}</span> <span class="metric-label">likes</span>
                        </p>
                        <a href="{m['Link']}" target="_blank">
                            <button style="background:#1f6feb;color:white;border:none;padding:8px 16px;border-radius:6px;cursor:pointer;width:100%;">
                                View Model ➜
                            </button>
                        </a>
                    </div>
                    """, unsafe_allow_html=True)

# [...](asc_slot://start-slot-1)--- TAB 2: GRANTS ---
with tab_grants:
    st.header("Startup Credits (The Big Money)")
    st.info("💡 Pro Tip: Apply to Microsoft Founders Hub first. They accept almost everyone and give GPT-4 API access.")
    
    grants = agent.get_tech_giant_grants()
    for g in grants:
        st.markdown(f"""
        <div class="big-card" style="border-left: 5px solid #a371f7;">
            <h2>{g['Company']}</h2>
            <p style="font-size:1.1em;">{g['Benefit']}</p>
            <p style="color:#8b949e;"><i>Requirement: {g['Req']}</i></p>
            <a href="{g['Link']}" target="_blank">
                <button style="background:#238636;color:white;border:none;padding:10px 20px;border-radius:6px;cursor:pointer;">
                    Apply Now ➜
                </button>
            </a>
        </div>
        """, unsafe_allow_html=True)

# --- TAB 3: PRODUCT HUNT ---
with tab_ph:
    st.header("Launching Today on Product Hunt")
    if st.button("Scan Product Hunt"):
        with st.spinner("Scanning for unicorns..."):
            products = agent.get_product_hunt_hot()
            for p in products:
                st.markdown(f"""
                <div class="big-card">
                    <span class="tag tag-hot">Today's Launch</span>
                    <h4>{p['Title']}</h4>
                    <p>{p['Desc']}</p>
                    <a href="{p['Link']}" target="_blank">Check it out ➜</a>
                </div>
                """, unsafe_allow_html=True)

# --- TAB 4: COUPONS ---
with tab_coupons:
    st.header("Scrape 100% Off Coupons")
    st.caption("Powered by CloudScraper™ (Bypasses Cloudflare protection)")
    
    if st.button("Run Coupon Scraper Pro"):
        with st.spinner("Hacking the matrix..."):
            deals = agent.scrape_coupons_pro()
            if deals:
                for d in deals:
                    st.markdown(f"""
                    <div class="big-card">
                        <span class="tag tag-deal">{d['Source']}</span>
                        <h4>{d['Title']}</h4>
                        <a href="{d['Link']}" target="_blank" style="color:#58a6ff;font-weight:bold;">GET LINK ➜</a>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.error("Even CloudScraper got blocked! Try again in 5 minutes.")

