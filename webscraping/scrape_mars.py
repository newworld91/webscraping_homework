from bs4 import BeautifulSoup as bs
import requests
import selenium
from splinter import Browser
import tweepy
import pandas as pd


def scrape():
    key = 'CKXRMmr80OJe75cRaFdm5B7ZV'
    secret_key = 'WqnUVGsGAl9PAbcI0bui8zXVtG0IpTTyKsWw2IpBqhq1JiIBKs'

    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    link = 'https://mars.nasa.gov/news/'
    browser.visit(link)
    html = browser.html

    mars = {}

    soup = bs(html, 'html.parser')


    mars['title'] = soup.find("div", class_="content_title").find('a').text
    mars['paragraph'] = soup.find('div', class_="article_teaser_body").text

    image_url = 'https://www.jpl.nasa.gov/spaceimages/images/mediumsize/PIA18846_ip.jpg'
    browser.visit(image_url)
    html2 = browser.html
    soup2 = bs(html2, 'html.parser')
    img = soup2.find('img')
    mars['featured_image'] = img['src']

    auth = tweepy.OAuthHandler(key, secret_key)
    api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())
    target_user = "marswxreport"
    full_tweet = api.user_timeline(target_user, count=1)
    mars_weather = full_tweet[0]['text']
    mars['weather'] = mars_weather

    url3 = 'https://space-facts.com/mars/'
    browser.visit(url3)
    html3 = browser.html
    mars_df = pd.read_html(html3)
    mars_df = pd.DataFrame(mars_df[0])
    mars_df.columns = ['Mars', 'Data']
    mars_df = mars_df.set_index('Mars')
    mars_table = mars_df.to_html()
    mars['Mars_Facts'] = mars_table

    url4 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url4)
    html4 = browser.html
    soup3 = bs(html4, 'html.parser')
    img = soup3.find_all('img', class_='thumb')
    title2 = soup3.find_all('div', class_='description')
    list_mars = []
    for i in range(len(img)):
        partial = soup3.find_all("img", class_="thumb")
        img_title = soup3.find_all('h3')
        dictionary={"title":img_title[i].text,"img_url":'https://astrogeology.usgs.gov' +  partial[i]['src']}
        list_mars.append(dictionary)

    mars['title_img'] = list_mars

    browser.quit()
    return mars


if __name__ == '__main__':
    test = scrape()
    for i in range(5):
        print(test['title_img'][i])