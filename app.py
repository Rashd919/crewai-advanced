
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html lang="ar">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>حصن راشد الرقمي</title>
        <style>
            body {
                background-color: #0A1931; /* لون كحلي داكن */
                color: #FFFFFF; /* نص أبيض ليتناسق مع الخلفية الداكنة */
                font-family: Arial, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                margin: 0;
                font-size: 2em;
                text-align: center;
            }
        </style>
    </head>
    <body>
        <h1>أهلاً بك يا راشد في حصنك الرقمي</h1>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(debug=True)
