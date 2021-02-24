from flask import Flask, render_template, request

app = Flask(__name__)

#Home page where user can recommend a movie
@app.route('/', methods=["POST", "GET"])
def home():
    return render_template("home.html")

#Second page where user can find recommendations made by other users
@app.route('/recommendations/')
def recommendations():
    return render_template("recommendations.html")

#On this page we thanks for the recommendation
@app.route('/thank you')
def thanks():
    return render_template("thanks.html")


if __name__ == "__main__":
    app.run(debug=True)