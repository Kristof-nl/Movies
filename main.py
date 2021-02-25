from flask import Flask, render_template, request
from pymongo import MongoClient

app = Flask(__name__)

#Create a MongoDB datebase
client = MongoClient("mongodb+srv://Krzysztof_nl:Kukuczka303@cluster0.dsf4q.mongodb.net/test")
app.db = client.Movies

#Home page where user can recommend a movie
@app.route('/', methods=["POST", "GET"])
def home():
    if request.method == "POST":
        movie = request.form.get("title")
        app.db.movie.insert({"movie title": movie})
        return render_template("thanks.html")
    else:
        return render_template("home.html")

#Second page where user can find recommendations made by other users
@app.route('/recommendations/')
def recommendations():
    print([i for i in app.db.movie.find({})])
    return render_template("recommendations.html")

#On this page we thanks for the recommendation
@app.route('/thanks')
def thanks():
    return render_template("thanks.html")


if __name__ == "__main__":
    app.run(debug=True)