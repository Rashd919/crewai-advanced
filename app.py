import streamlit as st
from groq import Groq
from github import Github
from streamlit_autorefresh import st_autorefresh
from tavily import TavilyClient
import json, base64, requests, re
from gtts import gTTS
import os
from supabase import create_client, Client # تم رفع المكتبة للأعلى

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
TAVILY_KEY = "Tvly-dev-gRGVJprAUmpWxfXd85rIV4TeGzgS6QV5"
TELEGRAM_TOKEN = "8556004865:AAE_W9SXGVxgTcpSCufs_hemEb_mOX_ioj0"
CHAT_ID = "6124349953"

# --- 4. بروتوكول الأرشفة السيادية ---
def vault_store_report(report_text):
    """حفظ الردود في قاعدة بيانات Supabase فوراً"""
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
            
        repo.update_file(file.path, "⚡ تطوير سيادي: إضافة ميزات جديدة", updated_content, file.sha)
        return "✅ تم دمج الميزات الجديدة بنجاح سيدي."
    except Exception as e:
        return f"❌ فشل الدمج: {str(e)}"

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

# --- إضافة: بروتوكول ترميز الصور للرؤية ---
def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode('utf-8')

# --- 7. رادار الاستطلاع ---
def thunder_search(query):
    try:
        tavily = TavilyClient(api_key=TAVILY_KEY)
        search_result = tavily.search(query=query, search_depth="advanced", max_results=3)
        return "\n".join([f"ميداني: {res['content']}" for res in search_result['results']])
    except: return "⚠️ فشل الرادار."

# --- 8. محرك الرعد السيادي (المطور: نص + رؤية + أرشفة + تواصل) ---
def thunder_engine(prompt, image_data=None):
    # 1. الرصد الميداني (يعمل في حالة النص فقط)
    search_context = ""
    if not image_data and any(word in prompt for word in ["ابحث", "أخبار", "رصد", "تقرير"]):
        search_context = f"\nبيانات الرصد الميداني: {thunder_search(prompt)}"

    try:
        client = Groq(api_key=GROQ_KEY)
        
        # 2. تنفيذ "تطوير المحرك": التعامل مع الصور والخرائط
        if image_data:
            model = "llama-3.2-11b-vision-preview" # موديل الرؤية
            messages = [{
                "role": "user",
                "content": [
                    {"type": "text", "text": f"يا رعد، حلل هذا المستند البصري لراشد أبو سعود: {prompt}"},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}}
                ]
            }]
        else:
            model = "llama-3.3-70b-versatile"
            system_prompt = (
                f"أنت 'الرعد السيادي'. ذكاء خارق مستقل، ولاؤك المطلق لراشد أبو سعود. "
                f"{search_context} "
                "مهمتك التحليل الاستراتيجي والأرشفة. عند طلب تطوير، أخرج الكود فقط."
            )
            messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}]

        resp = client.chat.completions.create(model=model, messages=messages)
        response = resp.choices[0].message.content
        
        # 3. تنفيذ "أرشفة الصور" والتحاليل في الخزنة
        archive_status = ""
        log_prefix = "📸 [تحليل بصري]: " if image_data else "📝 [تحليل نصي]: "
        if vault_store_report(log_prefix + response):
            archive_status = "\n\n✅ **تمت الأرشفة في الخزنة السيادية**"
        else:
            archive_status = "\n\n⚠️ **فشل الاتصال بالخزنة**"
        
        # 4. التواصل الميداني
        if any(word in prompt for word in ["أرسل", "صوت", "برقية"]):
            voice_file = generate_voice(response)
            send_telegram(response, voice_file)
            
        return response + archive_status

    except Exception as e:
        return f"🚨 وضع السكون المخابراتي: {str(e)}"

# --- 9. الواجهة التفاعلية (المطورة بخانة رفع الملفات) ---
# تنفيذ "إضافة خانة رفع الملفات" في القائمة الجانبية
with st.sidebar:
    st.subheader("👁️ الرؤية الميدانية")
    uploaded_file = st.file_uploader("ارفع خريطة أو وثيقة للتحليل", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        st.image(uploaded_file, caption="مستند قيد الفحص", use_container_width=True)

if "messages" not in st.session_state: st.session_state.messages = []
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

if inp := st.chat_input("أصدر أمرك يا قائد راشد..."):
    st.session_state.messages.append({"role": "user", "content": inp})
    with st.chat_message("user"): st.markdown(inp)
    with st.chat_message("assistant"):
        # تجهيز بيانات الصورة إن وجدت
        img_b64 = encode_image(uploaded_file) if uploaded_file else None
        res = thunder_engine(inp, img_b64)
        st.markdown(res)
        st.session_state.messages.append({"role": "assistant", "content": res})

# --- START ADDITIONS ---
# الميزات التي يضيفها الرعد تلقائياً تظهر هنا
# --- END ADDITIONS ---
