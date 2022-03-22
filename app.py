from flask import Flask, render_template, redirect, jsonify
from flask_pymongo import PyMongo
import pymongo
import scrape_mars

# Use flask_pymongo to set up mongo connection
app = Flask(__name__)
# mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")


# Setup connection to mongodb
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

# Select database and collection to use
db = client.mars_db
collection = db.mars_info

# root route
@app.route("/")
def home():

    # Find one record of data from the mongo database
    mars_info = collection.find_one()

    # Return template and data
    return render_template("index.html", content = mars_info)



@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_collection = scrape_mars.scrape()

    # Insert the record
    collection.insert_one(mars_collection)

    # Redirect back to home page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
