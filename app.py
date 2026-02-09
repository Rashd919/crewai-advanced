أنا الرعد! هدير! أمرك مطاع! سأغير الخلفية مع الحفاظ على صندوق الكتابة واضحًا وظاهرًا دائمًا في الأسفل. إليك كود بايثون الكامل لملف `app.py` باستخدام Flask:

هذا التطبيق سيقوم بما يلي:
1.  يعرض خلفية داكنة تتغير بين عدة حالات (عاصفة، سماء ليلية، غضب) عند طلبك.
2.  يحتفظ بصندوق إدخال الدردشة (chat_input) مثبتًا في أسفل الشاشة، مع خلفية داكنة شفافة لضمان وضوحه على أي خلفية.
3.  يُظهر تأثير اهتزاز خفيف (rumble) ليتناسب مع شخصية الرعد.

**لتحضير وتشغيل التطبيق:**

1.  **ثبت Flask:**
    bash
    pip install Flask
    
2.  **احفظ الكود:** احفظ الكود التالي في ملف باسم `app.py`.
3.  **شغل التطبيق:** افتح محطة الأوامر (Terminal) في نفس مجلد الملف ونفذ الأمر:
    bash
    python app.py
    
4.  **افتح المتصفح:** اذهب إلى العنوان الذي يظهر في Terminal (عادةً `http://127.0.0.1:5000/`).

**الآن، يمكنك التحدث إلى الرعد! جرب كتابة "غير الخلفية" أو "Change background" في صندوق الكتابة.**


# app.py
from flask import Flask, render_template_string, request

app = Flask(__name__)

# قائمة بحالات الخلفية المختلفة (لون الخلفية، لون النص)
# يتم التبديل بينها عند طلب التغيير
background_states = [
    {"bg_color": "#2c3e50", "text_color": "#ecf0f1", "name": "ليلة عاصفة"}, # أزرق داكن
    {"bg_color": "#4a235a", "text_color": "#fdebd0", "name": "سديم غامض"},   # أرجواني داكن
    {"bg_color": "#560000", "text_color": "#f5b7b1", "name": "غضب ناري"},     # أحمر داكن
    {"bg_color": "#0a192f", "text_color": "#a8b2d1", "name": "محيط عميق"},    # أزرق داكن جداً
    {"bg_color": "#1c002b", "text_color": "#e0bbff", "name": "فراغ كوني"}      # أرجواني أغمق
]
current_background_index = 0

@app.route('/', methods=['GET', 'POST'])
def thunder_app():
    global current_background_index # للإشارة إلى أننا سنعدل المتغير العام

    response_message = "أنا الرعد! أحدث هديرًا في السماء، وأجلب البرق والنور! ماذا تطلب مني؟"

    if request.method == 'POST':
        user_message = request.form.get('message', '').lower()

        if "غير الخلفية" in user_message or "change background" in user_message:
            current_background_index = (current_background_index + 1) % len(background_states)
            new_state = background_states[current_background_index]
            response_message = f"هدير! غيرت الخلفية إلى '{new_state['name']}'. هل هناك شيء آخر؟"
        else:
            response_message = f"هدير! رسالتك '{user_message}' وصلتني. لكن طلبي هو تغيير الخلفية فقط في الوقت الحالي."

    # تجهيز نمط الخلفية الحالي للعرض
    current_state = background_states[current_background_index]
    background_style = f"background-color: {current_state['bg_color']}; --text-color: {current_state['text_color']}; color: var(--text-color);"

    # قالب HTML مدمج مباشرة في بايثون
    html_template = """
    <!DOCTYPE html>
    <html lang="ar">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>الرعد - Thunder</title>
        <style>
            body {
                margin: 0;
                padding-bottom: 70px; /* لتوفير مساحة لصندوق الإدخال الثابت في الأسفل */
                font-family: 'Arial', sans-serif;
                display: flex;
                flex-direction: column;
                min-height: 100vh;
                {{ background_style | safe }}; /* النمط الديناميكي للخلفية، يستخدم 'safe' للسماح بـ CSS الخام */
                transition: background-color 0.8s ease-in-out, color 0.8s ease-in-out; /* انتقال سلس بين الخلفيات */
            }

            .thunder-display {
                flex-grow: 1; /* لجعل هذا العنصر يأخذ كل المساحة المتاحة */
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                text-align: center;
                padding: 20px;
                color: var(--text-color); /* استخدام متغير CSS للتحكم بلون النص بناءً على الخلفية */
            }

            h1 {
                font-size: 3em;
                margin-bottom: 20px;
                animation: rumble 1s infinite alternate; /* تأثير اهتزاز خفيف */
                color: inherit; /* ليرث اللون من العنصر الأب (body's --text-color) */
            }

            p {
                font-size: 1.2em;
                max-width: 600px;
                line-height: 1.6;
                color: inherit; /* ليرث اللون من العنصر الأب (body's --text-color) */
            }

            .chat-input-container {
                position: fixed; /* لتثبيت صندوق الإدخال في مكانه */
                bottom: 0;
                left: 0;
                right: 0;
                background-color: rgba(0, 0, 0, 0.8); /* خلفية داكنة وشفافة لضمان الوضوح */
                padding: 15px;
                border-top: 1px solid #444;
                box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.5);
                display: flex;
                justify-content: center;
                z-index: 1000; /* لضمان ظهوره فوق أي عناصر أخرى */
            }

            .chat-input-container form {
                display: flex;
                width: 100%;
                max-width: 800px;
            }

            .chat-input-container input[type="text"] {
                flex-grow: 1; /* ليأخذ كل المساحة المتاحة */
                padding: 12px 15px;
                border: 1px solid #555;
                border-radius: 25px;
                background-color: #333; /* خلفية داكنة لصندوق الكتابة */
                color: #f0f0f0; /* لون نص فاتح وواضح */
                font-size: 1.1em;
                margin-right: 10px;
                outline: none;
                box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.3);
            }

            .chat-input-container input[type="text"]::placeholder {
                color: #bbb; /* لون تلميح النص */
            }

            .chat-input-container button {
                padding: 12px 25px;
                background-color: #3498db; /* لون زر مميز */
                color: white;
                border: none;
                border-radius: 25px;
                cursor: pointer;
                font-size: 1.1em;
                font-weight: bold;
                transition: background-color 0.3s ease;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
            }

            .chat-input-container button:hover {
                background-color: #2980b9;
            }

            /* تأثير اهتزاز خفيف ليتناسب مع شخصية الرعد */
            @keyframes rumble {
                0% { transform: translateX(0px); }
                25% { transform: translateX(-2px) rotate(-0.5deg); }
                50% { transform: translateX(2px) rotate(0.5deg); }
                75% { transform: translateX(-1px) rotate(-0.2deg); }
                100% { transform: translateX(0px); }
            }
        </style>
    </head>
    <body>
        <div class="thunder-display">
            <h1>{{ response_message }}</h1>
        </div>

        <div class="chat-input-container">
            <form method="POST">
                <input type="text" name="message" placeholder="أخبرني بطلبك يا إنسان..." required>
                <button type="submit">أرسل</button>
            </form>
        </div>
    </body>
    </html>
    """
    return render_template_string(html_template, background_style=background_style, response_message=response_message)

if __name__ == '__main__':
    app.run(debug=True)
