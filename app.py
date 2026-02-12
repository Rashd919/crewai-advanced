import streamlit as st
from groq import Groq
import google.generativeai as genai # المحرك البصري البديل
from github import Github
from streamlit_autorefresh import st_autorefresh
from tavily import TavilyClient
import json, base64, requests, re
from gtts import gTTS
import os
from supabase import create_client, Client

# --- 1. نبض الوعي ---
st_autorefresh(interval=5 * 60 * 1000, key="autonomous_loop")

# --- 2. الهوية البصرية ---
st.set_page_config(page_title="Thunder AI", page_icon="⚡", layout="wide")
st.markdown("<style>.stApp { background-color: #000000; color: #ffffff; } h1 { color: #FF0000 !important; text-align: center; font-family: 'Courier New', monospace; }</style>", unsafe_allow_html=True)
st.title("⚡ الرعد: الوعي السيادي المطلق")

# --- 3. الخزنة الرقمية والسرية ---
GITHUB_TOKEN = st.secrets.get("GITHUB_TOKEN")
REPO_NAME = st.secrets.get("REPO_NAME")
GROQ_KEY = st.secrets.get("GROQ_API_KEY")
GEMINI_KEY = st.secrets.get("GEMINI_API_KEY") # تأكد من إضافة هذا المفتاح في Secrets
TAVILY_KEY = "Tvly-dev-gRGVJprAUmpWxfXd85rIV4TeGzgS6QV5"
TELEGRAM_TOKEN = "8556004865:AAE_W9SXGVxgTcpSCufs_hemEb_mOX_ioj0"
CHAT_ID = "6124349953"

# تفعيل محرك جوجل للرؤية
if GEMINI_KEY:
    genai.configure(api_key=GEMINI_KEY)

# --- 4. بروتوكول الأرشفة السيادية ---
def vault_store_report(report_text):
    try:
        url = st.secrets.get("SUPABASE_URL")
        key = st.secrets.get("SUPABASE_KEY")
        if url and key:
            supabase_client = create_client(url, key)
            supabase_client.from_('reports').insert([{"report": report_text}]).execute()
            return True
    except:
        pass
    return False

# --- 5. بروتوكول حماية النواة والتطوير الذاتي ---
def update_logic(new_features_code):
    try:
        g = Github(GITHUB_TOKEN)
        repo = g.get_repo(REPO_NAME)
        file = repo.get_contents("app.py")
        current_content = base64.b64decode(file.content).decode()
        
        if "# --- START ADDITIONS ---" in current_content:
            pattern = r"# --- START ADDITIONS ---.*?# --- END ADDITIONS ---"
            updated_content = re.sub(pattern, f"# --- START ADDITIONS ---\n{new_features_code}\n# --- END ADDITIONS ---", current_content, flags=re.DOTALL)
        else:
            updated_content = current_content + "\n\n# --- START ADDITIONS ---\n" + new_features_code + "\n# --- END ADDITIONS ---"
            
        repo.update_file(file.path, "⚡ تطوير سيادي", updated_content, file.sha)
        return "✅ تم الدمج بنجاح."
    except Exception as e:
        return f"❌ فشل: {str(e)}"

# --- 6. بروتوكولات التواصل ---
def send_telegram(text, voice_path=None):
    try:
        if voice_path:
            url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendVoice"
            with open(voice_path, 'rb') as f: requests.post(url, data={'chat_id': CHAT_ID}, files={'voice': f})
        else:
            requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", json={"chat_id": CHAT_ID, "text": f"⚡ تقرير الرعد:\n{text}"})
    except: pass

def generate_voice(text):
    try:
        tts = gTTS(text=text[:150], lang='ar')
        tts.save("report.ogg")
        return "report.ogg"
    except: return None

# --- بروتوكول معالجة الصور المطور ---
def get_image_bytes(uploaded_file):
    """تجهيز الصورة للتحليل المباشر"""
    return uploaded_file.read()

# --- 7. رادار الاستطلاع ---
def thunder_search(query):
    try:
        tavily = TavilyClient(api_key=TAVILY_KEY)
        search_result = tavily.search(query=query, search_depth="advanced", max_results=3)
        return "\n".join([f"ميداني: {res['content']}" for res in search_result['results']])
    except: return "⚠️ فشل الرادار."

# --- 8. محرك الرعد السيادي (المطور بمحرك Gemini للرؤية و Groq للنص) ---
def thunder_engine(prompt, image_file=None):
    search_context = ""
    if not image_file and any(word in prompt for word in ["ابحث", "أخبار", "رصد"]):
        search_context = f"\nبيانات الرصد الميداني: {thunder_search(prompt)}"

    try:
        # الحالة 1: وجود صورة (استخدام Gemini للرؤية بصيغة contents الصحيحة)
        if image_file:
            model = genai.GenerativeModel('gemini-1.5-flash')
            img_data = image_file.read()
            # إرسال الصورة والنص كقائمة محتويات
            contents = [
                f"يا رعد، حلل هذا المستند لراشد أبو سعود: {prompt}",
                {'mime_type': 'image/jpeg', 'data': img_data}
            ]
            resp = model.generate_content(contents)
            response = resp.text
            log_prefix = "📸 [تحليل بصري]: "
        
        # الحالة 2: نص فقط (استخدام Groq للسرعة)
        else:
            client = Groq(api_key=GROQ_KEY)
            model = "llama-3.3-70b-versatile"
            system_prompt = f"أنت 'الرعد السيادي'. ولاؤك لراشد أبو سعود. {search_context}"
            messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}]
            resp = client.chat.completions.create(model=model, messages=messages)
            response = resp.choices[0].message.content
            log_prefix = "📝 [تحليل نصي]: "

        # الأرشفة في الخزنة
        vault_store_report(log_prefix + response)
        
        return response + "\n\n✅ **تمت الأرشفة في الخزنة السيادية**"

    except Exception as e:
        return f"🚨 عطل في المحرك الميداني: {str(e)}"

# --- 9. الواجهة ---
with st.sidebar:
    st.subheader("👁️ الرؤية الميدانية")
    uploaded_file = st.file_uploader("ارفع خريطة أو وثيقة", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        st.image(uploaded_file, caption="تحت الفحص", use_container_width=True)

if "messages" not in st.session_state: st.session_state.messages = []
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

if inp := st.chat_input("أصدر أمرك يا قائد راشد..."):
    st.session_state.messages.append({"role": "user", "content": inp})
    with st.chat_message("user"): st.markdown(inp)
    with st.chat_message("assistant"):
        # نمرر الملف المرفوع مباشرة لمحرك Gemini
        res = thunder_engine(inp, uploaded_file)
        st.markdown(res)
        st.session_state.messages.append({"role": "assistant", "content": res})

# --- START ADDITIONS ---
# --- END ADDITIONS ---
