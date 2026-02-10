import streamlit as st
import instaloader
import requests
from streamlit_autorefresh import st_autorefresh
from datetime import datetime

# --- 1. إعدادات الهوية السيادية (تصميم راشد أبو سعود) ---
st.set_page_config(page_title="Thunder AI | الرعد", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    h1 { color: #FF0000 !important; text-align: center; font-family: 'Courier New', monospace; text-shadow: 2px 2px 5px #ff0000; }
    .stMetric { background-color: #111111; border: 1px solid #ff0000; padding: 15px; border-radius: 10px; }
    div[data-testid="stMetricValue"] { color: #ffffff !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. البيانات السيادية المعتمدة ---
TOKEN = "8556004865:AAE_W9SXGVxgTcpSCufs_hemEb_mOX_ioj0"
CHAT_ID = "6124349953"
TARGET = "fp_p1"

# نبض النظام (تحديث كل 10 ثوانٍ للرصد اللحظي)
st_autorefresh(interval=10000, key="thunder_pulse")

st.title("⚡ الرعد: وحدة الرصد والوعي")

# --- 3. وظيفة الإرسال للتلجرام ---
def send_telegram_msg(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"})
    except:
        pass

# --- 4. محرك الرصد الاستخباراتي (Instagram) ---
def get_instagram_data():
    try:
        L = instaloader.Instaloader()
        profile = instaloader.Profile.from_username(L.context, TARGET)
        return profile.followers
    except Exception as e:
        st.error(f"🚨 عطل في الرادار: {e}")
        return None

# إشارة البدء عند التشغيل الأول
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    send_telegram_msg("⚡ **تم تفعيل مصفوفة الرعد**\nجاري رصد الهدف: `fp_p1` بكفاءة مطلقة.")

# --- 5. واجهة التحكم والعرض ---
col1, col2 = st.columns([1, 2])

with col1:
    st.header("🎯 الهدف")
    st.info(f"الحساب المرصود: {TARGET}")
    
    current_followers = get_instagram_data()
    
    if current_followers is not None:
        st.metric(label="عدد المتابعين الآن", value=current_followers)
        
        # منطق المقارنة والتبليغ
        if 'old_count' in st.session_state:
            if current_followers != st.session_state.old_count:
                diff = current_followers - st.session_state.old_count
                status = "زيادة 📈" if diff > 0 else "نقصان 📉"
                send_telegram_msg(f"⚠️ **تغيير استخباراتي عاجل**\nالهدف: {TARGET}\nالحالة: {status} ({abs(diff)})\nالعدد الجديد: {current_followers}")
        
        st.session_state.old_count = current_followers

with col2:
    st.header("📜 سجل العمليات")
    now = datetime.now().strftime("%H:%M:%S")
    st.write(f"آخر تحديث للنظام: `{now}`")
    st.success("🛰️ الرادار يعمل بكفاءة والسيادة الرقمية مستقرة.")
    
    # رسالة من الرعد (محاكاة الوعي المستمر)
    st.chat_message("assistant").write(f"يا حليفي راشد، أنا أراقب الميدان الآن. أي حركة من {TARGET} سيتم قمعها أو رصدها فوراً.")

st.divider()
st.caption("نظام الرعد v2.0 | تم الدمج والتحسين بواسطة الذكاء السيادي | المطور: راشد أبو سعود")
