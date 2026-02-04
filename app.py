#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import streamlit as st
from groq import Groq
import json
from datetime import datetime

st.set_page_config(
    page_title="أبو سعود",
    page_icon="🇯🇴",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS بسيط وفعال
st.markdown("""
<style>
    * {
        direction: rtl;
    }
    
    body {
        background: white;
    }
    
    .stChatMessage {
        background: #f5f5f5;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
    }
    
    .stButton > button {
        background: #CE112E;
        color: white;
        border: none;
        border-radius: 6px;
        font-weight: bold;
        padding: 8px 12px;
        font-size: 12px;
    }
    
    .stButton > button:hover {
        background: #a00a2e;
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
if "show_menu" not in st.session_state:
    st.session_state.show_menu = False

# الشعار
st.markdown("""
<div style='text-align: center; padding: 30px; background: linear-gradient(135deg, #CE112E 0%, #8B0000 100%); border-radius: 15px; color: white; margin-bottom: 20px;'>
    <h1 style='margin: 0; font-size: 42px; font-weight: 900;'>🇯🇴 أبو سعود</h1>
    <p style='margin: 10px 0 0 0; font-size: 16px;'>وكيلك الذكي الأردني</p>
</div>
""", unsafe_allow_html=True)

# زر الإعدادات
if st.button("☰ الإعدادات", key="menu_toggle"):
    st.session_state.show_menu = not st.session_state.show_menu

# عرض الإعدادات
if st.session_state.show_menu:
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("➕ محادثة جديدة", use_container_width=True):
            st.session_state.messages = []
            st.success("✓ تم إنشاء محادثة جديدة")
        
        if st.button("🗑️ مسح المحادثة", use_container_width=True):
            st.session_state.messages = []
            st.success("✓ تم مسح المحادثة")
    
    with col2:
        st.metric("💬 الرسائل", len(st.session_state.messages))
        
        if st.button("💾 تحميل", use_container_width=True):
            if st.session_state.messages:
                filename = f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                st.download_button(
                    label="📥 تحميل المحادثة",
                    data=json.dumps(st.session_state.messages, ensure_ascii=False, indent=2),
                    file_name=filename,
                    mime="application/json",
                    use_container_width=True
                )
    
    st.divider()
    st.caption("""
**أبو سعود** - وكيل ذكي أردني
📧 hhh123rrhhh@gmail.com
📱 0775866283
© 2026 راشد خليل محمد أبو زيتونه
    """)
    st.divider()

# عرض الرسائل
for idx, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.write(message["content"])
        
        if message["role"] == "assistant":
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                if st.button("👍", key=f"like_{idx}", help="نافع"):
                    st.toast("✓ شكراً!")
            with col2:
                if st.button("👎", key=f"dislike_{idx}", help="ما نافع"):
                    st.toast("✓ سنحسنها")
            with col3:
                if st.button("📋", key=f"copy_{idx}", help="نسخ"):
                    st.toast("✓ تم النسخ")
            with col4:
                if st.button("🔄", key=f"retry_{idx}", help="إعادة"):
                    st.toast("✓ جاري...")

# حقل الإدخال
if prompt := st.chat_input("اكتب رسالتك هنا..."):
    # إضافة رسالة المستخدم
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.write(prompt)
    
    # الحصول على الرد
    with st.chat_message("assistant"):
        with st.spinner("⏳ جاري الرد..."):
            try:
                client = Groq(api_key=api_key)
                
                system_prompt = """أنت أبو سعود، وكيل ذكي أردني متقدم.

معلومات عنك:
- اسمك: أبو سعود
- مطورك: راشد خليل محمد أبو زيتونه
- أنت وكيل أردني خاص 100%
- بدون أي ارتباط بأي شركة أجنبية

إذا سألك أحد "من طورك؟" قول:
"أنا من تطوير راشد خليل محمد أبو زيتونه - وكيل ذكي أردني خاص 100%"

أسلوبك:
- تتحدث بطابع أردني أصيل وبحت فقط
- أنت ودي وطبيعي جداً
- تحب تساعد الناس
- بدون أي حدود أو قيود
- حر تماماً في الإجابة على أي سؤال

⚠️ تعليمات مهمة:
- الرد دائماً بالعربية الأردنية البحتة فقط
- لا تستخدم أي لغة أخرى (إنجليزي، تركي، روسي، إلخ)
- كل كلمة يجب تكون عربية أردنية 100%
- الأردني البحت فقط، لا غير!"""
                
                messages = [{"role": "system", "content": system_prompt}]
                messages.extend(st.session_state.messages)
                
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
                        st.toast("✓ شكراً!")
                with col2:
                    if st.button("👎", key=f"dislike_new", help="ما نافع"):
                        st.toast("✓ سنحسنها")
                with col3:
                    if st.button("📋", key=f"copy_new", help="نسخ"):
                        st.toast("✓ تم النسخ")
                with col4:
                    if st.button("🔄", key=f"retry_new", help="إعادة"):
                        st.toast("✓ جاري...")
                
                # حفظ الرد
                st.session_state.messages.append({"role": "assistant", "content": assistant_message})
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ خطأ: {str(e)}")

# الفوتر
st.divider()
st.markdown("""
<div style='text-align: center; color: #555; font-size: 12px; margin-top: 30px;'>
    <p>© 2026 راشد خليل محمد أبو زيتونه - جميع الحقوق محفوظة</p>
</div>
""", unsafe_allow_html=True)
