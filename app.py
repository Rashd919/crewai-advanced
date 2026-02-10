:


from flask import Flask, render_template

app = Flask(__name__)

# التعديل على عنوان الصفحة
@app.route('/')
def index():
    return render_template('base.html', title='نظام الرعد السيادي')

# التعديل على الشريط الجانبي
@app.context_processor
def side_bar():
    return dict(maintainer='المطور: راشد أبو سعود')

if __name__ == '__main__':
    app.run(debug=True)