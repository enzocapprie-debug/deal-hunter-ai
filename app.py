import streamlit as st
import feedparser
import requests
from bs4 import BeautifulSoup
import pandas as pd
import google.generativeai as genai

# ==========================================
# 🎨 UI & THEME ENGINE
# ==========================================
st.set_page_config(page_title="Founder OS v7 (Gemini)", page_icon="⚡", layout="wide")

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
    
    .stTextArea textarea, .stTextInput input {
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
    }
    
    .tag {display: inline-block; padding: 4px 10px; border-radius: 6px; font-size: 10px; font-weight: 700;}
    .tag-blue {background: rgba(59, 130, 246, 0.15); color: #60a5fa !important;}
    .tag-green {background: rgba(16, 185, 129, 0.15); color: #34d399 !important;}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 🧠 BACKEND LOGIC (GEMINI UPGRADE)
# ==========================================

class FounderEngine:
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0'}

    def generate_code_gemini(self, prompt, stack, mode, api_key):
        if not api_key:
            return "⚠️ Error: Please enter your Google Gemini API Key in the sidebar."
        
        try:
            # [...](asc_slot://start-slot-13)Configure Gemini
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Context Prompt
            system_instruction = f"You are an expert {stack} developer."
            if mode == "Debugger":
                user_msg = f"{system_instruction} Fix this broken code and explain the fix:\n\n{prompt}"
            else:
                user_msg = f"{system_instruction} Write production-ready code for: {prompt}. Provide ONLY the code, no markdown ticks."
            
            response = model.generate_content(user_msg)
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"

    def get_assets(self):
        return [
            {"Name": "DeepSeek-R1", "Type": "AI Model", "Source": "HuggingFace", "Link": "https://huggingface.co/deepseek-ai/DeepSeek-R1"},
            {"Name": "Microsoft Founders", "Type": "Grant", "Source": "Microsoft", "Link": "https://www.microsoft.com/en-us/startups"},
            {"Name": "Google Cloud", "Type": "Grant", "Source": "Google", "Link": "https://startup.google.com/cloud/"},
            {"Name": "AWS Activate", "Type": "Grant", "Source": "Amazon", "Link": "https://aws.amazon.com/activate/"},
            {"Name": "Udemy 100% Off", "Type": "Coupon", "Source": "Discudemy", "Link": "https://www.discudemy.com/all"}
        ]

    def scrape_coupons(self):
        deals = []
        try:
            resp = requests.get("https://www.discudemy.com/all", headers=self.headers, timeout=5)
            soup = BeautifulSoup(resp.text, 'html.parser')
            for item in soup.find_all('section', class_='card')[:12]:
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
    st.markdown("### Founder OS <span style='font-size:0.8em; color:#3b82f6'>v7.0</span>", unsafe_allow_html=True)
    st.markdown("---")
    app_mode = st.radio("SELECT MODULE", ["💻 Gemini Studio", "🕵️ Deal Hunter"])
    st.markdown("---")
    # THE KEY SLOT
    gemini_key = st.text_input("Gemini API Key", type="password", help="Get it from aistudio.google.com")

if app_mode == "💻 Gemini Studio":
    st.markdown("<h1>💻 Gemini Code Studio</h1>", unsafe_allow_html=True)
    st.markdown("<p>Powered by Google Gemini 1.5 Flash</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1: mode = st.selectbox("Mode", ["Generator", "Debugger"])
    with col2: stack = st.selectbox("Stack", ["HTML/Tailwind", "React", "Python"])
    
    prompt = st.text_area("Input Command", height=150, placeholder="e.g., Create a sticky navbar with a glassmorphism effect...")
    
    if st.button("RUN GEMINI ⚡"):
        with st.spinner("Gemini is coding..."):
            result = engine.generate_code_gemini(prompt, stack, mode, gemini_key)
            st.code(result)

elif app_mode == "🕵️ Deal Hunter":
    st.markdown("<h1>🕵️ Deal Hunter</h1>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["💎 ASSETS", "⚡ LIVE COUPONS"])
    
    [...](asc_slot://start-slot-15)with tab1:
        for a in engine.get_assets():
            st.markdown(f"""
            <div class="glass-card" style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <span class="tag tag-green">{a['Type']}</span>
                    <span style="margin-left:10px; font-weight:bold; color:#fff;">{a['Name']}</span>
                </div>
                <a href="{a['Link']}" target="_blank" style="text-decoration:none; color:#3b82f6; font-weight:bold;">View ↗</a>
            </div>
            """, unsafe_allow_html=True)
            
    with tab2:
        if st.button("SCAN COUPONS"):
            deals = engine.scrape_coupons()
            for d in deals:
                st.markdown(f"""
                <div class="glass-card">
                    <span class="tag tag-blue">100% OFF</span>
                    <h4 style="margin:10px 0;">{d['Title']}</h4>
                    <a href="{d['Link']}" target="_blank" style="color:#60a5fa; font-weight:bold;">Claim ➜</a>
                </div>""", unsafe_allow_html=True)
