# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

def set_scrape(set_link):
    browser.visit(set_link)
    # create empty lists
    # card names in set
    card_names = []
    # link to more card details
    card_links = []

    # gather html from url
    html = browser.html
    deck_soup = soup(html, 'html.parser')

    # scrape card names and links
    rows = deck_soup.select('a.card-grid-item-card')
    for row in rows:
        card_names.append(row.text.strip())
        card_links.append(row['href'])

    return card_names, card_links