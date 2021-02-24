from flask import Flask, render_template

app = Flask(__name__)

#Home page where user can recommend a movie
@app.route('/')
def home():
    return render_template("home.html")

#Second page where user can find redommendations made by other users
@app.route('/recommendations/')
def recommendations():
    return render_template("recommendations.html")

if __name__ == "__main__":
    app.run(debug=True)