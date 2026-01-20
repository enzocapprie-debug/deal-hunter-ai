import streamlit as st
import feedparser
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

# ==========================================
# 🧠 THE BRAIN (Backend Logic)
# ==========================================

class DealHunterAgent:
    def __init__(self):
        # We rotate User-Agents to look less like a robot
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
            'Mozilla/5.0 (Linux; Android 10; SM-A505FN) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Mobile Safari/537.36'
        ]

    def _get_headers(self):
        return {'User-Agent': random.choice(self.user_agents)}

    def get_rss_giveaways(self):
        """Fetches from official RSS feeds (The most stable method)."""
        feeds = [
            ("Giveaway of the Day (Game)", "https://game.giveawayoftheday.com/feed/"),
            ("Giveaway of the Day (Software)", "https://www.giveawayoftheday.com/feed/"),
            ("SharewareOnSale", "http://feeds.feedburner.com/sharewareonsale"),
        ]
        
        deals = []
        for source_name, url in feeds:
            try:
                feed = feedparser.parse(url)
                for entry in feed.entries[:5]: # Top 5 from each
                    deals.append({
                        "Title": entry.title,
                        "Source": source_name,
                        "Link": entry.link,
                        "Description": entry.summary[:150] + "..." if hasattr(entry, 'summary') else "Click to see details.",
                        "Type": "RSS Feed"
                    })
            except Exception as e:
                print(f"Error fetching {source_name}: {e}")
        
        return deals

    def scrape_discudemy(self):
        """Scrapes Discudemy for verified 100% OFF coupons."""
        url = "https://www.discudemy.com/all"
        deals = []
        try:
            response = requests.get(url, headers=self._get_headers(), timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Discudemy structure (this changes rarely)
            items = soup.find_all('section', class_='card')
            
            for item in items[:10]:
                title_tag = item.find('a', class_='card-header')
                if title_tag:
                    # Check if it says 'Free' or '100% off'
                    # Discudemy usually lists valid free ones, but we double check label
                    label = item.find('div', class_='ui label')
                    if label and 'Free' in label.get_text():
                        deals.append({
                            "Title": title_tag.get_text(strip=True),
                            "Source": "Discudemy",
                            "Link": title_tag['href'], # Note: This links to their internal page, user clicks through
                            "Category": "Education"
                        })
        except Exception:
            # Silently fail if site blocks us, so app doesn't crash
            pass
        return deals

    def scrape_real_discount(self):
        """Scrapes Real.Discount for Udemy coupons."""
        url = "https://www.real.discount/udemy-coupon-code/" 
        deals = []
        try:
            response = requests.get(url, headers=self._get_headers(), timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Finding the list items
            items = soup.find_all('div', class_='col-sm-12 col-md-6 col-lg-4')
            
            for item in items[:8]:
                link_tag = item.find('a')
                title_tag = item.find('h3')
                
                if link_tag and title_tag:
                    deals.append({
                        "Title": title_tag.get_text(strip=True),
                        "Source": "Real.Discount",
                        "Link": "https://www.real.discount" + link_tag['href'] if link_tag['href'].startswith('/') else link_tag['href'],
                        "Category": "Education"
                    })
        except Exception:
            pass
        return deals

    def get_student_pack(self):
        return [
            {"Title": "GitHub Student Pack", "Desc": "Access to Canva Pro, Namecheap domains, and Azure credits.", "Link": "https://education.github.com/pack"},
            {"Title": "Notion Education", "Desc": "Unlimited blocks and file uploads for free.", "Link": "https://www.notion.so/product/notion-for-education"},
            {"Title": "JetBrains IDEs", "Desc": "Free PyCharm, IntelliJ, and WebStorm for students.", "Link": "https://www.jetbrains.com/community/education/#students"},
            {"Title": "Amazon Prime Student", "Desc": "6 Months free Prime (Movies, Shipping).", "Link": "https://www.amazon.com/student"}
        ]

# ==========================================
# 🖥️ THE DASHBOARD (Frontend)
# ==========================================

st.set_page_config(page_title="DealHunter Pro", page_icon="⚡", layout="wide")

# Matrix/Cyberpunk Styling
st.markdown("""
<style>
    body {color: #e0e0e0; background-color: #121212;}
    .stButton>button {width: 100%; border-radius: 5px; background: #222; border: 1px solid #333; color: #00ff41; transition: 0.3s;}
    .stButton>button:hover {background: #00ff41; color: black; border-color: #00ff41;}
    .deal-card {
        background: #1e1e1e;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 15px;
        border-left: 4px solid #00ff41;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .deal-card h4 {color: #ffffff; margin-top: 0;}
    .deal-card a {color: #00ff41; text-decoration: none; font-weight: bold; border: 1px solid #00ff41; padding: 5px 10px; border-radius: 4px;}
    .deal-card a:hover {background: #00ff41; color: black;}
    .source-tag {font-size: 0.8em; color: #888; text-transform: uppercase; letter-spacing: 1px;}
</style>
""", unsafe_allow_html=True)

st.title("⚡ DealHunter Pro Agent")
st.caption("Aggregating: GiveawayOfTheDay, SharewareOnSale, Discudemy, Real.Discount & GitHub")

agent = DealHunterAgent()

# Interface Tabs
tab_giveaways, tab_udemy, tab_students = st.tabs(["🎁 Software Giveaways", "📚 Udemy 100% Off", "🎓 Student Loot"])

with tab_giveaways:
    if st.button("🔄 Scan RSS Feeds"):
        with st.spinner("Connecting to global giveaway feeds..."):
            items = agent.get_rss_giveaways()
            if items:
                for i in items:
                    st.markdown(f"""
                    <div class="deal-card">
                        <span class="source-tag">{i['Source']}</span>
                        <h4>{i['Title']}</h4>
                        <p>{i['Description']}</p>
                        <a href="{i['Link']}" target="_blank">GET IT FREE ➜</a>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.error("Connection failed. Check your internet.")

with tab_udemy:
    col1, col2 = st.columns([1,3])
    with col1:
        st.info("⚠️ Note: Some links may require you to click 'Take Course' on the aggregator site first.")
    with col2:
        if st.button("🔎 Hunt for Coupons"):
            with st.spinner("Scraping Discudemy & Real.Discount..."):
                all_coupons = []
                
                # Run Scrapers
                all_coupons.extend(agent.scrape_discudemy())
                time.sleep(1) # Be polite to the server
                all_coupons.extend(agent.scrape_real_discount())
                
                if all_coupons:
                    for c in all_coupons:
                        st.markdown(f"""
                        <div class="deal-card">
                            <span class="source-tag">{c['Source']}</span>
                            <h4>{c['Title']}</h4>
                            <a href="{c['Link']}" target="_blank">ENROLL FREE ➜</a>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.warning("No coupons found. The sites might be protected by Cloudflare at this moment.")

with tab_students:
    st.markdown("### 🎓 Verified Student Packs")
    packs = agent.get_student_pack()
    for p in packs:
        st.markdown(f"""
        <div class="deal-card" style="border-left: 4px solid #ff0055;">
            <h4>{p['Title']}</h4>
            <p>{p['Desc']}</p>
            <a href="{p['Link']}" style="color:#ff0055; border-color:#ff0055;" target="_blank">CLAIM OFFER ➜</a>
        </div>
        """, unsafe_allow_html=True)
