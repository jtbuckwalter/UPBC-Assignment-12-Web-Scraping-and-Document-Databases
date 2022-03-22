# Dependencies
from bs4 import BeautifulSoup
import requests
from flask_pymongo import PyMongo
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import pprint


def scrape():

    # urls to scrape
    jpl_url = 'https://spaceimages-mars.com'
    nasa_news_url = 'https://redplanetscience.com/'
    mars_facts_url = 'https://galaxyfacts-mars.com'


    # set up database
    # conn = 'mongodb://localhost:27017'
    # client = pymongo.MongoClient(conn)
    # db = client.mars_db
    # collection = db.info


    #set up browser and parser
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # set up collection
    mars_collection = {}

    # retrieve nasa news page
    browser.visit(nasa_news_url)
    time.sleep(1)
    html = browser.html
    soup = bs(html, 'html.parser')
    results = soup.find('section', class_='image_and_description_container')
    news_title = results.find_all('div', class_='content_title')[0].text
    news_description = results.find_all('div', class_='article_teaser_body')[0].text

    # add mars news to mars_collection
    mars_collection['news_title'] = news_title
    mars_collection['news_description'] = news_description


    # retrieve jpl featured image
    browser.visit(jpl_url)
    time.sleep(1)
    html = browser.html
    soup = bs(html, 'html.parser')
    image = soup.find('img', class_='headerimage')
    img_src = 'https://spaceimages-mars.com/' + image['src']

    # add featured image to mars_collection
    mars_collection['featured_image'] = img_src

    # retrieve mars facts
    tables = pd.read_html(mars_facts_url)
    df = tables[0]
    df.head()
    html_table = df.to_html(classes='table')

    # add mars facts table to mars_collection
    mars_collection['mars_facts'] = html_table

    # add mars hemisphere images to mars_collection
    mars_hemispheres = [
        {"hemisphere_title": "Valles Marineris Hemisphere", "img_url": "https://marshemispheres.com/images/valles_marineris_enhanced-full.jpg"},
        {"hemisphere_title": "Cerberus Hemisphere", "img_url": "https://marshemispheres.com/images/full.jpg"},
        {"hemisphere_title": "Schiaparelli Hemisphere", "img_url": "https://marshemispheres.com/images/schiaparelli_enhanced-full.jpg"},
        {"hemisphere_title": "Syrtis Major Hemisphere", "img_url": "https://marshemispheres.com/images/syrtis_major_enhanced-full.jpg"},
    ]
    mars_collection['mars_hemispheres'] = mars_hemispheres

    # add data to mongo_db
    # db.mars_info.insert_one(mars_collection)

    # quit browser
    browser.quit()

    # return results
    return mars_collection
