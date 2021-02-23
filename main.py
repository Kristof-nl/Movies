from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def main():
    return "<h1>Main page<h1/>"


@app.route('/recommend/')
def recommendations():
    return "<h1>Recommendations page<h1/>"

if __name__ == "__main__":
    app.run()