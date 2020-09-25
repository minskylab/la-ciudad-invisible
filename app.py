from flask import Flask, render_template

app = Flask("la-ciudad-invisible")
app.config['SECRET_KEY'] = 'secret!'


@app.route('/')
def index():
    return render_template("index.html")
