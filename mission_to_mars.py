from splinter import Browser
from bs4 import BeautifulSoup
import requests
import pandas as pd

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)


def mars():
    browser = init_browser()
    hemisphere_image_urls = []

    mars_news_url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"

    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

    mars_twitter_url = "https://twitter.com/marswxreport?lang=en"

    mars_facts_url = "https://space-facts.com/mars/"

    usgs_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    #"https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    response1 = requests.get(mars_news_url)
    # Create BeautifulSoup object; parse with 'html.parser'
    soup1 = BeautifulSoup(response1.text, 'html.parser')
    #get first news title and content paragraph
    news_p = soup1.find('div', class_="slide").div.text.strip()

    news_title = soup1.find('div', class_='content_title').a.text.strip()

    #"https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    response2 = requests.get(jpl_url)
    # Create BeautifulSoup object; parse with 'html.parser'
    soup2 = BeautifulSoup(response2.text, 'html.parser')

    featured_image_url = 'https://www.jpl.nasa.gov' + soup2.find('a', class_='button fancybox').get('data-fancybox-href')
        
    #"https://twitter.com/marswxreport?lang=en"
    response3 = requests.get(mars_twitter_url)
    # Create BeautifulSoup object; parse with 'html.parser'
    soup3 = BeautifulSoup(response3.text, 'html.parser')
    
    mars_weather = soup3.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text.rstrip()

    #"https://space-facts.com/mars/"
#     response4 = requests.get(mars_facts_url)
    # Create BeautifulSoup object; parse with 'html.parser'
#     soup4 = BeautifulSoup(response4.text, 'html.parser')

    data = pd.read_html(mars_facts_url)
    mars_df = pd.DataFrame(data[0])
    mars_facts = mars_df.to_html()

    #Soup is based on browser
    html = browser.html
    browser.visit(usgs_url)
    html = browser.html
    soup4 = BeautifulSoup(html, 'html.parser')
    links = soup4.find_all('div', class_='description')
    
    for link in links:
        
        html = browser.html
        soup4 = BeautifulSoup(html, 'html.parser')
        browser.visit('https://astrogeology.usgs.gov' +  link.a['href'])
        
        html = browser.html
        soup4 = BeautifulSoup(html, 'html.parser')
        hemisphere_image_urls.append({'title': link.h3.text, 
                                    'img_url': soup4.find('div', class_='downloads').ul.li.a['href']})
    
    browser.quit()

    mars_data = {"news_title": news_title,
            "news_p": news_p,
            "featured_image_url": featured_image_url,
            "mars_weather": mars_weather,
            "mars_facts": mars_facts,
            "hemisphere_image_urls": hemisphere_image_urls}
    return mars_data
