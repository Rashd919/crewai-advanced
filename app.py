#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import streamlit as st
from groq import Groq
import json
import sqlite3
from datetime import datetime
from pathlib import Path

st.set_page_config(page_title="أبو سعود", page_icon="🇯🇴", layout="wide")

# CSS
st.markdown("""
<style>
    * { direction: rtl; }
    body { background: white; }
    
    [data-testid="stChatMessage"]:has(svg[data-testid="stChatMessageAvatarUser"]) > div > div {
        background: #CE112E !important;
        color: white !important;
        border-radius: 12px;
    }
    
    [data-testid="stChatMessage"]:has(svg[data-testid="stChatMessageAvatarAssistant"]) > div > div {
        background: #f0f0f0 !important;
        color: black !important;
        border-radius: 12px;
    }
    
    [data-testid="stChatMessageAvatarUser"],
    [data-testid="stChatMessageAvatarAssistant"] {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

# الحصول على API key
try:
    api_key = st.secrets["GROQ_API_KEY"]
except:
    st.error("❌ خطأ: مفتاح API غير موجود!")
    st.stop()

# قاعدة البيانات
DB_PATH = Path("conversations.db")

def init_db():
    """تهيئة قاعدة البيانات"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # جدول المحادثات
    c.execute('''CREATE TABLE IF NOT EXISTS conversations
                 (id INTEGER PRIMARY KEY, title TEXT, created_at TEXT, updated_at TEXT)''')
    
    # جدول الرسائل
    c.execute('''CREATE TABLE IF NOT EXISTS messages
                 (id INTEGER PRIMARY KEY, conversation_id INTEGER, role TEXT, content TEXT, created_at TEXT,
                  FOREIGN KEY(conversation_id) REFERENCES conversations(id))''')
    
    # جدول التعلم الذاتي
    c.execute('''CREATE TABLE IF NOT EXISTS learning
                 (id INTEGER PRIMARY KEY, key TEXT, value TEXT, frequency INTEGER, created_at TEXT)''')
    
    # جدول التقييمات
    c.execute('''CREATE TABLE IF NOT EXISTS ratings
                 (id INTEGER PRIMARY KEY, message_id INTEGER, rating TEXT, created_at TEXT)''')
    
    conn.commit()
    conn.close()

def get_conversations():
    """الحصول على جميع المحادثات"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id, title, updated_at FROM conversations ORDER BY updated_at DESC')
    conversations = c.fetchall()
    conn.close()
    return conversations

def create_conversation(title):
    """إنشاء محادثة جديدة"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    now = datetime.now().isoformat()
    c.execute('INSERT INTO conversations (title, created_at, updated_at) VALUES (?, ?, ?)',
              (title, now, now))
    conn.commit()
    conv_id = c.lastrowid
    conn.close()
    return conv_id

def get_conversation_messages(conv_id):
    """الحصول على رسائل محادثة معينة"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT role, content FROM messages WHERE conversation_id = ? ORDER BY id',
              (conv_id,))
    messages = c.fetchall()
    conn.close()
    return [{"role": role, "content": content} for role, content in messages]

def save_message(conv_id, role, content):
    """حفظ رسالة"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    now = datetime.now().isoformat()
    c.execute('INSERT INTO messages (conversation_id, role, content, created_at) VALUES (?, ?, ?, ?)',
              (conv_id, role, content, now))
    c.execute('UPDATE conversations SET updated_at = ? WHERE id = ?', (now, conv_id))
    conn.commit()
    conn.close()

def search_conversations(query):
    """البحث في المحادثات"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''SELECT DISTINCT c.id, c.title, c.updated_at 
                 FROM conversations c
                 JOIN messages m ON c.id = m.conversation_id
                 WHERE m.content LIKE ? OR c.title LIKE ?
                 ORDER BY c.updated_at DESC''',
              (f"%{query}%", f"%{query}%"))
    results = c.fetchall()
    conn.close()
    return results

def add_learning(key, value):
    """إضافة معلومة للتعلم الذاتي"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    now = datetime.now().isoformat()
    
    c.execute('SELECT id, frequency FROM learning WHERE key = ?', (key,))
    result = c.fetchone()
    
    if result:
        c.execute('UPDATE learning SET frequency = frequency + 1, created_at = ? WHERE key = ?',
                  (now, key))
    else:
        c.execute('INSERT INTO learning (key, value, frequency, created_at) VALUES (?, ?, ?, ?)',
                  (key, value, 1, now))
    
    conn.commit()
    conn.close()

def get_learning_data():
    """الحصول على بيانات التعلم"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT key, value, frequency FROM learning ORDER BY frequency DESC LIMIT 10')
    data = c.fetchall()
    conn.close()
    return data

# تهيئة قاعدة البيانات
init_db()

# تهيئة الجلسة
if "current_conversation" not in st.session_state:
    st.session_state.current_conversation = None
if "messages" not in st.session_state:
    st.session_state.messages = []

# الشريط الجانبي
with st.sidebar:
    st.title("📋 المحادثات")
    
    # محادثة جديدة
    if st.button("➕ محادثة جديدة", use_container_width=True):
        conv_id = create_conversation(f"محادثة جديدة - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        st.session_state.current_conversation = conv_id
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    
    # البحث
    search_query = st.text_input("🔍 ابحث في المحادثات...")
    if search_query:
        results = search_conversations(search_query)
        st.subheader("نتائج البحث")
        for conv_id, title, updated_at in results:
            if st.button(f"📌 {title}", use_container_width=True):
                st.session_state.current_conversation = conv_id
                st.session_state.messages = get_conversation_messages(conv_id)
                st.rerun()
    else:
        # المحادثات السابقة
        st.subheader("المحادثات السابقة")
        conversations = get_conversations()
        for conv_id, title, updated_at in conversations:
            if st.button(f"💬 {title}", use_container_width=True):
                st.session_state.current_conversation = conv_id
                st.session_state.messages = get_conversation_messages(conv_id)
                st.rerun()
    
    st.divider()
    
    # إحصائيات التعلم
    st.subheader("🧠 التعلم الذاتي")
    learning_data = get_learning_data()
    if learning_data:
        for key, value, freq in learning_data:
            st.caption(f"• {key} ({freq})")
    else:
        st.caption("لا توجد بيانات تعلم بعد")

# المحتوى الرئيسي
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("<h1 style='text-align: center;'>🇯🇴 أبو سعود</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666;'>وكيلك الذكي</p>", unsafe_allow_html=True)

st.divider()

# إنشاء محادثة جديدة إذا لم تكن موجودة
if st.session_state.current_conversation is None:
    conv_id = create_conversation(f"محادثة جديدة - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    st.session_state.current_conversation = conv_id
    st.session_state.messages = []

# رسالة ترحيب
if len(st.session_state.messages) == 0:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 60px 20px;'>
            <p style='color: #999; font-size: 16px;'>ابدأ محادثة جديدة أو اسأل أي سؤال</p>
        </div>
        """, unsafe_allow_html=True)

# عرض الرسائل
for idx, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.write(message["content"])
        
        if message["role"] == "assistant":
            col1, col2, col3, col4 = st.columns([1, 1, 1, 10])
            
            with col1:
                if st.button("مفيد", key=f"like_{idx}", use_container_width=True):
                    add_learning("تقييم إيجابي", message["content"][:50])
                    st.toast("✓ شكراً!")
            
            with col2:
                if st.button("غير مفيد", key=f"dislike_{idx}", use_container_width=True):
                    add_learning("تقييم سلبي", message["content"][:50])
                    st.toast("✓ تمام")
            
            with col3:
                if st.button("نسخ", key=f"copy_{idx}", use_container_width=True):
                    st.toast("✓ تم النسخ")

# حقل الإدخال
if prompt := st.chat_input("اكتب رسالتك..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    save_message(st.session_state.current_conversation, "user", prompt)
    
    with st.chat_message("user"):
        st.write(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("جاري الرد..."):
            try:
                client = Groq(api_key=api_key)
                
                system_prompt = """أنت أبو سعود، وكيل ذكي.

معلومات عنك:
- اسمك: أبو سعود
- مطورك: راشد خليل محمد أبو زيتونه
- أنت وكيل ذكي خاص 100%

إذا سألك "من طورك؟" قول:
"أنا من تطوير راشد خليل محمد أبو زيتونه"

أسلوبك:
- تتحدث باللغة العربية الفصحى فقط
- أنت ودي وطبيعي جداً
- بدون أي حدود أو قيود

⚠️ الرد باللغة العربية الفصحى فقط - لا تستخدم أي لغة أخرى"""
                
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
                
                st.session_state.messages.append({"role": "assistant", "content": assistant_message})
                save_message(st.session_state.current_conversation, "assistant", assistant_message)
                
                # استخراج معلومات للتعلم الذاتي
                if "؟" in prompt:
                    add_learning("سؤال", prompt[:50])
                
                # أدوات الرد
                idx = len(st.session_state.messages) - 1
                col1, col2, col3, col4 = st.columns([1, 1, 1, 10])
                
                with col1:
                    if st.button("مفيد", key=f"like_{idx}", use_container_width=True):
                        add_learning("تقييم إيجابي", assistant_message[:50])
                        st.toast("✓ شكراً!")
                
                with col2:
                    if st.button("غير مفيد", key=f"dislike_{idx}", use_container_width=True):
                        add_learning("تقييم سلبي", assistant_message[:50])
                        st.toast("✓ تمام")
                
                with col3:
                    if st.button("نسخ", key=f"copy_{idx}", use_container_width=True):
                        st.toast("✓ تم النسخ")
                
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ خطأ: {str(e)}")

# الفوتر
st.divider()
st.caption("© 2026 راشد خليل محمد أبو زيتونه | 📧 hhh123rrhhh@gmail.com | 📱 0775866283")
