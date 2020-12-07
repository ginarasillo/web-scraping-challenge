from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import requests
import time


def scrape():
    # Opening headless chrome
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=True)

    # Get latest mars news
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    news_title = soup.findAll('div', class_='content_title')[1].text
    news_p = soup.find('div', class_='article_teaser_body').text

    # Get latest featured mars image
    images_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(images_url)
    # Sleep to wait page to fully load
    time.sleep(2)
    html_images = browser.html
    soup = BeautifulSoup(html_images, 'html.parser')
    featured_image_url = soup.find("section", class_='main_feature').find("article").find("footer").find("a")[
        "data-fancybox-href"]
    featured_image_full_url = f'https://www.jpl.nasa.gov{featured_image_url}'

    # Get latest mars report tweet
    weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)
    time.sleep(2)
    html_weather = browser.html
    mars_weather = ""
    soup = BeautifulSoup(html_weather, 'html.parser')
    latest_tweets = soup.find_all('article')
    for tweet in latest_tweets:
        if "Retweeted" not in tweet.text:
            spans = tweet.findAll("span")
            if len(spans) >= 4:
                mars_weather = spans[4].text
                break

    # Get facts table
    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)
    mars_data = pd.read_html(facts_url)
    mars_data = pd.DataFrame(mars_data[0])
    mars_facts = mars_data.to_html(header=False, index=False)

    # Get the hemispheres images
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)
    html_hemispheres = browser.html
    soup = BeautifulSoup(html_hemispheres, 'html.parser')
    items = soup.find_all('div', class_='item')
    hemisphere_image_urls = []
    hemispheres_main_url = 'https://astrogeology.usgs.gov'
    for item in items:
        title = item.find('h3').text
        partial_img_url = item.find('a', class_='itemLink product-item')['href']
        browser.visit(hemispheres_main_url + partial_img_url)
        partial_img_html = browser.html
        soup = BeautifulSoup(partial_img_html, 'html.parser')
        img_url = hemispheres_main_url + soup.find('img', class_='thumb')['src']
        hemisphere_image_urls.append({"title": title, "img_url": img_url})

    return {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_full_url,
        "mars_weather": mars_weather,
        "mars_facts": mars_facts,
        "hemisphere_images": hemisphere_image_urls
    }

