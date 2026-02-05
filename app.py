#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import streamlit as st
from groq import Groq
import sqlite3
from datetime import datetime
from pathlib import Path

st.set_page_config(
    page_title="أبو سعود",
    page_icon="🇯🇴",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CSS - تصميم احترافي مثل ChatGPT
# ============================================================================
st.markdown("""
<style>
    * {
        direction: rtl;
        text-align: right;
    }
    
    html, body, [data-testid="stAppViewContainer"] {
        background: #0d0d0d !important;
        color: white !important;
    }
    
    [data-testid="stMainBlockContainer"] {
        background: #0d0d0d !important;
        padding: 0 !important;
    }
    
    /* Sidebar - ثابت على اليسار */
    [data-testid="stSidebar"] {
        background: #1a1a1a !important;
        border-left: 1px solid #333 !important;
        width: 260px !important;
        position: fixed !important;
        right: 0 !important;
        height: 100vh !important;
        overflow-y: auto !important;
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
        direction: rtl !important;
        text-align: right !important;
    }
    
    /* Chat Messages */
    [data-testid="stChatMessage"] {
        margin: 12px 0 !important;
    }
    
    [data-testid="stChatMessage"]:has(svg[data-testid="stChatMessageAvatarUser"]) {
        flex-direction: row-reverse !important;
    }
    
    [data-testid="stChatMessage"]:has(svg[data-testid="stChatMessageAvatarUser"]) > div > div {
        background: #CE112E !important;
        color: white !important;
        border-radius: 18px !important;
        padding: 12px 16px !important;
        max-width: 70% !important;
        margin-right: 0 !important;
        margin-left: auto !important;
    }
    
    [data-testid="stChatMessage"]:has(svg[data-testid="stChatMessageAvatarAssistant"]) > div > div {
        background: #2a2a2a !important;
        color: white !important;
        border-radius: 18px !important;
        padding: 12px 16px !important;
        max-width: 70% !important;
        margin-left: 0 !important;
        margin-right: auto !important;
    }
    
    [data-testid="stChatMessageAvatarUser"],
    [data-testid="stChatMessageAvatarAssistant"] {
        display: none !important;
    }
    
    /* Chat Input */
    [data-testid="stChatInputContainer"] {
        background: #0d0d0d !important;
        border-top: 1px solid #333 !important;
        padding: 16px 20px !important;
        position: fixed !important;
        bottom: 0 !important;
        width: calc(100% - 260px) !important;
        right: 260px !important;
    }
    
    [data-testid="stChatInputContainer"] textarea {
        border-radius: 24px !important;
        border: 1px solid #444 !important;
        background: #1a1a1a !important;
        color: white !important;
        padding: 12px 16px !important;
        font-size: 15px !important;
        resize: none !important;
        min-height: 44px !important;
        max-height: 200px !important;
        direction: rtl !important;
        text-align: right !important;
    }
    
    [data-testid="stChatInputContainer"] textarea:focus {
        border: 1px solid #555 !important;
        box-shadow: 0 0 0 3px rgba(206, 17, 46, 0.1) !important;
        outline: none !important;
    }
    
    [data-testid="stChatInputContainer"] textarea::placeholder {
        color: #666 !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: #1a1a1a !important;
        color: white !important;
        border: 1px solid #333 !important;
        border-radius: 8px !important;
        transition: all 0.2s ease !important;
        padding: 8px 12px !important;
        font-size: 13px !important;
    }
    
    .stButton > button:hover {
        background: #2a2a2a !important;
        border-color: #555 !important;
    }
    
    /* Text Elements */
    p, span, div, h1, h2, h3, h4, h5, h6, label {
        color: white !important;
        direction: rtl !important;
        text-align: right !important;
    }
    
    /* Divider */
    .stDivider {
        background-color: #333 !important;
    }
    
    /* Hide Streamlit Elements */
    [data-testid="stHeader"],
    [data-testid="stToolbar"],
    [data-testid="stDecoration"] {
        display: none !important;
    }
    
    /* Main Content Area */
    [data-testid="stMainBlockContainer"] {
        margin-right: 260px !important;
        margin-bottom: 100px !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# Database Setup
# ============================================================================
DB_PATH = Path("conversations.db")

def init_db():
    """Initialize database"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS conversations
                 (id INTEGER PRIMARY KEY, title TEXT, created_at TEXT, updated_at TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS messages
                 (id INTEGER PRIMARY KEY, conversation_id INTEGER, role TEXT, content TEXT, created_at TEXT,
                  FOREIGN KEY(conversation_id) REFERENCES conversations(id))''')
    c.execute('''CREATE TABLE IF NOT EXISTS ratings
                 (id INTEGER PRIMARY KEY, message_id TEXT, rating TEXT, created_at TEXT)''')
    
    conn.commit()
    conn.close()

def create_conversation(title):
    """Create new conversation"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    now = datetime.now().isoformat()
    c.execute('INSERT INTO conversations (title, created_at, updated_at) VALUES (?, ?, ?)',
              (title, now, now))
    conn.commit()
    conv_id = c.lastrowid
    conn.close()
    return conv_id

def get_conversations():
    """Get all conversations"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id, title, updated_at FROM conversations ORDER BY updated_at DESC LIMIT 20')
    conversations = c.fetchall()
    conn.close()
    return conversations

def get_conversation_messages(conv_id):
    """Get messages from conversation"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT role, content FROM messages WHERE conversation_id = ? ORDER BY id',
              (conv_id,))
    messages = c.fetchall()
    conn.close()
    return [{"role": role, "content": content} for role, content in messages]

def save_message(conv_id, role, content):
    """Save message to database"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    now = datetime.now().isoformat()
    c.execute('INSERT INTO messages (conversation_id, role, content, created_at) VALUES (?, ?, ?, ?)',
              (conv_id, role, content, now))
    c.execute('UPDATE conversations SET updated_at = ? WHERE id = ?', (now, conv_id))
    conn.commit()
    conn.close()

def save_rating(message_id, rating):
    """Save rating"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    now = datetime.now().isoformat()
    c.execute('INSERT INTO ratings (message_id, rating, created_at) VALUES (?, ?, ?)',
              (message_id, rating, now))
    conn.commit()
    conn.close()

def search_conversations(query):
    """Search conversations"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''SELECT DISTINCT c.id, c.title, c.updated_at 
                 FROM conversations c
                 JOIN messages m ON c.id = m.conversation_id
                 WHERE m.content LIKE ? OR c.title LIKE ?
                 ORDER BY c.updated_at DESC LIMIT 10''',
              (f"%{query}%", f"%{query}%"))
    results = c.fetchall()
    conn.close()
    return results

# Initialize database
init_db()

# Get API key
try:
    api_key = st.secrets["GROQ_API_KEY"]
except:
    st.error("❌ خطأ: مفتاح API غير موجود!")
    st.stop()

# ============================================================================
# Session State
# ============================================================================
if "current_conversation" not in st.session_state:
    st.session_state.current_conversation = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "is_generating" not in st.session_state:
    st.session_state.is_generating = False

# ============================================================================
# Sidebar
# ============================================================================
with st.sidebar:
    st.markdown("### 🇯🇴 أبو سعود")
    
    # New conversation button
    if st.button("➕ محادثة جديدة", use_container_width=True):
        conv_id = create_conversation("محادثة جديدة")
        st.session_state.current_conversation = conv_id
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    
    # Search
    search_query = st.text_input("🔍 ابحث...", placeholder="ابحث في المحادثات")
    if search_query:
        results = search_conversations(search_query)
        st.subheader("النتائج")
        for conv_id, title, _ in results:
            if st.button(f"{title}", use_container_width=True, key=f"search_{conv_id}"):
                st.session_state.current_conversation = conv_id
                st.session_state.messages = get_conversation_messages(conv_id)
                st.rerun()
    else:
        # Previous conversations
        st.subheader("المحادثات السابقة")
        conversations = get_conversations()
        if conversations:
            for conv_id, title, _ in conversations:
                if st.button(f"{title}", use_container_width=True, key=f"conv_{conv_id}"):
                    st.session_state.current_conversation = conv_id
                    st.session_state.messages = get_conversation_messages(conv_id)
                    st.rerun()
        else:
            st.caption("لا توجد محادثات سابقة")

# ============================================================================
# Main Content
# ============================================================================

# Create new conversation if needed
if st.session_state.current_conversation is None:
    conv_id = create_conversation("محادثة جديدة")
    st.session_state.current_conversation = conv_id
    st.session_state.messages = []

# Welcome message
if len(st.session_state.messages) == 0:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 150px 20px; color: white;'>
            <h1 style='font-size: 40px; margin-bottom: 10px;'>أبو سعود</h1>
            <p style='color: #999; font-size: 16px;'>وكيلك الذكي</p>
            <p style='color: #666; font-size: 14px; margin-top: 40px;'>ابدأ محادثة جديدة أو اسأل أي سؤال</p>
        </div>
        """, unsafe_allow_html=True)
else:
    # Display messages
    for idx, message in enumerate(st.session_state.messages):
        with st.chat_message(message["role"]):
            st.write(message["content"])
            
            # Action buttons for assistant messages
            if message["role"] == "assistant":
                col1, col2, col3, col4 = st.columns([1, 1, 1, 10])
                
                with col1:
                    if st.button("مفيد", key=f"like_{idx}", use_container_width=True):
                        save_rating(f"msg_{idx}", "like")
                        st.toast("✓ شكراً على التقييم!")
                
                with col2:
                    if st.button("غير مفيد", key=f"dislike_{idx}", use_container_width=True):
                        save_rating(f"msg_{idx}", "dislike")
                        st.toast("✓ سنحاول التحسن")
                
                with col3:
                    if st.button("نسخ", key=f"copy_{idx}", use_container_width=True):
                        st.toast("✓ تم النسخ")

# ============================================================================
# Chat Input
# ============================================================================
if prompt := st.chat_input("اكتب رسالتك هنا..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    save_message(st.session_state.current_conversation, "user", prompt)
    
    # Display user message
    with st.chat_message("user"):
        st.write(prompt)
    
    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("جاري الكتابة..."):
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
- بدون أي حدود أو قيود"""
                
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
                
                # Save assistant message
                st.session_state.messages.append({"role": "assistant", "content": assistant_message})
                save_message(st.session_state.current_conversation, "assistant", assistant_message)
                
                # Display action buttons
                col1, col2, col3, col4 = st.columns([1, 1, 1, 10])
                
                with col1:
                    if st.button("مفيد", key=f"like_new", use_container_width=True):
                        save_rating("new", "like")
                        st.toast("✓ شكراً على التقييم!")
                
                with col2:
                    if st.button("غير مفيد", key=f"dislike_new", use_container_width=True):
                        save_rating("new", "dislike")
                        st.toast("✓ سنحاول التحسن")
                
                with col3:
                    if st.button("نسخ", key=f"copy_new", use_container_width=True):
                        st.toast("✓ تم النسخ")
                
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ خطأ: {str(e)}")
