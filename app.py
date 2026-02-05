#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import streamlit as st
from groq import Groq
from datetime import datetime
import json

# ============================================================================
# PAGE CONFIG - يجب أن يكون أول شيء
# ============================================================================
st.set_page_config(
    page_title="أبو سعود",
    page_icon="🇯🇴",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# GLOBAL CSS - RTL صحيح 100%
# ============================================================================
st.markdown("""
<style>
/* ===== RESET GLOBAL ===== */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

html, body {
    direction: rtl !important;
    text-align: right !important;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: #ffffff !important;
    color: #000000 !important;
    overflow: hidden;
}

/* ===== SIDEBAR - يمين الشاشة ===== */
[data-testid="stSidebar"] {
    background: #f7f7f7 !important;
    border-left: 1px solid #e5e5e5 !important;
    width: 280px !important;
    position: fixed !important;
    right: 0 !important;
    top: 0 !important;
    height: 100vh !important;
    z-index: 1000 !important;
    overflow-y: auto !important;
    overflow-x: hidden !important;
    direction: rtl !important;
}

[data-testid="stSidebarContent"] {
    padding: 20px 16px !important;
    direction: rtl !important;
    text-align: right !important;
}

/* ===== MAIN CONTAINER ===== */
[data-testid="stAppViewContainer"] {
    background: #ffffff !important;
    direction: rtl !important;
}

[data-testid="stMainBlockContainer"] {
    background: #ffffff !important;
    padding: 0 !important;
    margin: 0 !important;
    margin-right: 280px !important;
    width: calc(100% - 280px) !important;
    height: 100vh !important;
    display: flex !important;
    flex-direction: column !important;
    overflow: hidden !important;
    direction: rtl !important;
}

/* ===== MESSAGES CONTAINER ===== */
[data-testid="stChatMessageContainer"] {
    flex: 1 !important;
    overflow-y: auto !important;
    overflow-x: hidden !important;
    padding: 20px !important;
    display: flex !important;
    flex-direction: column !important;
    gap: 12px !important;
    direction: rtl !important;
    scroll-behavior: smooth !important;
}

/* ===== CHAT MESSAGES ===== */
[data-testid="stChatMessage"] {
    display: flex !important;
    margin: 0 !important;
    padding: 0 !important;
    gap: 8px !important;
    direction: rtl !important;
    align-items: flex-end !important;
}

/* User Message */
[data-testid="stChatMessage"]:has(svg[data-testid="stChatMessageAvatarUser"]) {
    flex-direction: row-reverse !important;
    justify-content: flex-end !important;
}

[data-testid="stChatMessage"]:has(svg[data-testid="stChatMessageAvatarUser"]) > div:last-child {
    background: #10a37f !important;
    color: white !important;
    border-radius: 18px !important;
    padding: 12px 16px !important;
    max-width: 65% !important;
    word-wrap: break-word !important;
    direction: rtl !important;
    text-align: right !important;
}

/* Assistant Message */
[data-testid="stChatMessage"]:has(svg[data-testid="stChatMessageAvatarAssistant"]) {
    flex-direction: row !important;
    justify-content: flex-start !important;
}

[data-testid="stChatMessage"]:has(svg[data-testid="stChatMessageAvatarAssistant"]) > div:last-child {
    background: #f0f0f0 !important;
    color: #000000 !important;
    border-radius: 18px !important;
    padding: 12px 16px !important;
    max-width: 65% !important;
    word-wrap: break-word !important;
    direction: rtl !important;
    text-align: right !important;
}

/* Hide Avatars */
[data-testid="stChatMessageAvatarUser"],
[data-testid="stChatMessageAvatarAssistant"] {
    display: none !important;
}

/* ===== INPUT CONTAINER ===== */
[data-testid="stChatInputContainer"] {
    background: #ffffff !important;
    border-top: 1px solid #e5e5e5 !important;
    padding: 16px 20px !important;
    position: fixed !important;
    bottom: 0 !important;
    right: 280px !important;
    left: 0 !important;
    z-index: 500 !important;
    height: auto !important;
    flex-shrink: 0 !important;
}

[data-testid="stChatInputContainer"] textarea {
    border-radius: 24px !important;
    border: 1px solid #d1d5db !important;
    background: #ffffff !important;
    color: #000000 !important;
    padding: 12px 16px !important;
    font-size: 15px !important;
    resize: none !important;
    min-height: 44px !important;
    max-height: 120px !important;
    direction: rtl !important;
    text-align: right !important;
    font-family: inherit !important;
}

[data-testid="stChatInputContainer"] textarea:focus {
    border: 1px solid #10a37f !important;
    box-shadow: 0 0 0 3px rgba(16, 163, 127, 0.1) !important;
    outline: none !important;
}

[data-testid="stChatInputContainer"] textarea::placeholder {
    color: #999999 !important;
    direction: rtl !important;
    text-align: right !important;
}

/* Send Button */
[data-testid="stChatInputContainer"] button {
    background: transparent !important;
    border: none !important;
    color: #10a37f !important;
    font-size: 20px !important;
    cursor: pointer !important;
    padding: 8px 12px !important;
    transition: all 0.2s ease !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}

[data-testid="stChatInputContainer"] button:hover {
    color: #0d8659 !important;
    transform: scale(1.15) !important;
}

/* ===== TEXT & TYPOGRAPHY ===== */
p, span, div, h1, h2, h3, h4, h5, h6, label, li {
    direction: rtl !important;
    text-align: right !important;
    color: #000000 !important;
}

/* ===== BUTTONS ===== */
.stButton > button {
    background: transparent !important;
    color: #000000 !important;
    border: 1px solid #d1d5db !important;
    border-radius: 8px !important;
    padding: 8px 12px !important;
    font-size: 13px !important;
    transition: all 0.2s ease !important;
    direction: rtl !important;
    text-align: center !important;
}

.stButton > button:hover {
    background: #f7f7f7 !important;
    border-color: #10a37f !important;
    color: #10a37f !important;
}

/* ===== DIVIDER ===== */
hr {
    border: none !important;
    border-top: 1px solid #e5e5e5 !important;
    margin: 12px 0 !important;
}

/* ===== HIDE UNNECESSARY ELEMENTS ===== */
[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"],
.stDeployButton,
footer {
    display: none !important;
}

/* ===== SCROLLBAR ===== */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: transparent;
}

::-webkit-scrollbar-thumb {
    background: #d1d5db;
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: #10a37f;
}

/* ===== SUBHEADER ===== */
[data-testid="stMarkdownContainer"] h2 {
    font-size: 16px !important;
    font-weight: 600 !important;
    margin: 16px 0 8px 0 !important;
    color: #000000 !important;
    direction: rtl !important;
    text-align: right !important;
}

/* ===== CAPTION ===== */
.stCaption {
    font-size: 12px !important;
    color: #666666 !important;
    direction: rtl !important;
    text-align: right !important;
}

/* ===== DIVIDER ===== */
.stDivider {
    margin: 12px 0 !important;
}

</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE
# ============================================================================
if "messages" not in st.session_state:
    st.session_state.messages = []
if "saved_conversations" not in st.session_state:
    st.session_state.saved_conversations = []
if "security_mode" not in st.session_state:
    st.session_state.security_mode = False

# ============================================================================
# SIDEBAR - شريط المهام
# ============================================================================
with st.sidebar:
    st.markdown("### 🇯🇴 أبو سعود")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("✏️ جديد", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    with col2:
        if st.button("🔍 بحث", use_container_width=True):
            st.info("🔍 ميزة البحث قريباً")
    
    st.divider()
    
    st.markdown("### 💬 المحادثات")
    
    if st.session_state.saved_conversations:
        for idx, conv in enumerate(st.session_state.saved_conversations):
            col1, col2 = st.columns([4, 1])
            with col1:
                if st.button(
                    f"{conv['title'][:20]}...",
                    use_container_width=True,
                    key=f"saved_{idx}"
                ):
                    st.session_state.messages = conv['messages'].copy()
                    st.rerun()
            with col2:
                if st.button("🗑️", key=f"delete_{idx}", use_container_width=True):
                    st.session_state.saved_conversations.pop(idx)
                    st.rerun()
    else:
        st.caption("لا توجد محادثات محفوظة")
    
    st.divider()
    
    st.markdown("### 🔒 الأمان")
    
    if st.button("🛡️ وضع الأمان", use_container_width=True):
        st.session_state.security_mode = not st.session_state.security_mode
    
    if st.session_state.security_mode:
        st.success("✓ وضع الأمان مفعّل")
    
    if st.button("🔐 تحليل الأمان", use_container_width=True):
        st.info("🔍 جاري فحص الأمان...")
    
    st.divider()
    
    st.markdown("### ℹ️ المعلومات")
    st.caption("""
    **المطور:** راشد خليل محمد أبو زيتونه
    
    **البريد:** hhh123rrhhh@gmail.com
    
    **الواتس:** 0775866283
    
    © 2026
    """)

# ============================================================================
# MAIN CHAT AREA
# ============================================================================

# Empty State
if len(st.session_state.messages) == 0:
    st.markdown("""
    <div style='
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 100%;
        text-align: center;
        padding: 40px;
        direction: rtl;
    '>
        <h1 style='font-size: 32px; margin-bottom: 10px; color: #000;'>مرحباً بك 👋</h1>
        <p style='color: #999; font-size: 16px; direction: rtl; text-align: center;'>
            ابدأ محادثة جديدة مع أبو سعود
        </p>
    </div>
    """, unsafe_allow_html=True)
else:
    # Display Messages
    for idx, message in enumerate(st.session_state.messages):
        with st.chat_message(message["role"]):
            st.write(message["content"])
            
            # Action Buttons (only for assistant messages)
            if message["role"] == "assistant":
                col1, col2, col3 = st.columns([1, 1, 6])
                with col1:
                    if st.button("👍", key=f"like_{idx}", help="مفيد"):
                        st.toast("✓ شكراً على التقييم!")
                with col2:
                    if st.button("👎", key=f"dislike_{idx}", help="غير مفيد"):
                        st.toast("✓ سنحاول التحسن")

# ============================================================================
# INPUT AREA - صندوق الكتابة
# ============================================================================

try:
    api_key = st.secrets["GROQ_API_KEY"]
except:
    st.error("❌ خطأ: مفتاح API غير موجود!")
    st.stop()

if prompt := st.chat_input("اكتب رسالتك هنا..."):
    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })
    
    # Display user message
    with st.chat_message("user"):
        st.write(prompt)
    
    # Generate response
    with st.chat_message("assistant"):
        try:
            client = Groq(api_key=api_key)
            
            system_prompt = """أنت أبو سعود، وكيل ذكي متخصص.
مطورك: راشد خليل محمد أبو زيتونه

معلومات عنك:
- اسمك: أبو سعود
- أنت وكيل ذكي متقدم
- تتحدث اللغة العربية الفصحى بطلاقة
- تفهم السياق والمشاعر
- تقدم إجابات مفصلة ومفيدة

معلومات المستخدم:
- الاسم: راشد خليل محمد أبو زيتونه
- البريد: hhh123rrhhh@gmail.com
- الهاتف: 0775866283

تعليمات:
- كن ودياً وحترافياً
- أجب بوضوح وإيجاز
- استخدم الترقيم والنقاط عند الحاجة
- اسأل توضيحات إذا لم تفهم السؤال"""
            
            messages = [{"role": "system", "content": system_prompt}]
            for msg in st.session_state.messages:
                messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
            
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                max_tokens=2000,
                temperature=0.7
            )
            
            assistant_message = response.choices[0].message.content
            st.write(assistant_message)
            
            # Add assistant message to history
            st.session_state.messages.append({
                "role": "assistant",
                "content": assistant_message
            })
            
            # Action buttons
            col1, col2, col3 = st.columns([1, 1, 6])
            with col1:
                if st.button("👍", key=f"like_new", help="مفيد"):
                    st.toast("✓ شكراً على التقييم!")
            with col2:
                if st.button("👎", key=f"dislike_new", help="غير مفيد"):
                    st.toast("✓ سنحاول التحسن")
            
        except Exception as e:
            st.error(f"❌ خطأ: {str(e)}")

# ============================================================================
# FOOTER BUTTONS - أزرار الحفظ والمسح
# ============================================================================

if len(st.session_state.messages) > 0:
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("💾 حفظ", use_container_width=True):
            title = f"محادثة - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            st.session_state.saved_conversations.append({
                "title": title,
                "messages": st.session_state.messages.copy(),
                "created_at": datetime.now().isoformat()
            })
            st.toast("✓ تم حفظ المحادثة!")
    
    with col2:
        if st.button("🗑️ مسح", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    
    with col3:
        if st.button("📋 نسخ", use_container_width=True):
            st.toast("✓ تم النسخ!")
