import os
import json
import datetime
import random
import urllib.request
import base64
import io

# Gradio is not a standard library but is assumed for UI based on `app.py` context.
# If strictly "standard libraries" only (e.g., no external pip installs), a UI
# like this is not possible, and the Excel/plotting features would be severely limited.
try:
    import gradio as gr
except ImportError:
    print("Error: Gradio library not found. Please install it: pip install gradio")
    exit(1)

# pandas and matplotlib are also not standard libraries but are essential
# for Excel processing and plotting. The features will be disabled if not found.
try:
    import pandas as pd
    import matplotlib.pyplot as plt
    plt.switch_backend('Agg') # Use a non-interactive backend for server-side plotting
except ImportError:
    pd = None
    plt = None
    print("Warning: pandas and matplotlib not found. Excel and plotting features will be disabled.")
    print("Please install them for full functionality: pip install pandas openpyxl matplotlib")


# --- Global Variables ---
conversation_history = [] # Stores flat history: ["User: ...", "Ra'ad: ..."]

# GitHub Configuration - IMPORTANT: Update these placeholders
# For security, use environment variables for GITHUB_TOKEN.
GITHUB_REPO_OWNER = os.getenv("GITHUB_REPO_OWNER", "your_github_username")
GITHUB_REPO_NAME = os.getenv("GITHUB_REPO_NAME", "your_repo_name")
GITHUB_FILE_PATH = "chat_history.txt"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN") # Needs 'repo' scope personal access token

# --- Ra'ad's Personality and Knowledge Base ---
RAAD_PERSONALITY = "محلل استراتيجي" # Strategic Analyst
SECURITY_TIPS = [
    "منظوراً استراتيجياً، تأكد دائمًا من استخدام كلمات مرور قوية وفريدة لكل حساب.",
    "قم بتفعيل المصادقة متعددة العوامل (MFA) حيثما أمكن لطبقة أمان إضافية.",
    "احذر من رسائل التصيد الاحتيالي (Phishing) والروابط المشبوهة؛ التحليل النقدي ضروري.",
    "حافظ على تحديث برامجك بانتظام لسد الثغرات الأمنية المحتملة.",
    "قم بعمل نسخ احتياطية لبياناتك الهامة بشكل دوري للحفاظ على استمرارية العمل.",
    "استخدم برنامج مكافحة فيروسات وجدار حماية موثوق به كجزء من استراتيجيتك الدفاعية.",
    "تجنب شبكات الواي فاي العامة للتعاملات الحساسة؛ قد تشكل تهديدًا استراتيجياً لبياناتك.",
    "راجع إعدادات الخصوصية على وسائل التواصل الاجتماعي والمنصات الأخرى بانتظام.",
    "ثقف نفسك باستمرار حول التهديدات السيبرانية الشائعة لتكون مستعدًا استراتيجياً.",
    "راجع نشاط حساباتك بانتظام بحثًا عن أي علامات غير معتادة."
]

# --- GitHub API Interaction Functions (using urllib.request - standard library) ---

def _github_api_request(method, url, data=None, headers=None):
    if not GITHUB_TOKEN or GITHUB_REPO_OWNER == "your_github_username" or GITHUB_REPO_NAME == "your_repo_name":
        return {"error": "GitHub credentials not fully configured. Cannot perform GitHub operations."}

    _headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "Raad-Assistant" # Required by GitHub API
    }
    if headers:
        _headers.update(headers)

    req = urllib.request.Request(url, headers=_headers, method=method)
    post_data = None
    if data:
        req.add_header('Content-Type', 'application/json; charset=utf-8')
        post_data = json.dumps(data).encode('utf-8')
        req.add_header('Content-Length', len(post_data))

    try:
        with urllib.request.urlopen(req, data=post_data) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        error_details = e.read().decode('utf-8')
        return {"error": f"GitHub API error: {e.code} - {e.reason}", "details": error_details}
    except Exception as e:
        return {"error": f"An unexpected error occurred during GitHub API request: {e}"}

def load_chat_history_from_github():
    global conversation_history
    file_url = f"https://api.github.com/repos/{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}/contents/{GITHUB_FILE_PATH}"
    response = _github_api_request("GET", file_url)

    if "content" in response:
        decoded_content = base64.b64decode(response["content"]).decode('utf-8')
        conversation_history = [line.strip() for line in decoded_content.strip().split('\n') if line.strip()]
        # print("Chat history loaded from GitHub.") # For debugging
    elif response.get("error") and "Not Found" in response["error"]:
        print("Chat history file not found on GitHub. Starting fresh.")
        conversation_history = []
    elif response.get("error"):
        print(f"Error loading chat history from GitHub: {response['error']}")
        conversation_history = []
    return conversation_history

def save_chat_history_to_github():
    file_url = f"https://api.github.com/repos/{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}/contents/{GITHUB_FILE_PATH}"
    content = "\n".join(conversation_history)
    encoded_content = base64.b64encode(content.encode('utf-8')).decode('utf-8')

    # Get current file SHA to update it (required for PUT requests)
    response_get = _github_api_request("GET", file_url)
    sha = None
    if "sha" in response_get:
        sha = response_get["sha"]
    elif response_get.get("error") and "Not Found" in response_get["error"]:
        pass # File doesn't exist, will be created
    elif response_get.get("error"):
        print(f"Warning: Could not get SHA for existing file. {response_get.get('error', '')}")
        # Proceed without SHA, GitHub will return 409 if file exists and SHA is missing.

    data = {
        "message": f"Update chat history - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "content": encoded_content,
        "sha": sha
    }

    response_put = _github_api_request("PUT", file_url, data=data)

    if response_put and "content" in response_put:
        # print("Chat history saved to GitHub.") # For debugging
        pass
    elif response_put and response_put.get("error"):
        print(f"Error saving chat history to GitHub: {response_put['error']}")
    else:
        print("Failed to save chat history to GitHub due to an unexpected response.")

# --- Ra'ad's Core Logic (Personality and Response Generation) ---

def generate_strategic_response_text(user_input):
    """Generates Ra'ad's text response based on user input, reflecting his strategic analyst persona."""
    if "Excel" in user_input or "excel" in user_input or "مخططات" in user_input or "بيانات" in user_input:
        return "بصفتي محللاً استراتيجياً، أدرك أهمية البيانات. هل يمكنك تزويدي بملف Excel لكي أحلله وأقدم لك رؤى بيانية؟"
    elif "أمن" in user_input or "نصيحة" in user_input or "أمان" in user_input:
        tip = random.choice(SECURITY_TIPS)
        return f"من منظور أمني استراتيجي، أود أن أقدم لك نصيحة: {tip} هل هناك أي تحليل آخر يمكنني تقديمه لك؟"
    elif user_input.lower() in ["مرحباً", "hello", "السلام عليكم", ""]: # Handle greeting or empty input
        return f"أهلاً بك. بصفتي {RAAD_PERSONALITY}، أنا هنا لمساعدتك في تحليل البيانات وتقديم الرؤى الاستراتيجية. كيف يمكنني خدمتك اليوم؟"
    elif "تخزين" in user_input or "ذاكرة" in user_input or "GitHub" in user_input:
        return f"أنا مصمم لتخزين المحادثات بشكل دائم على GitHub لضمان استمرارية الذاكرة التشغيلية، تمامًا كما طلبت. هذا يعزز قدرتنا على تتبع التطورات الاستراتيجية."
    else:
        return f"بصفتي {RAAD_PERSONALITY}، أحلل طلبك من منظور استراتيجي. يمكنني معالجة البيانات، تقديم نصائح أمنية، وتوثيق محادثاتنا. ما هي أولويتك الحالية؟"

def get_daily_security_tip():
    """Provides a random security tip from the list."""
    return random.choice(SECURITY_TIPS)

# --- Excel Processing and Plotting ---

def process_excel_and_plot(file_path):
    """
    Reads an Excel file, performs basic analysis, and generates a plot if possible.
    Returns a message and a base64 encoded PNG image as HTML.
    """
    if pd is None or plt is None:
        return "لا يمكنني معالجة ملفات Excel أو رسم المخططات. لم يتم تثبيت المكتبات اللازمة (pandas, matplotlib).", None

    try:
        df = pd.read_excel(file_path)
        plot_image_data = None
        plot_message = f"تم قراءة بيانات Excel بنجاح. يحتوي الملف على {df.shape[0]} صفوف و {df.shape[1]} أعمدة. "

        numeric_cols = df.select_dtypes(include=['number']).columns
        if len(numeric_cols) >= 2:
            # Create a simple scatter plot for the first two numeric columns
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.scatter(df[numeric_cols[0]], df[numeric_cols[1]])
            ax.set_xlabel(numeric_cols[0], fontsize=12)
            ax.set_ylabel(numeric_cols[1], fontsize=12)
            ax.set_title(f'Scatter Plot: {numeric_cols[0]} vs {numeric_cols[1]}', fontsize=14)
            ax.grid(True, linestyle='--', alpha=0.7)
            plt.tight_layout()

            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            plot_image_data = base64.b64encode(buf.read()).decode('utf-8')
            plt.close(fig) # Close the figure to free memory

            plot_message += f"تم إنشاء مخطط بياني لعلاقة {numeric_cols[0]} بـ {numeric_cols[1]}. هل تريد تحليلًا أعمق؟"
        elif len(numeric_cols) == 1:
            # Create a histogram for a single numeric column
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.hist(df[numeric_cols[0]].dropna(), bins=10, edgecolor='black')
            ax.set_xlabel(numeric_cols[0], fontsize=12)
            ax.set_ylabel('التكرار', fontsize=12)
            ax.set_title(f'مخطط التكرار: {numeric_cols[0]}', fontsize=14)
            ax.grid(True, linestyle='--', alpha=0.7)
            plt.tight_layout()

            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            plot_image_data = base664.b64encode(buf.read()).decode('utf-8')
            plt.close(fig)

            plot_message += f"تم إنشاء مخطط بياني تكراري لـ {numeric_cols[0]}. هل تريد تحليلًا أعمق؟"
        else:
            plot_message += "لا توجد أعمدة رقمية كافية لرسم مخطط تلقائي. يرجى تحديد الأعمدة إذا كنت تريد مخططًا معينًا."

        return plot_message, f'<img src="data:image/png;base64,{plot_image_data}" alt="Generated Plot" style="max-width:100%; height:auto;">' if plot_image_data else None

    except Exception as e:
        return f"حدث خطأ أثناء معالجة ملف Excel: {e}", None

# --- Main Interaction Logic Function (as requested by "keep apply_direct_update") ---

def apply_direct_update(user_input, gradio_history_list, excel_file_path):
    """
    Processes user input, handles Excel uploads, generates Ra'ad's response,
    updates chat history, and saves to GitHub.
    """
    global conversation_history

    plot_html_output = None
    bot_response_text = ""
    user_input_for_history = user_input if user_input else "" # Capture user input, even if empty

    # 1. Handle Excel File Upload
    if excel_file_path is not None:
        excel_analysis_message, html_content = process_excel_and_plot(excel_file_path)
        bot_response_text = excel_analysis_message
        plot_html_output = html_content
        
        # Add to global conversation history
        if user_input_for_history: # If user provided text along with Excel
            conversation_history.append(f"User: {user_input_for_history}")
        conversation_history.append(f"Ra'ad (Excel Analysis): {bot_response_text}")

    # 2. Handle User Text Input (if no Excel was uploaded, or as a follow-up)
    elif user_input:
        conversation_history.append(f"User: {user_input_for_history}")
        bot_response_text = generate_strategic_response_text(user_input)
        conversation_history.append(f"Ra'ad: {bot_response_text}")
    
    # 3. Handle cases with no specific user input (e.g., initial load, or just hitting send/empty input)
    else: # user_input is empty and excel_file_path is None
        # Provide a default greeting/prompt if the chat is empty or no input was given
        if not gradio_history_list: # First interaction of the session
            bot_response_text = generate_strategic_response_text("") # Get initial greeting
            conversation_history.append(f"Ra'ad: {bot_response_text}")
        else:
            # If there's history but no new input, provide a generic prompt/greeting
            bot_response_text = generate_strategic_response_text("") # Generic response
            conversation_history.append(f"Ra'ad: {bot_response_text}")
            user_input_for_history = "" # No user input to display for this specific interaction

    # 4. Update Gradio's chat history list format
    # Append new interaction if there was any input or if it's the very first bot response.
    if user_input_for_history or bot_response_text:
        # If user_input was empty but Ra'ad responded (e.g., initial greeting), pass None for user message
        gradio_history_list.append([user_input_for_history if user_input_for_history else None, bot_response_text])

    # 5. Save conversation to GitHub for long-term memory
    save_chat_history_to_github()

    # Return values for Gradio UI components
    # gr.update(visible=...) dynamically shows/hides the plot area
    return gradio_history_list, "", plot_html_output, gr.update(visible=bool(plot_html_output))

# --- Initial Setup for Gradio ---
# Load chat history from GitHub at application startup
load_chat_history_from_github()

# Convert flat `conversation_history` to Gradio's `[[user, bot], ...]` format for initial display
initial_gradio_history = []
i = 0
while i < len(conversation_history):
    user_msg = None
    bot_msg = None
    if conversation_history[i].startswith("User: "):
        user_msg = conversation_history[i][len("User: "):]
        i += 1
    
    if i < len(conversation_history) and (conversation_history[i].startswith("Ra'ad: ") or conversation_history[i].startswith("Ra'ad (Excel Analysis): ")):
        bot_msg = conversation_history[i].split(': ', 1)[1] # Get text after first colon and space
        i += 1
    elif i < len(conversation_history) and conversation_history[i].startswith("System: "): # Also handle system messages as bot responses
        bot_msg = conversation_history[i][len("System: "):]
        i += 1

    if user_msg is not None or bot_msg is not None:
        initial_gradio_history.append([user_msg, bot_msg])
    # If a message doesn't fit the User/Ra'ad pattern, skip it to avoid infinite loops, or handle specifically.
    # For now, assuming alternating User/Ra'ad, or Ra'ad only for initial greeting.


# --- Gradio User Interface Definition ---
with gr.Blocks() as demo:
    gr.Markdown(f"## يا رعد: {RAAD_PERSONALITY}")
    gr.Markdown("أنا هنا لمساعدتك في تحليل البيانات وتقديم الرؤى الاستراتيجية. يمكنك التحدث معي، رفع ملفات Excel، أو طلب نصيحة أمنية.")

    chat_history_ui = gr.Chatbot(label="الدردشة مع رعد", value=initial_gradio_history, avatar_images=["https://i.imgur.com/4q3N1j4.png", "https://i.imgur.com/9n2n2n2.png"]) # Placeholder avatars
    user_input_ui = gr.Textbox(label="أدخل رسالتك هنا...", placeholder="كيف يمكنني تحليل بيانات المبيعات؟")
    excel_upload_ui = gr.File(label="ارفع ملف Excel هنا", file_types=[".xlsx", ".xls"], type="filepath")

    with gr.Row():
        send_button = gr.Button("إرسال", variant="primary")
        security_tip_button = gr.Button("نصيحة أمنية يومية")

    security_tip_output = gr.Textbox(label="نصيحة أمنية", interactive=False)
    excel_plot_display = gr.HTML(label="المخطط البياني", visible=False) # Initially hidden

    # Link UI components to the interaction logic
    send_button.click(
        fn=apply_direct_update,
        inputs=[user_input_ui, chat_history_ui, excel_upload_ui],
        outputs=[chat_history_ui, user_input_ui, excel_plot_display, excel_plot_display]
    )
    user_input_ui.submit( # Allow hitting enter to submit the message
        fn=apply_direct_update,
        inputs=[user_input_ui, chat_history_ui, excel_upload_ui],
        outputs=[chat_history_ui, user_input_ui, excel_plot_display, excel_plot_display]
    )

    security_tip_button.click(
        fn=get_daily_security_tip,
        inputs=[],
        outputs=[security_tip_output]
    )
    
    # Initial load behavior: Ra'ad gives a greeting if history is empty
    def initial_greeting_or_history(history_list):
        if not history_list:
            # If no history is loaded, generate an initial greeting from Ra'ad.
            # Use apply_direct_update with empty user_input to trigger initial bot response logic.
            # This function needs to return a list of lists like `gradio_history_list`.
            # For simplicity, we directly generate the response here.
            bot_response = generate_strategic_response_text("")
            conversation_history.append(f"Ra'ad: {bot_response}")
            save_chat_history_to_github()
            return [[None, bot_response]]
        return history_list

    demo.load(
        fn=initial_greeting_or_history,
        inputs=[chat_history_ui],
        outputs=[chat_history_ui]
    )

# --- Main Execution Block ---
if __name__ == "__main__":
    if not GITHUB_TOKEN:
        print("\n--- WARNING: GitHub Token Not Set ---")
        print("GitHub persistence (long-term memory) will not work.")
        print("Please set the GITHUB_TOKEN environment variable with a GitHub Personal Access Token")
        print("that has 'repo' scope. E.g., export GITHUB_TOKEN='ghp_YOUR_TOKEN'")
        print("Also ensure GITHUB_REPO_OWNER and GITHUB_REPO_NAME are updated in the script or via env vars.")
        print("------------------------------------\n")

    demo.launch()