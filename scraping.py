from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt

def scrape_all():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome',**executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    data = {
      "news_title": news_title,
      "news_paragraph": news_paragraph,
      "featured_image": featured_image(browser),
      "facts": mars_facts(),
      "last_modified": dt.datetime.now()}

    # Stop webdriver and return data
    browser.quit()
    return data

def mars_news(browser):
    # Image News from NASA Website
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    browser.is_element_present_by_css('ul.item_list li.slide', wait_time=1)

    html=browser.html
    news_soup = soup(html,'html.parser')

    try:
        slide_elem = news_soup.select_one('ul.item_list li.slide')

        news_title = slide_elem.find('div', class_='content_title').get_text()

        news_p = slide_elem.find('div', class_ = 'article_teaser_body').get_text()
    except AttributeError:
        return None, None

    return news_title, news_p

def featured_image(browser):
    # Image Scraping from NASA Website
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    #Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()

    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_element = browser.links.find_by_partial_text('more info')
    more_info_element.click()


    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    try:
        img_url_rel = img_soup.select_one('figure.lede a img').get('src')
        img_url = f'https://www.jpl.nasa.gov/{img_url_rel}'
    except AttributeError:
        return None

    return img_url
def mars_facts():


    # Get facts from a third site
    url ='https://space-facts.com/mars/'
    # browser.visit(url)
    try:

        df = pd.read_html(url)[0]
        
    except BaseException:
        return None
    
    df.columns=['description', 'value']
    df.set_index('description', inplace=True)
    
    return df.to_html(classes="table table-striped")

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all()) 


