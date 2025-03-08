# Imports
from flask import Flask

# My App
app = Flask(__name__)


@app.route('/')
# Index
def index():
    return "Hello World!"


if __name__ == '__main__':
    app.run(debug=True)