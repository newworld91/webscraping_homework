from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import scrape_mars
from scrape_mars import scrape


app = Flask(__name__,template_folder='/Users/stevenovis/Desktop/webscraping')
app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"


mongo = PyMongo(app)

@app.route("/")
def index():
    try:
        mars = mongo.db.mars.find_one()
    except:
        mars = {}

    print("mars mongo pull:")
    print(mars)
    return render_template("index.html", mars = mars)


@app.route("/scrape")
def scraperoute():
    mars = mongo.db.mars
    mars_data = scrape()
    mars_dict = \
    {
        "title": mars_data["title"],
        "paragraph": mars_data["paragraph"],
        "featured_image": mars_data["featured_image"],
        "weather": mars_data["weather"],
        "mars_facts": mars_data["Mars_Facts"],
        "title_img": mars_data["title_img"]
    }
    print("Mars dict:")
    print(mars_dict)
    mars.insert_one(mars_dict)

    return redirect("http://localhost:5000/", code=302)



if __name__ == '__main__':
    app.run(debug=True)