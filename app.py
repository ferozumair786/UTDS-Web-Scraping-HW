from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import mission_to_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
# app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
# mongo = PyMongo(app)

# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/craigslist_app")
mongo = PyMongo(app, uri="mongodb://ferozumair786:***Canidium786@ds155596.mlab.com:55596/heroku_6501q5h6")


@app.route("/")
def index():
    data = mongo.db.collection.find_one()
    if data is None:
        return render_template("index.html")
    else: 
        return render_template("index.html", data=data)


@app.route("/scrape")
def scraper():
    # data = mongo.db.data.find()
    mars_data = mission_to_mars.mars()
    mongo.db.collection.update({}, mars_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
