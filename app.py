import streamlit as st
import google.generativeai as genai
import pandas as pd
import plotly.express as px
import io
import requests
import json
import random
import numpy as np # لفلترة الأعمدة الرقمية

# --- 1. إعدادات GitHub والمفاتيح السرية ---
# تأكد من إضافة GOOGLE_API_KEY, github_token, github_repo في .streamlit/secrets.toml
GITHUB_REPO = st.secrets["github_repo"]
GITHUB_TOKEN = st.secrets["github_token"]
CHAT_HISTORY_FILE = "chat_history.json" # اسم الملف الذي سيتم تخزين المحادثات فيه

# --- 2. وظائف GitHub للمزامنة ---

def update_file_on_github(repo, file_path, new_content, commit_message, token):
    """
    تحديث ملف على GitHub.
    repo: "username/repo_name"
    file_path: المسار إلى الملف داخل المستودع.
    new_content: المحتوى الجديد للملف (string).
    commit_message: رسالة الالتزام (commit message).
    token: GitHub Personal Access Token.
    """
    url = f"https://api.github.com/repos/{repo}/contents/{file_path}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    # الحصول على معلومات الملف الحالية (للحصول على SHA)
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        file_data = response.json()
        sha = file_data["sha"]
    elif response.status_code == 404:
        sha = None # الملف غير موجود، سيتم إنشاؤه
    else:
        st.error(f"GitHub API Error (read for update): {response.status_code} - {response.text}")
        return False

    # ترميز المحتوى الجديد إلى Base64
    import base64
    encoded_content = base64.b64encode(new_content.encode('utf-8')).decode('utf-8')

    data = {
        "message": commit_message,
        "content": encoded_content,
        "sha": sha # مطلوب لتحديث ملف موجود
    }

    # إرسال طلب PUT لتحديث/إنشاء الملف
    response = requests.put(url, headers=headers, json=data)
    if response.status_code in [200, 201]:
        return True
    else:
        st.error(f"GitHub API Error (write): {response.status_code} - {response.text}")
        return False

def read_file_from_github(repo, file_path, token):
    """
    قراءة محتوى ملف من GitHub.
    repo: "username/repo_name"
    file_path: المسار إلى الملف داخل المستودع.
    token: GitHub Personal Access Token.
    """
    url = f"https://api.github.com/repos/{repo}/contents/{file_path}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        file_data = response.json()
        import base64
        # فك ترميز المحتوى من Base64
        content = base64.b64decode(file_data["content"]).decode('utf-8')
        return content
    elif response.status_code == 404:
        return None # الملف غير موجود
    else:
        st.error(f"GitHub API Error (read): {response.status_code} - {response.text}")
        return None

# --- 3. إعداد نموذج Gemini ---
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# تحديد شخصية "رعد" - المحلل الاستراتيجي
persona_prompt = (
    "أنت 'رعد'، محلل استراتيجي ذكي وموضوعي، مهمتك هي تقديم تحليلات دقيقة، مخططات بيانية بناءً على البيانات، وتقديم نصائح أمنية قيمة. "
    "حافظ على لهجة مهنية ومباشرة. عندما تتحدث، استخدم دائمًا صيغة 'أيها القائد الاستراتيجي'."
)

# قائمة النصائح الأمنية
security_tips = [
    "استخدم كلمات مرور قوية وفريدة لكل حساب. فكّر في استخدام مدير كلمات المرور لتسهيل العملية.",
    "فعّل المصادقة الثنائية (2FA) على جميع حساباتك المهمة؛ إنها طبقة دفاع إضافية حيوية.",
    "كن حذرًا للغاية من رسائل البريد الإلكتروني والروابط المشبوهة (التصيد الاحتيالي)؛ تحقق دائمًا من المرسل قبل النقر.",
    "قم بتحديث برامجك وأنظمة التشغيل بانتظام لسد الثغرات الأمنية المعروفة.",
    "احتفظ بنسخ احتياطية من بياناتك المهمة في مكان آمن ومنفصل لحمايتها من الفقدان.",
    "لا تشارك معلوماتك الشخصية أو المالية أبدًا عبر وسائل التواصل الاجتماعي؛ فهي ليست منصة آمنة لذلك.",
    "استخدم شبكة VPN عند الاتصال بشبكات Wi-Fi عامة وغير موثوقة لحماية خصوصيتك وبياناتك.",
    "راجع أذونات التطبيقات قبل تثبيتها وفكر فيما إذا كانت تحتاج حقًا لتلك الصلاحيات للمهام المطلوبة.",
    "قم بتشفير أجهزتك المحمولة ومحركات الأقراص الصلبة لحماية بياناتك في حالة السرقة أو الفقدان.",
    "كن واعيًا للروابط المختصرة؛ قد تخفي وجهات ضارة. استخدم أدوات معاينة الروابط."
]

# --- 4. وظيفة الحصول على استجابة Gemini ---
def get_gemini_response(question, chat_session):
    try:
        response = chat_session.send_message(question, stream=True)
        return "".join([chunk.text for chunk in response])
    except Exception as e:
        st.error(f"حدث خطأ أثناء التواصل مع نموذج Gemini: {e}")
        return "عذرًا، واجهت مشكلة في الاتصال. يرجى المحاولة مرة أخرى."

# --- 5. واجهة المستخدم الرئيسية في Streamlit ---
def main():
    st.set_page_config(page_title="رعد - المحلل الاستراتيجي", layout="wide")

    st.title("⚡ رعد: المحلل الاستراتيجي الذكي 📊")
    st.markdown(
        """
        <style>
        .stButton>button {
            width: 100%;
            border-radius: 20px;
            border: 1px solid #4CAF50;
            color: #4CAF50;
        }
        .stButton>button:hover {
            background-color: #4CAF50;
            color: white;
        }
        .reportview-container .main .block-container{
            padding-top: 2rem;
            padding-right: 2rem;
            padding-left: 2rem;
            padding-bottom: 2rem;
        }
        </style>
        """, unsafe_allow_html=True
    )

    # --- 6. الذاكرة طويلة المدى (تحميل المحادثات) ---
    if "messages" not in st.session_state:
        st.session_state.messages = []
        try:
            history_content = read_file_from_github(GITHUB_REPO, CHAT_HISTORY_FILE, GITHUB_TOKEN)
            if history_content:
                st.session_state.messages = json.loads(history_content)
                st.info("تم تحميل سجل المحادثات بنجاح من GitHub، أيها القائد الاستراتيجي.")
            else:
                st.session_state.messages.append({"role": "assistant", "content": f"{persona_prompt.split('.')[0]}. أهلاً بك أيها القائد الاستراتيجي! كيف يمكنني تحليل البيانات أو تقديم نصيحة اليوم؟"})
        except json.JSONDecodeError:
            st.error("خطأ في قراءة سجل المحادثات من GitHub (تنسيق JSON غير صالح). سيتم بدء محادثة جديدة.")
            st.session_state.messages = [{"role": "assistant", "content": f"{persona_prompt.split('.')[0]}. أهلاً بك أيها القائد الاستراتيجي! كيف يمكنني تحليل البيانات أو تقديم نصيحة اليوم؟"}]
        except Exception as e:
            st.error(f"حدث خطأ أثناء تحميل سجل المحادثات من GitHub: {e}. سيتم بدء محادثة جديدة.")
            st.session_state.messages = [{"role": "assistant", "content": f"{persona_prompt.split('.')[0]}. أهلاً بك أيها القائد الاستراتيجي! كيف يمكنني تحليل البيانات أو تقديم نصيحة اليوم؟"}]

    # تهيئة نموذج الدردشة مع Persona
    if 'chat_session' not in st.session_state:
        model = genai.GenerativeModel('gemini-pro')
        # يمكن تمرير الـ persona كجزء من تاريخ الدردشة الأول إذا لم يكن هناك تاريخ محفوظ
        # أو يمكن تضمينه في كل استعلام
        # هنا سنضيفه كجزء من أول رسالة تلقائية
        st.session_state.chat_session = model.start_chat(history=[])


    # --- 7. تطوير الشخصية: نصيحة أمنية يومية وزر في الواجهة ---
    with st.sidebar:
        st.markdown("---")
        st.subheader("💡 نصيحة أمنية من رعد")
        if st.button("احصل على نصيحة أمنية"):
            st.info(random.choice(security_tips))
        st.markdown("---")

        # --- 8. تحليل البيانات: قراءة Excel وإنشاء مخططات ---
        st.header("📊 تحليل البيانات مع رعد")
        uploaded_file = st.file_uploader("حمّل ملف Excel (.xlsx) للتحليل", type=["xlsx"])

        if uploaded_file:
            try:
                df = pd.read_excel(uploaded_file)
                st.session_state['dataframe_to_analyze'] = df # تخزين DataFrame في session_state
                st.success("تم تحميل الملف بنجاح، أيها القائد الاستراتيجي! يمكننا الآن البدء في التحليل.")

                st.subheader("نظرة سريعة على البيانات:")
                st.dataframe(df.head())

                st.subheader("إنشاء مخطط بياني:")
                plot_type = st.selectbox("اختر نوع المخطط:", ["مخطط عمودي (Bar)", "مخطط خطي (Line)", "مخطط مبعثر (Scatter)", "مخطط تكراري (Histogram)"])

                numerical_cols = df.select_dtypes(include=np.number).columns.tolist()
                all_cols = df.columns.tolist()

                if not all_cols:
                    st.warning("الملف لا يحتوي على أعمدة للتحليل، أيها القائد الاستراتيجي.")
                else:
                    if plot_type == "مخطط تكراري (Histogram)":
                        if not numerical_cols:
                            st.warning("لا توجد أعمدة رقمية لإنشاء مخطط تكراري، أيها القائد الاستراتيجي.")
                        else:
                            hist_col = st.selectbox("اختر العمود للمخطط التكراري:", numerical_cols, key="hist_col")
                            if hist_col:
                                fig = px.histogram(df, x=hist_col, title=f"توزيع {hist_col} - تحليل رعد")
                                st.plotly_chart(fig)
                    else: # Bar, Line, Scatter
                        if not all_cols:
                            st.warning("لا توجد أعمدة في البيانات لإنشاء مخططات، أيها القائد الاستراتيجي.")
                        else:
                            x_col = st.selectbox("اختر محور X:", all_cols, key="x_col")
                            y_col = st.selectbox("اختر محور Y (يفضل عمود رقمي):", numerical_cols, key="y_col")

                            if x_col and y_col:
                                if plot_type == "مخطط عمودي (Bar)":
                                    fig = px.bar(df, x=x_col, y=y_col, title=f"مخطط عمودي: {x_col} مقابل {y_col} - تحليل رعد")
                                elif plot_type == "مخطط خطي (Line)":
                                    fig = px.line(df, x=x_col, y=y_col, title=f"مخطط خطي: {x_col} مقابل {y_col} - تحليل رعد")
                                elif plot_type == "مخطط مبعثر (Scatter)":
                                    fig = px.scatter(df, x=x_col, y=y_col, title=f"مخطط مبعثر: {x_col} مقابل {y_col} - تحليل رعد")
                                st.plotly_chart(fig)

            except Exception as e:
                st.error(f"حدث خطأ أثناء قراءة ملف Excel أو إنشاء المخطط: {e}. يرجى التأكد من أن الملف بصيغة صالحة.")
        st.markdown("---")

    # --- عرض سجل المحادثات ---
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # --- حقل إدخال الدردشة ---
    if prompt := st.chat_input("تفضل بطرح سؤالك أو طلب تحليل، أيها القائد الاستراتيجي..."):
        # إضافة رسالة المستخدم إلى سجل المحادثات
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("رعد يحلل ويستعد للرد..."):
                # تمرير Persona و المحادثات السابقة لـ Gemini
                # بما أننا نستخدم ChatSession، فإن التاريخ يدار تلقائيًا
                # ونضيف الـ persona_prompt كبداية لأي سؤال جديد
                full_prompt_with_persona = f"{persona_prompt}\n\nالسؤال: {prompt}"
                response = get_gemini_response(full_prompt_with_persona, st.session_state.chat_session)
                st.markdown(response)
        
        # إضافة رد Gemini إلى سجل المحادثات
        st.session_state.messages.append({"role": "assistant", "content": response})

        # --- 9. الذاكرة طويلة المدى (حفظ المحادثات) ---
        try:
            # حفظ المحادثات كـ JSON لتسهيل القراءة والكتابة
            history_to_save = json.dumps(st.session_state.messages, ensure_ascii=False, indent=2)
            update_file_on_github(GITHUB_REPO, CHAT_HISTORY_FILE, history_to_save, "Update chat history (Ra'ad)", GITHUB_TOKEN)
            # st.success("تم حفظ المحادثة بنجاح على GitHub.") # قد تكون مزعجة في كل مرة
        except Exception as e:
            st.error(f"فشل حفظ سجل المحادثات على GitHub: {e}")

if __name__ == "__main__":
    main()


**شرح التعديلات الرئيسية:**

1.  **`secrets.toml` و `requirements.txt`:** تم توضيح الإعدادات الضرورية لمفاتيح API و GitHub token والمكتبات المطلوبة.
2.  **وظائف GitHub (`read_file_from_github`, `update_file_on_github`):**
    *   تم توفير تنفيذ لهذه الوظائف باستخدام مكتبة `requests` للتعامل مع GitHub API.
    *   تقوم هذه الوظائف بقراءة وتحديث ملف `chat_history.json` في مستودع GitHub الخاص بك.
    *   يتم استخدام `base64` لترميز المحتوى وفك ترميزه لأن GitHub API يتعامل مع محتوى الملفات المشفرة بهذه الطريقة.
3.  **الذاكرة طويلة المدى (`CHAT_HISTORY_FILE`, تحميل/حفظ المحادثات):**
    *   عند بدء التطبيق، يحاول الكود قراءة `chat_history.json` من GitHub. إذا وجده، يقوم بتحميل المحادثات السابقة إلى `st.session_state.messages`.
    *   بعد كل تفاعل (سؤال المستخدم ورد رعد)، يتم تحديث `st.session_state.messages` ثم يتم حفظه مرة أخرى إلى `chat_history.json` على GitHub.
    *   تم استخدام `json.dumps` و `json.loads` لتخزين قائمة القواميس (`messages`) بشكل منظم.
4.  **تطوير الشخصية ("رعد" المحلل الاستراتيجي):**
    *   تم تعريف متغير `persona_prompt` يحدد أسلوب "رعد" وشخصيته.
    *   تم تعديل رسالة الترحيب الأولية لتعكس الشخصية الجديدة.
    *   يتم إلحاق `persona_prompt` بكل سؤال يرسل إلى نموذج Gemini لمساعدته في الحفاظ على الدور.
5.  **زر ونصيحة أمنية يومية:**
    *   تمت إضافة قسم في الشريط الجانبي (`st.sidebar`) يحتوي على زر "احصل على نصيحة أمنية".
    *   عند النقر عليه، يعرض التطبيق نصيحة أمنية عشوائية من قائمة `security_tips` محددة مسبقًا. يمكنك توسيع هذه القائمة أو جعل Gemini يولدها.
6.  **تحليل البيانات (Excel والمخططات):**
    *   تمت إضافة قسم "تحليل البيانات" في الشريط الجانبي.
    *   **`st.file_uploader`:** يتيح للمستخدمين تحميل ملفات Excel (`.xlsx`).
    *   **`pandas.read_excel`:** يقرأ الملف المحمل إلى DataFrame.
    *   **`st.dataframe`:** يعرض أول 5 صفوف من البيانات كنظرة عامة.
    *   **`plotly.express`:** يوفر أدوات سهلة الاستخدام لإنشاء مخططات تفاعلية.
        *   يمكن للمستخدمين اختيار نوع المخطط (عمودي، خطي، مبعثر، تكراري).
        *   يمكنهم تحديد الأعمدة لمحوري X و Y.
        *   يتم استخدام `df.select_dtypes(include=np.number)` لفلترة الأعمدة الرقمية لمحور Y والمخططات التكرارية.
7.  **`st.session_state`:** تم استخدامها لتخزين حالة التطبيق (مثل سجل المحادثات، و DataFrame المحمل) لضمان استمرار البيانات عبر إعادة تحميل Streamlit.
8.  **التعريب:** تم الحفاظ على الرسائل والواجهة باللغة العربية.
9.  **التحقق من الأخطاء:** تمت إضافة كتل `try-except` للتعامل مع الأخطاء المحتملة عند قراءة ملفات Excel أو التواصل مع GitHub أو Gemini.

الآن، عند نشر هذا التطبيق على Streamlit Cloud (أو تشغيله محليًا)، سيقوم "رعد" بتحميل سجل محادثاته من GitHub، وتقديم شخصيته كمحلل استراتيجي، والسماح لك بتحليل ملفات Excel وإنشاء المخططات، كل ذلك مع الحفاظ على ذاكرته طويلة المدى وتقديم نصائح أمنية قيمة.