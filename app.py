# Imports
from flask import Flask, render_template

# My App
app = Flask(__name__)


@app.route('/')
# Index
def index():
    return render_template("index.html")

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/employee_dashboard')
def employee_dashboard():
    return render_template('employee_dashboard.html')

@app.route('/boss_dashboard')
def boss_dashboard():
    return render_template('boss_dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)