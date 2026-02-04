#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import streamlit as st
from groq import Groq
import json
from datetime import datetime
import pyperclip

st.set_page_config(
    page_title="أبو سعود",
    page_icon="🇯🇴",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS محسّن
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
        max-width: 900px;
        margin: 0 auto;
    }
    
    /* الشعار الأردني */
    .jordanian-header {
        text-align: center;
        padding: 40px 20px;
        background: linear-gradient(135deg, #CE112E 0%, #8B0000 100%);
        border-radius: 15px;
        color: white;
        margin-bottom: 30px;
        box-shadow: 0 8px 32px rgba(206, 17, 38, 0.3);
    }
    
    .jordanian-header h1 {
        font-size: 48px;
        margin: 0;
        font-weight: 900;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        letter-spacing: 2px;
    }
    
    .jordanian-header p {
        margin: 15px 0 0 0;
        font-size: 16px;
        opacity: 0.95;
        font-weight: 500;
    }
    
    /* زر القائمة */
    .menu-button {
        position: fixed;
        top: 20px;
        left: 20px;
        z-index: 999;
        background: #CE112E;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 15px;
        font-size: 24px;
        cursor: pointer;
        box-shadow: 0 4px 12px rgba(206, 17, 38, 0.3);
    }
    
    .menu-button:hover {
        background: #a00a2e;
        transform: scale(1.05);
    }
    
    /* حقل الإدخال */
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
    
    /* الأزرار الصغيرة */
    .action-buttons {
        display: flex;
        gap: 8px;
        margin-top: 10px;
        justify-content: flex-start;
        flex-wrap: wrap;
    }
    
    .action-button {
        background: #f0f0f0;
        border: 1px solid #ddd;
        border-radius: 6px;
        padding: 6px 12px;
        font-size: 12px;
        cursor: pointer;
        transition: all 0.2s ease;
        color: #2c3e50;
    }
    
    .action-button:hover {
        background: #CE112E;
        color: white;
        border-color: #CE112E;
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
if "show_menu" not in st.session_state:
    st.session_state.show_menu = False
if "stats" not in st.session_state:
    st.session_state.stats = {"total_messages": 0, "total_conversations": 0}

# زر القائمة (ثلاث شحطات)
col1, col2, col3 = st.columns([1, 20, 1])
with col1:
    if st.button("☰", key="menu_toggle", help="فتح الإعدادات"):
        st.session_state.show_menu = not st.session_state.show_menu

# عرض القائمة إذا تم فتحها
if st.session_state.show_menu:
    with st.expander("⚙️ الإعدادات والأدوات", expanded=True):
        
        # المحادثات
        st.markdown("### 💬 المحادثات")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("➕ محادثة جديدة"):
                new_id = f"conv_{len(st.session_state.conversations) + 1}"
                st.session_state.conversations[new_id] = []
                st.session_state.current_conversation = new_id
                st.session_state.messages = []
                st.success("تم إنشاء محادثة جديدة ✓")
                st.rerun()
        with col2:
            if st.button("🗑️ مسح المحادثة"):
                st.session_state.messages = []
                st.success("تم مسح المحادثة ✓")
                st.rerun()
        
        # المحادثات السابقة
        if st.session_state.conversations:
            st.markdown("**المحادثات السابقة:**")
            for conv_id, conv_messages in st.session_state.conversations.items():
                if conv_messages:
                    first_msg = conv_messages[0]["content"][:30] + "..."
                    if st.button(f"📌 {first_msg}", key=f"conv_{conv_id}"):
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
        
        # التحميل
        st.markdown("### 💾 التحميل")
        if st.session_state.messages:
            filename = f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            st.download_button(
                label="📥 تحميل المحادثة",
                data=json.dumps(st.session_state.messages, ensure_ascii=False, indent=2),
                file_name=filename,
                mime="application/json",
                use_container_width=True
            )
        else:
            st.info("لا توجد محادثة لتحميلها")
        
        st.divider()
        
        # معلومات التطبيق
        st.markdown("### ℹ️ عن التطبيق")
        st.caption("""
**أبو سعود** - وكيل ذكي أردني

**المطور:**
راشد خليل محمد أبو زيتونه

**التواصل:**
📧 hhh123rrhhh@gmail.com
📱 0775866283

**الحقوق:**
© 2026 جميع الحقوق محفوظة
        """)

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
                if st.button("👍", key=f"like_{idx}", help="نافع"):
                    st.toast("شكراً على التقييم الإيجابي! 😊")
            with col2:
                if st.button("👎", key=f"dislike_{idx}", help="ما نافع"):
                    st.toast("سنحاول تحسين الردود 💪")
            with col3:
                if st.button("📋", key=f"copy_{idx}", help="نسخ"):
                    st.toast("تم النسخ ✓")
            with col4:
                if st.button("🔄", key=f"retry_{idx}", help="إعادة"):
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
                    if st.button("👍", key=f"like_new", help="نافع"):
                        st.toast("شكراً على التقييم الإيجابي! 😊")
                with col2:
                    if st.button("👎", key=f"dislike_new", help="ما نافع"):
                        st.toast("سنحاول تحسين الردود 💪")
                with col3:
                    if st.button("📋", key=f"copy_new", help="نسخ"):
                        st.toast("تم النسخ ✓")
                with col4:
                    if st.button("🔄", key=f"retry_new", help="إعادة"):
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
<div style='text-align: center; color: #555; font-size: 12px; margin-top: 30px;'>
    <p>© 2026 راشد خليل محمد أبو زيتونه - جميع الحقوق محفوظة</p>
</div>
""", unsafe_allow_html=True)
