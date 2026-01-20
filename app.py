import streamlit as st
import feedparser
import requests
from bs4 import BeautifulSoup
import pandas as pd
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

# ==========================================
# 🎨 UI & THEME ENGINE
# ==========================================
st.set_page_config(page_title="Founder OS v8.0", page_icon="⚡", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    .stApp {
        background: radial-gradient(circle at 50% 0%, #0f172a 0%, #000000 100%);
        font-family: 'Inter', sans-serif;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
    }
    
    h1, h2, h3 {color: white !important;}
    p, span, div, label {color: #94a3b8 !important;}
    
    .stTextArea textarea, .stTextInput input, .stSelectbox div[data-baseweb="select"] {
        background-color: #0F0F12 !important; 
        color: #e2e8f0 !important; 
        border: 1px solid #333 !important;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white !important;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        width: 100%;
    }
    
    .tag {display: inline-block; padding: 4px 10px; border-radius: 6px; font-size: 10px; font-weight: 700;}
    .tag-blue {background: rgba(59, 130, 246, 0.15); color: #60a5fa !important;}
    .tag-green {background: rgba(16, 185, 129, 0.15); color: #34d399 !important;}
    .tag-purple {background: rgba(139, 92, 246, 0.15); color: #a78bfa !important;}
    .tag-orange {background: rgba(245, 158, 11, 0.15); color: #fbbf24 !important;}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 🧠 BACKEND LOGIC (EXPANDED)
# ==========================================

class FounderEngine:
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0'}

    def generate_code_gemini(self, prompt, stack, mode, api_key):
        if not api_key:
            return "⚠️ Error: Please enter your Google Gemini API Key in the sidebar."
        
        try:
            genai.configure(api_key=api_key)
            
            # UNLOCKED SAFETY SETTINGS
            safety_settings = {
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            }
            
            model = genai.GenerativeModel(model_name='gemini-1.5-flash', safety_settings=safety_settings)
            
            # INTELLIGENT PROMPTING BASED ON MODE
            base_prompt = f"You are an expert {stack} developer."
            
            if mode == "Generator":
                user_msg = f"{base_prompt} Write production-ready code for: {prompt}. Provide ONLY the code, no markdown ticks."
            elif mode == "Debugger":
                user_msg = f"{base_prompt} Fix this broken code and explain the error:\n\n{prompt}"
            elif mode == "Security Audit":
                user_msg = f"{base_prompt} ANALYZE this code for security vulnerabilities (XSS, SQL Injection, etc) and provide a fixed version:\n\n{prompt}"
            elif mode == "Refactor/Optimize":
                user_msg = f"{base_prompt} REFACTOR this code to be cleaner, faster, and more professional:\n\n{prompt}"
            elif mode == "Documentation":
                user_msg = f"{base_prompt} Write professional documentation (README/Comments) for this code:\n\n{prompt}"
            elif mode == "Unit Tests":
                user_msg = f"{base_prompt} Write comprehensive Unit Tests for this code:\n\n{prompt}"
            
            response = model.generate_content(user_msg)
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"

    def get_assets(self, category):
        # EXPANDED DATABASE
        db = {
            "Grants": [
                {"Name": "Microsoft Founders", "Value": "$150k", "Link": "https://www.microsoft.com/en-us/startups"},
                {"Name": "Google Cloud", "Value": "$350k", "Link": "https://startup.google.com/cloud/"},
                {"Name": "AWS Activate", "Value": "$100k", "Link": "https://aws.amazon.com/activate/"},
                {"Name": "Notion Startups", "Value": "6 Mo Free", "Link": "https://www.notion.so/startups"},
                {"Name": "OpenAI Residency", "Value": "$$$", "Link": "https://openai.com/residencies"}
            ],
            "Crypto": [
                {"Name": "Binance Labs", "Value": "VC Fund", "Link": "https://labs.binance.com/"},
                {"Name": "Solana Grants", "Value": "Funding", "Link": "https://solana.org/grants"},
                {"Name": "Ethereum ESP", "Value": "Grants", "Link": "https://esp.ethereum.foundation/applicants"},
                {"Name": "Base Ecosystem", "Value": "Build", "Link": "https://base.org/ecosystem"},
                {"Name": "Optimism Retro", "Value": "Airdrop", "Link": "https://app.optimism.io/retropgf"}
            ],
            "Hackathons": [
                {"Name": "Devpost", "Value": "Global", "Link": "https://devpost.com/"},
                {"Name": "ETHGlobal", "Value": "Web3", "Link": "https://ethglobal.com/"},
                {"Name": "DoraHacks", "Value": "Crypto", "Link": "https://dorahacks.io/"},
                {"Name": "Kaggle Competitions", "Value": "AI/ML", "Link": "https://www.kaggle.com/competitions"}
            ],
            "AI Tools": [
                {"Name": "Hugging Face", "Value": "Models", "Link": "https://huggingface.co/"},
                {"Name": "Replicate", "Value": "API", "Link": "https://replicate.com/"},
                {"Name": "LangChain", "Value": "Framework", "Link": "https://www.langchain.com/"},
                {"Name": "Vercel AI SDK", "Value": "Frontend", "Link": "https://sdk.vercel.ai/docs"}
            ]
        }
        return db.get(category, [])

    def scrape_coupons(self):
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
# 🖥️ FRONTEND
# ==========================================

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/11529/11529610.png", width=50)
    st.markdown("### Founder OS <span style='font-size:0.8em; color:#3b82f6'>v8.0</span>", unsafe_allow_html=True)
    st.markdown("---")
    app_mode = st.radio("SELECT MODULE", ["💻 Gemini Studio", "🕵️ Deal Hunter"])
    st.markdown("---")
    gemini_key = st.text_input("Gemini API Key", type="password")

if app_mode == "💻 Gemini Studio":
    st.markdown("<h1>💻 Gemini Code Studio</h1>", unsafe_allow_html=True)
    
    # EXPANDED CONTROLS
    col1, col2 = st.columns(2)
    with col1: 
        mode = st.selectbox("Operation Mode", [
            "Generator", 
            "Debugger", 
            "Security Audit", 
            "Refactor/Optimize", 
            "Documentation", 
            "Unit Tests"
        ])
    with col2: 
        stack = st.selectbox("Tech Stack", [
            "HTML/Tailwind", 
            "React/Next.js", 
            "Python/Streamlit", 
            "Node.js/Express", 
            "Solidity (Web3)", 
            "Flutter/Dart",
            "SQL/Postgres",
            "Rust"
        ])
    
    prompt = st.text_area("Input Command", height=150, placeholder=f"Enter instructions for {mode}...")
    
    if st.button("EXECUTE AGENT ⚡"):
        with st.spinner("Gemini is working..."):
            result = engine.generate_code_gemini(prompt, stack, mode, gemini_key)
            st.code(result)

elif app_mode == "🕵️ Deal Hunter":
    st.markdown("<h1>🕵️ Deal Hunter</h1>", unsafe_allow_html=True)
    
    # EXPANDED TABS
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "💸 GRANTS", 
        "🪙 CRYPTO", 
        "🏆 HACKATHONS", 
        "🧠 AI TOOLS", 
        "⚡ COUPONS"
    ])
    
    def render_cards(category, color):
        for a in engine.get_assets(category):
            st.markdown(f"""
            <div class="glass-card" style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <span class="tag {color}">{a['Value']}</span>
                    <span style="margin-left:10px; font-weight:bold; color:#fff;">{a['Name']}</span>
                </div>
                <a href="{a['Link']}" target="_blank" style="text-decoration:none; color:#3b82f6; font-weight:bold;">View ↗</a>
            </div>
            """, unsafe_allow_html=True)

    with tab1: render_cards("Grants", "tag-green")
    with tab2: render_cards("Crypto", "tag-orange")
    with tab3: render_cards("Hackathons", "tag-purple")
    with tab4: render_cards("AI Tools", "tag-blue")
            
    with tab5:
        if st.button("SCAN 100% OFF COUPONS"):
            deals = engine.scrape_coupons()
            for d in deals:
                st.markdown(f"""
                <div class="glass-card">
                    <span class="tag tag-blue">FREE</span>
                    <h4 style="margin:10px 0;">{d['Title']}</h4>
                    <a href="{d['Link']}" target="_blank" style="color:#60a5fa; font-weight:bold;">Claim ➜</a>
                </div>""", unsafe_allow_html=True)
