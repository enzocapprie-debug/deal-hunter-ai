import streamlit as st
import feedparser
import requests
from bs4 import BeautifulSoup
import pandas as pd
import random

# ==========================================
# 🎨 UI & THEME ENGINE
# ==========================================
st.set_page_config(page_title="Founder OS v6", page_icon="⚡", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    /* GLOBAL THEME */
    .stApp {
        background: radial-gradient(circle at 50% 0%, #1e1e2e 0%, #000000 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* HIDE STREAMLIT CHROME */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* SIDEBAR STYLE */
    section[data-testid="stSidebar"] {
        background-color: #050505;
        border-right: 1px solid #222;
    }

    /* GLASS CARDS */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
    }
    .glass-card:hover {
        border-color: rgba(255, 255, 255, 0.2);
        box-shadow: 0 10px 40px rgba(0,0,0,0.5);
        transform: translateY(-3px);
        transition: all 0.3s ease;
    }

    /* TYPOGRAPHY */
    h1, h2, h3 {color: white !important; font-weight: 800 !important; letter-spacing: -0.5px;}
    p, span, div, label {color: #94a3b8 !important;}
    
    /* INPUTS */
    .stTextArea textarea, .stTextInput input {
        background-color: #0F0F12 !important; 
        color: #e2e8f0 !important; 
        border: 1px solid #333 !important;
        border-radius: 8px;
    }
    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: #7C3AED !important;
        box-shadow: 0 0 0 1px #7C3AED !important;
    }

    /* BUTTONS */
    .stButton>button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white !important;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        padding: 0.6rem 1rem;
        transition: all 0.2s;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 5px 20px rgba(139, 92, 246, 0.4);
    }

    /* TAGS */
    .tag {
        display: inline-block; padding: 4px 10px; border-radius: 6px; 
        font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;
    }
    .tag-purple {background: rgba(139, 92, 246, 0.15); color: #a78bfa !important;}
    .tag-green {background: rgba(16, 185, 129, 0.15); color: #34d399 !important;}
    .tag-orange {background: rgba(245, 158, 11, 0.15); color: #fbbf24 !important;}
    .tag-blue {background: rgba(59, 130, 246, 0.15); color: #60a5fa !important;}

</style>
""", unsafe_allow_html=True)

# ==========================================
# 🧠 BACKEND LOGIC
# ==========================================

class FounderEngine:
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0'}

    # --- AI STUDIO FUNCTIONS ---
    def generate_code(self, prompt, stack, mode, hf_key=None):
        API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
        headers = {"Authorization": f"Bearer {hf_key}"} if hf_key else {}
        
        system_prompt = f"You are an expert {stack} developer."
        if mode == "Debugger":
            full_prompt = f"<s>[INST] {system_prompt} Fix the following broken code and explain the error:\n\n{prompt} [/INST]"
        else:
            full_prompt = f"<s>[INST] {system_prompt} Write production-ready code for: {prompt}. Provide ONLY the code. [/INST]"
            
        payload = {"inputs": full_prompt, "parameters": {"max_new_tokens": 1500, "temperature": 0.4}}
        
        try:
            response = requests.post(API_URL, headers=headers, json=payload)
            return response.json()[0]['generated_text']
        except:
            return "⚠️ Error: API Busy. Please use a free Hugging Face Token in the settings sidebar."

    def get_ui_blueprint(self, component):
        # Instant cache for common components
        blueprints = {
            "Landing Page": "<!-- HTML Structure -->\n<nav class='flex justify-between p-6'>...</nav>\n<section class='hero h-screen'>...</section>",
            "Login Form": "<form class='glass-panel p-8'>\n  <input type='email' placeholder='Email' />\n  <button>Login</button>\n</form>",
            "Dashboard Shell": "<div class='grid grid-cols-12 h-screen'>\n  <aside class='col-span-2 bg-black'>Sidebar</aside>\n  <main class='col-span-10'>Content</main>\n</div>"
        }
        return blueprints.get(component, "No blueprint found.")

    # --- DEAL HUNTER FUNCTIONS ---
    def get_assets(self, query=""):
        # Simulated data for stability (Replace with scraper in prod)
        assets = [
            {"Name": "DeepSeek-R1", "Type": "AI Model", "Source": "HuggingFace", "Link": "https://huggingface.co/deepseek-ai/DeepSeek-R1", "Tag": "Trending"},
            {"Name": "Microsoft Founders", "Type": "Grant", "Source": "Microsoft", "Link": "https://www.microsoft.com/en-us/startups", "Tag": "$150k"},
            {"Name": "Google Cloud", "Type": "Grant", "Source": "Google", "Link": "https://startup.google.com/cloud/", "Tag": "$350k"},
            {"Name": "Solana Foundation", "Type": "Crypto", "Source": "Solana", "Link": "https://solana.org/grants", "Tag": "Web3"},
            {"Name": "AWS Activate", "Type": "Grant", "Source": "Amazon", "Link": "https://aws.amazon.com/activate/", "Tag": "$100k"},
            {"Name": "ETHGlobal", "Type": "Hackathon", "Source": "Ethereum", "Link": "https://ethglobal.com/", "Tag": "Prizes"},
            {"Name": "Udemy 100% Off", "Type": "Coupon", "Source": "Discudemy", "Link": "https://www.discudemy.com/all", "Tag": "Free"}
        ]
        
        if query:
            return [a for a in assets if query.lower() in a['Name'].lower() or query.lower() in a['Type'].lower()]
        return assets

    def scrape_live_coupons(self):
        deals = []
        try:
            resp = requests.get("https://www.discudemy.com/all", headers=self.headers, timeout=5)
            soup = BeautifulSoup(resp.text, 'html.parser')
            for item in soup.find_all('section', class_='card')[:15]:
                link = item.find('a', class_='card-header')
                if link: deals.append({"Title": link.get_text(strip=True), "Link": link['href']})
        except: pass
        return deals

engine = FounderEngine()

# ==========================================
# 🖥️ SIDEBAR NAVIGATION
# ==========================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/11529/11529610.png", width=50)
    st.markdown("### Founder OS <span style='font-size:0.8em; color:#7C3AED'>v6.0</span>", unsafe_allow_html=True)
    st.markdown("---")
    
    app_mode = st.radio("SELECT MODULE", ["💻 AI Studio", "🕵️ Deal Hunter"])
    
    st.markdown("---")
    st.markdown("##### ⚙️ Settings")
    hf_key = st.text_input("HF API Token", type="password", help="Paste Hugging Face Token here for speed.")

# ==========================================
# 🚀 APP 1: AI STUDIO
# ==========================================
if app_mode == "💻 AI Studio":
    st.markdown("<h1>💻 AI Code Studio</h1>", unsafe_allow_html=True)
    st.markdown("<p>Generative Development Environment</p>", unsafe_allow_html=True)
    
    # CONTROLS
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        mode = st.selectbox("Mode", ["Generator", "Debugger", "UI Library"])
    with col2:
        stack = st.selectbox("Tech Stack", ["HTML/Tailwind", "React/Next.js", "Python/Streamlit"])
    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        # Placeholder for future metrics
    
    # MAIN WORKSPACE
    if mode == "UI Library":
        st.markdown("### 📦 Instant Components")
        st.caption("One-click code blueprints.")
        
        c1, c2, c3 = st.columns(3)
        if c1.button("Landing Page"):
            st.code(engine.get_ui_blueprint("Landing Page"), language="html")
        if c2.button("Login Form"):
            st.code(engine.get_ui_blueprint("Login Form"), language="html")
        if c3.button("Dashboard Shell"):
            st.code(engine.get_ui_blueprint("Dashboard Shell"), language="html")
            
    else:
        # Generator & Debugger
        st.markdown(f"### ⚡ {mode}")
        prompt_input = st.text_area("Input Command / Code", height=150, placeholder="Describe the feature or paste broken code here...")
        
        if st.button("RUN AGENT ⚡"):
            if prompt_input:
                with st.spinner("Compiling..."):
                    result = engine.generate_code(prompt_input, stack, mode, hf_key)
                    st.code(result)
            else:
                st.warning("Input is empty.")

# ==========================================
# 🚀 APP 2: DEAL HUNTER
# ==========================================
elif app_mode == "🕵️ Deal Hunter":
    st.markdown("<h1>🕵️ Deal Hunter</h1>", unsafe_allow_html=True)
    st.markdown("<p>Global Asset & Capital Scanner</p>", unsafe_allow_html=True)
    
    # SEARCH BAR
    search_query = st.text_input("🔍 Search Database (e.g., 'Grant', 'Crypto', 'AI')", placeholder="Filter by type or name...")
    
    # TABS
    tab1, tab2, tab3 = st.tabs(["💎 ALL ASSETS", "⚡ LIVE COUPONS", "📡 RADAR"])
    
    with tab1:
        assets = engine.get_assets(search_query)
        for a in assets:
            # Color coding tags
            color = "tag-purple" if a['Type'] == "AI Model" else "tag-green" if a['Type'] == "Grant" else "tag-orange"
            
            st.markdown(f"""
            <div class="glass-card" style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <span class="tag {color}">{a['Type']}</span>
                    <span style="margin-left:10px; font-weight:bold; color:#fff;">{a['Name']}</span>
                    <div style="font-size:0.8em; margin-top:5px; opacity:0.7;">{a['Source']} • {a['Tag']}</div>
                </div>
                <a href="{a['Link']}" target="_blank" style="text-decoration:none;">
                    <button style="background:#222; color:white; border:1px solid #333; padding:8px 16px; border-radius:6px; cursor:pointer;">View ↗</button>
                </a>
            </div>
            """, unsafe_allow_html=True)
            
    with tab2:
        if st.button("🔄 SCAN LATEST COUPONS"):
            deals = engine.scrape_live_coupons()
            for d in deals:
                st.markdown(f"""
                <div class="glass-card">
                    <span class="tag tag-blue">100% OFF</span>
                    <h4 style="margin:10px 0;">{d['Title']}</h4>
                    <a href="{d['Link']}" target="_blank" style="color:#60a5fa; font-weight:bold;">Claim Deal ➜</a>
                </div>
                """, unsafe_allow_html=True)
                
    with tab3:
        st.markdown("### 📡 Live Radar")
        c1, c2 = st.columns(2)
        with c1:
            st.info("🦄 **Product Hunt:** Scanning for launches...")
            st.markdown("- **Devin AI** (Trending #1)\n- **Sora** (Video Gen)")
        with c2:
            st.success("💰 **Hackathons:** Active now")
            st.markdown("- **ETHGlobal London** ($500k Prize)\n- **Solana Renaissance** ($1M Prize)")
