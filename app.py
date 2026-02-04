#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import streamlit as st
from groq import Groq
import json
from datetime import datetime

st.set_page_config(
    page_title="أبو سعود",
    page_icon="🇯🇴",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS محسّن مع ألوان واضحة
st.markdown("""
<style>
    * {
        direction: rtl;
        text-align: right;
    }
    
    html, body, [data-testid="stAppViewContainer"] {
        background: #ffffff;
    }
    
    [data-testid="stHeader"] {
        background: transparent;
    }
    
    [data-testid="stToolbar"] {
        display: none;
    }
    
    .main {
        background: white;
    }
    
    /* الشعار الأردني */
    .jordanian-header {
        text-align: center;
        padding: 40px;
        background: linear-gradient(135deg, #CE112E 0%, #8B0000 100%);
        border-radius: 15px;
        color: white;
        margin-bottom: 30px;
        box-shadow: 0 8px 32px rgba(206, 17, 38, 0.3);
    }
    
    .jordanian-header h1 {
        font-size: 56px;
        margin: 0;
        font-weight: 900;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        letter-spacing: 2px;
    }
    
    .jordanian-header p {
        margin: 15px 0 0 0;
        font-size: 18px;
        opacity: 0.95;
        font-weight: 500;
    }
    
    /* الشريط الجانبي */
    [data-testid="stSidebar"] {
        background: #f8f9fa;
        border-right: 4px solid #CE112E;
    }
    
    [data-testid="stSidebar"] h3 {
        color: #2c3e50;
        font-weight: 700;
        margin-top: 20px;
        margin-bottom: 15px;
        font-size: 18px;
    }
    
    [data-testid="stSidebar"] h4 {
        color: #34495e;
        font-weight: 600;
        margin-top: 15px;
        margin-bottom: 10px;
        font-size: 14px;
    }
    
    /* الأزرار */
    .stButton > button {
        background: linear-gradient(135deg, #CE112E 0%, #a00a2e 100%);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: bold;
        font-size: 14px;
        padding: 10px 20px;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(206, 17, 38, 0.3);
    }
    
    /* حقول الإدخال */
    .stSelectbox, .stRadio {
        color: #2c3e50;
    }
    
    [data-testid="stChatInputContainer"] input {
        border-radius: 25px;
        border: 2px solid #CE112E !important;
        padding: 12px 20px !important;
        font-size: 16px !important;
        color: #2c3e50 !important;
    }
    
    [data-testid="stChatInputContainer"] input:focus {
        border: 2px solid #a00a2e !important;
        box-shadow: 0 0 10px rgba(206, 17, 38, 0.3) !important;
    }
    
    /* الرسائل */
    .stChatMessage {
        padding: 15px;
        border-radius: 12px;
        margin: 10px 0;
    }
    
    /* النصوص */
    .stMarkdown {
        color: #2c3e50;
    }
    
    /* البطاقات */
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        border-left: 4px solid #CE112E;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    
    /* الفاصل */
    hr {
        border-color: #CE112E;
        margin: 20px 0;
    }
    
    /* النصوص الصغيرة */
    .stCaption {
        color: #555;
        font-size: 13px;
        line-height: 1.6;
    }
    
    /* الأيقونات */
    .icon-row {
        display: flex;
        gap: 10px;
        justify-content: center;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# الحصول على API key
try:
    api_key = st.secrets["GROQ_API_KEY"]
except:
    st.error("❌ خطأ: مفتاح API غير موجود!")
    st.stop()

# تهيئة الجلسة
if "messages" not in st.session_state:
    st.session_state.messages = []
if "conversations" not in st.session_state:
    st.session_state.conversations = {}
if "current_conversation" not in st.session_state:
    st.session_state.current_conversation = None
if "theme" not in st.session_state:
    st.session_state.theme = "light"
if "stats" not in st.session_state:
    st.session_state.stats = {"total_messages": 0, "total_conversations": 0}

# الشريط الجانبي
with st.sidebar:
    st.markdown("### ⚙️ الإعدادات")
    
    # المظهر
    st.markdown("#### 🎨 المظهر")
    theme = st.radio("اختر المظهر:", ["☀️ فاتح", "🌙 غامق"], horizontal=False)
    st.session_state.theme = "dark" if "🌙" in theme else "light"
    
    # اللغة
    st.markdown("#### 🌐 اللغة")
    language = st.selectbox("اختر اللغة:", ["العربية 🇯🇴", "English 🇬🇧"], label_visibility="collapsed")
    
    st.divider()
    
    # المحادثات
    st.markdown("### 💬 المحادثات")
    
    if st.button("➕ محادثة جديدة", use_container_width=True):
        new_id = f"conv_{len(st.session_state.conversations) + 1}"
        st.session_state.conversations[new_id] = []
        st.session_state.current_conversation = new_id
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    
    # قائمة المحادثات السابقة
    if st.session_state.conversations:
        st.markdown("**المحادثات السابقة:**")
        for conv_id, conv_messages in st.session_state.conversations.items():
            if conv_messages:
                first_msg = conv_messages[0]["content"][:25] + "..."
                if st.button(f"📌 {first_msg}", use_container_width=True, key=f"conv_{conv_id}"):
                    st.session_state.current_conversation = conv_id
                    st.session_state.messages = conv_messages
                    st.rerun()
    
    st.divider()
    
    # الإحصائيات
    st.markdown("### 📊 الإحصائيات")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("💬 الرسائل", st.session_state.stats["total_messages"])
    with col2:
        st.metric("📁 المحادثات", st.session_state.stats["total_conversations"])
    
    st.divider()
    
    # الخيارات
    st.markdown("### 🛠️ الخيارات")
    
    if st.button("🗑️ مسح المحادثة", use_container_width=True):
        st.session_state.messages = []
        st.success("تم مسح المحادثة ✓")
        st.rerun()
    
    if st.button("💾 تحميل المحادثة", use_container_width=True):
        if st.session_state.messages:
            filename = f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            st.download_button(
                label="📥 اضغط للتحميل",
                data=json.dumps(st.session_state.messages, ensure_ascii=False, indent=2),
                file_name=filename,
                mime="application/json",
                use_container_width=True
            )
        else:
            st.warning("لا توجد محادثة لتحميلها")
    
    st.divider()
    
    # معلومات التطبيق
    st.markdown("### ℹ️ عن التطبيق")
    st.caption("""
**أبو سعود**
وكيل ذكي أردني متقدم

**المطور:**
راشد خليل محمد أبو زيتونه

**التواصل:**
📧 hhh123rrhhh@gmail.com
📱 0775866283
💬 واتس آب

**الحقوق:**
© 2026 جميع الحقوق محفوظة
    """)

# المحتوى الرئيسي
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # الشعار الأردني
    st.markdown("""
    <div class="jordanian-header">
        <h1>🇯🇴 أبو سعود</h1>
        <p>وكيلك الذكي الأردني</p>
    </div>
    """, unsafe_allow_html=True)

# عرض الرسائل
for idx, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.write(message["content"])
        
        if message["role"] == "assistant":
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                if st.button("👍 نافع", key=f"like_{idx}"):
                    st.toast("شكراً على التقييم الإيجابي! 😊")
            with col2:
                if st.button("👎 ما نافع", key=f"dislike_{idx}"):
                    st.toast("سنحاول تحسين الردود 💪")
            with col3:
                if st.button("📋 نسخ", key=f"copy_{idx}"):
                    st.toast("تم النسخ ✓")
            with col4:
                if st.button("🔄 إعادة", key=f"retry_{idx}"):
                    st.toast("جاري إعادة الرد...")

# حقل الإدخال
if prompt := st.chat_input("اكتب رسالتك هنا..."):
    # إضافة رسالة المستخدم
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.stats["total_messages"] += 1
    
    with st.chat_message("user"):
        st.write(prompt)
    
    # الحصول على الرد
    with st.chat_message("assistant"):
        with st.spinner("⏳ جاري الرد..."):
            try:
                client = Groq(api_key=api_key)
                
                # تحضير الرسائل
                messages = [
                    {
                        "role": "system",
                        "content": "أنت أبو سعود، وكيل ذكي أردني. أجب على كل الأسئلة بحرية تامة وبطابع أردني."
                    }
                ]
                
                # إضافة الرسائل السابقة
                for msg in st.session_state.messages:
                    messages.append(msg)
                
                # استدعاء Groq API
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=messages,
                    temperature=1.0,
                    max_tokens=2000
                )
                
                assistant_message = response.choices[0].message.content
                st.write(assistant_message)
                
                # أزرار التقييم
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    if st.button("👍 نافع", key=f"like_new"):
                        st.toast("شكراً على التقييم الإيجابي! 😊")
                with col2:
                    if st.button("👎 ما نافع", key=f"dislike_new"):
                        st.toast("سنحاول تحسين الردود 💪")
                with col3:
                    if st.button("📋 نسخ", key=f"copy_new"):
                        st.toast("تم النسخ ✓")
                with col4:
                    if st.button("🔄 إعادة", key=f"retry_new"):
                        st.toast("جاري إعادة الرد...")
                
                # حفظ الرد
                st.session_state.messages.append({"role": "assistant", "content": assistant_message})
                
                # حفظ المحادثة
                if st.session_state.current_conversation:
                    st.session_state.conversations[st.session_state.current_conversation] = st.session_state.messages
                else:
                    new_id = f"conv_{len(st.session_state.conversations) + 1}"
                    st.session_state.conversations[new_id] = st.session_state.messages
                    st.session_state.current_conversation = new_id
                    st.session_state.stats["total_conversations"] += 1
                
            except Exception as e:
                st.error(f"❌ خطأ: {str(e)}")

# الفوتر
st.divider()
st.markdown("""
<div style='text-align: center; color: #555; font-size: 13px; margin-top: 30px;'>
    <p><strong>🇯🇴 أبو سعود - وكيلك الذكي الأردني</strong></p>
    <p>من تطوير: راشد خليل محمد أبو زيتونه</p>
    <p>© 2026 جميع الحقوق محفوظة | تطبيق ذكي أردني 100%</p>
</div>
""", unsafe_allow_html=True)
