```python
# app.py

from flask import Flask

app = Flask(__name__)

# تغيير عنوان الصفحة
app.config['PAGE_TITLE'] = 'نظام الرعد السيادي'

# تغيير لون الخلفية
@app.route('/')
def index():
    return '''
        <html>
            <head>
                <title>{}</title>
                <style>
                    body {{
                        background-color: #3f3d56; /* الإلغاء من الأزرق الداكن */
                    }}
                </style>
            </head>
            <body>
                <h1>حسناً في نظام الرعد السيادي</h1>
            </body>
        </html>
    '''.format(app.config['PAGE_TITLE'])

if __name__ == '__main__':
    app.run()
```
في هذه النسخة، تم تغيير عنوان الصفحة إلى "نظام الرعد السيادي" وتم تغيير لون الخلفية من الأزرق الداكن إلى #3f3d56.