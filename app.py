#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import streamlit as st
from groq import Groq
from datetime import datetime

st.set_page_config(
    page_title="أبو سعود",
    page_icon="🇯🇴",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS
st.markdown("""
<style>
    * {
        direction: rtl;
        text-align: right;
    }
    
    html, body, [data-testid="stAppViewContainer"] {
        background: #ffffff !important;
        color: #000000 !important;
    }
    
    [data-testid="stSidebar"] {
        background: #f7f7f7 !important;
        border-left: 1px solid #d1d5db !important;
        width: 280px !important;
        position: fixed !important;
        right: 0 !important;
        height: 100vh !important;
        z-index: 50 !important;
    }
    
    [data-testid="stSidebarContent"] {
        padding: 16px !important;
        overflow-y: auto !important;
        height: 100vh !important;
    }
    
    [data-testid="stMainBlockContainer"] {
        background: #ffffff !important;
        padding: 20px !important;
        margin-bottom: 100px !important;
        margin-right: 280px !important;
        max-width: 900px !important;
    }
    
    [data-testid="stChatInputContainer"] {
        background: #ffffff !important;
        border-top: 1px solid #d1d5db !important;
        padding: 16px 20px !important;
        position: fixed !important;
        bottom: 0 !important;
        left: 0 !important;
        right: 280px !important;
        z-index: 100 !important;
    }
    
    [data-testid="stChatInputContainer"] textarea {
        border-radius: 12px !important;
        border: 1px solid #d1d5db !important;
        background: #ffffff !important;
        color: #000000 !important;
        padding: 12px 16px !important;
        font-size: 15px !important;
        resize: none !important;
        min-height: 44px !important;
        max-height: 150px !important;
        direction: rtl !important;
        text-align: right !important;
    }
    
    [data-testid="stChatInputContainer"] textarea:focus {
        border: 1px solid #10a37f !important;
        box-shadow: 0 0 0 2px rgba(16, 163, 127, 0.1) !important;
        outline: none !important;
    }
    
    [data-testid="stChatInputContainer"] button {
        background: transparent !important;
        border: none !important;
        color: #10a37f !important;
        font-size: 18px !important;
        cursor: pointer !important;
        padding: 8px !important;
        transition: all 0.2s ease !important;
    }
    
    [data-testid="stChatInputContainer"] button:hover {
        color: #0d8659 !important;
        transform: scale(1.1) !important;
    }
    
    [data-testid="stChatMessage"] {
        margin: 16px 0 !important;
    }
    
    [data-testid="stChatMessage"]:has(svg[data-testid="stChatMessageAvatarUser"]) {
        flex-direction: row-reverse !important;
    }
    
    [data-testid="stChatMessage"]:has(svg[data-testid="stChatMessageAvatarUser"]) > div > div {
        background: #10a37f !important;
        color: white !important;
        border-radius: 18px !important;
        padding: 12px 16px !important;
        max-width: 70% !important;
        margin-left: auto !important;
    }
    
    [data-testid="stChatMessage"]:has(svg[data-testid="stChatMessageAvatarAssistant"]) > div > div {
        background: #f7f7f7 !important;
        color: #000000 !important;
        border-radius: 18px !important;
        padding: 12px 16px !important;
        max-width: 70% !important;
        margin-right: auto !important;
    }
    
    [data-testid="stChatMessageAvatarUser"],
    [data-testid="stChatMessageAvatarAssistant"] {
        display: none !important;
    }
    
    .stButton > button {
        background: transparent !important;
        color: #000000 !important;
        border: 1px solid #d1d5db !important;
        border-radius: 8px !important;
        padding: 8px 12px !important;
        font-size: 13px !important;
        transition: all 0.2s ease !important;
    }
    
    .stButton > button:hover {
        background: #f7f7f7 !important;
        border-color: #10a37f !important;
    }
    
    p, span, div, h1, h2, h3, h4, h5, h6, label {
        color: #000000 !important;
        direction: rtl !important;
        text-align: right !important;
    }
    
    [data-testid="stHeader"],
    [data-testid="stToolbar"],
    [data-testid="stDecoration"] {
        display: none !important;
    }
</style>
""", unsafe_allow_html=True)

# Get API key
try:
    api_key = st.secrets["GROQ_API_KEY"]
except:
    st.error("❌ خطأ: مفتاح API غير موجود!")
    st.stop()

# Session State
if "messages" not in st.session_state:
    st.session_state.messages = []
if "saved_conversations" not in st.session_state:
    st.session_state.saved_conversations = []
if "security_mode" not in st.session_state:
    st.session_state.security_mode = False

def detect_emotion(text):
    """تحليل بسيط للمشاعر"""
    positive_words = ["شكراً", "ممتاز", "رائع", "جميل", "أحب", "يعجبني", "ممتن"]
    negative_words = ["سيء", "سخيف", "فاشل", "كره", "غضب", "محبط", "مزعج"]
    
    text_lower = text.lower()
    
    if any(word in text_lower for word in positive_words):
        return "positive"
    elif any(word in text_lower for word in negative_words):
        return "negative"
    return "neutral"

# Sidebar - شريط المهام على اليمين
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; margin-bottom: 20px;'>
        <h2 style='margin: 0; font-size: 20px;'>🇯🇴 أبو سعود</h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("✏️ جديد", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    
    with col2:
        if st.button("🔍 بحث", use_container_width=True):
            pass
    
    st.divider()
    
    st.subheader("المحادثات")
    
    if st.session_state.saved_conversations:
        for idx, conv in enumerate(st.session_state.saved_conversations):
            col1, col2 = st.columns([4, 1])
            with col1:
                if st.button(f"{conv['title'][:25]}", use_container_width=True, key=f"saved_{idx}"):
                    st.session_state.messages = conv['messages'].copy()
                    st.rerun()
            with col2:
                if st.button("🗑️", key=f"delete_{idx}"):
                    st.session_state.saved_conversations.pop(idx)
                    st.rerun()
    else:
        st.caption("لا توجد محادثات محفوظة")
    
    st.divider()
    
    st.subheader("🔒 الأمان")
    
    if st.button("🛡️ وضع الأمان", use_container_width=True):
        st.session_state.security_mode = not st.session_state.security_mode
    
    if st.session_state.security_mode:
        st.success("✓ وضع الأمان مفعّل")
        st.caption("الوكيل سيراقب الأنشطة المريبة")
    
    if st.button("🔐 تحليل الأمان", use_container_width=True):
        st.info("🔍 جاري فحص الأمان...")
    
    if st.button("📊 تقرير الحماية", use_container_width=True):
        st.info("📈 سيتم إنشاء تقرير شامل")
    
    st.divider()
    
    st.subheader("المعلومات")
    st.caption("""
    **مطورك:** راشد خليل محمد أبو زيتونه
    
    **البريد:** hhh123rrhhh@gmail.com
    
    **الواتس:** 0775866283
    """)

# Main Content
if len(st.session_state.messages) == 0:
    st.markdown("""
    <div style='text-align: center; padding: 200px 20px;'>
        <h1 style='font-size: 36px; margin-bottom: 10px;'>مرحباً بك</h1>
        <p style='color: #999; font-size: 16px;'>ابدأ محادثة جديدة مع أبو سعود</p>
    </div>
    """, unsafe_allow_html=True)
else:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
            
            if message["role"] == "assistant":
                col1, col2, col3 = st.columns([1, 1, 10])
                
                with col1:
                    if st.button("👍", key=f"like_{id(message)}"):
                        st.toast("✓ شكراً!")
                
                with col2:
                    if st.button("👎", key=f"dislike_{id(message)}"):
                        st.toast("✓ سنحاول التحسن")

# Chat Input
if prompt := st.chat_input("اكتب رسالتك..."):
    emotion = detect_emotion(prompt)
    
    st.session_state.messages.append({"role": "user", "content": prompt, "emotion": emotion})
    
    with st.chat_message("user"):
        st.write(prompt)
    
    with st.chat_message("assistant"):
        try:
            client = Groq(api_key=api_key)
            
            system_prompt = """أنت أبو سعود، وكيل ذكي.
مطورك: راشد خليل محمد أبو زيتونه

قدراتك:
- تتعلم من المحادثات السابقة
- تفهم المشاعر والانفعالات
- تقدم إجابات مخصصة
- تتحدث باللغة العربية الفصحى
- تراقب الأمان والحماية

معلومات عن المستخدم:
- الاسم: راشد خليل محمد أبو زيتونه
- البريد: hhh123rrhhh@gmail.com
- الواتس: 0775866283"""
            
            messages = [{"role": "system", "content": system_prompt}]
            for msg in st.session_state.messages:
                messages.append({"role": msg["role"], "content": msg["content"]})
            
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                max_tokens=2000
            )
            
            assistant_message = response.choices[0].message.content
            st.write(assistant_message)
            
            st.session_state.messages.append({"role": "assistant", "content": assistant_message, "emotion": "neutral"})
            
            # Show action buttons
            col1, col2, col3 = st.columns([1, 1, 10])
            
            with col1:
                if st.button("👍", key=f"like_new"):
                    st.toast("✓ شكراً!")
            
            with col2:
                if st.button("👎", key=f"dislike_new"):
                    st.toast("✓ سنحاول التحسن")
            
            st.rerun()
            
        except Exception as e:
            st.error(f"❌ خطأ: {str(e)}")

# Save Conversation Button
if len(st.session_state.messages) > 0:
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("💾 حفظ المحادثة", use_container_width=True):
            title = f"محادثة - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            st.session_state.saved_conversations.append({
                "title": title,
                "messages": st.session_state.messages.copy(),
                "created_at": datetime.now().isoformat()
            })
            st.toast("✓ تم الحفظ!")
    with col2:
        if st.button("🗑️ مسح المحادثة", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
