# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

def scrapeCardList(setLink):
    browser.visit(setLink)
    # create empty lists
    # card names in set
    cardNames = []
    # link to more card details
    cardLinks = []

    # gather html from url
    html = browser.html
    setSoup = soup(html, 'html.parser')

    # scrape card names and links
    rows = setSoup.select('a.card-grid-item-card')
    for row in rows:
        cardNames.append(row.text.strip())
        cardLinks.append(row['href'])

    return cardNames, cardLinks

def scrapeCards(cardLinks, setAbbr):
    # create empty lists
    manaCosts = []
    cmc = []
    white = []
    blue = []
    black = []
    red = []
    green = []
    cardType = []
    subtype = []
    rarity = []
    power = []
    toughness = []
    cardSet = []

    for link in cardLinks:
        browser.visit(link)
        html=browser.html
        cardSoup = soup(html, 'html.parser')
        
        # mana cost
        manaRows = cardSoup.select('span.card-text-mana-cost abbr')
        manaCost=''
        for manaRow in manaRows:
            manaCost += manaRow.text
        manaCosts.append(manaCost)

        # converted mana cost (cmc)
        mc = manaCost.replace('{X}', '').replace('}{', ',').replace('{', '').replace('}', '').split(',')
        if mc[0].isdigit():
            cmc.append(int(mc[0]) + len(mc) - 1)
        else:
            cmc.append(len(mc))

        # colors
        white.append('1') if 'W' in manaCost else white.append('0')
        blue.append('1') if 'U' in manaCost else blue.append('0')
        black.append('1') if 'B' in manaCost else black.append('0')
        red.append('1') if 'R' in manaCost else red.append('0') 
        green.append('1') if 'G' in manaCost else green.append('0')
        
        # card type and subtype
        fullType = cardSoup.select('p.card-text-type-line')[0].text.strip().split(' — ')
        cardType.append(fullType[0])
        if len(fullType) == 1:
            subtype.append('')
        else:
            subtype.append(fullType[1])
        
        # rarity
        rarity.append(cardSoup.select('span.prints-current-set-details')[0].text.split(' · ')[1])
        
        # power and toughness (for creatures)
        statsRows = cardSoup.select('div.card-text-stats')
        if len(statsRows)==0:
            power.append('')
            toughness.append('')
        elif ':' in statsRows[0].text:
            power.append('')
            toughness.append(statsRows[0].text.strip().split(': ')[-1])
        else: 
            power.append(statsRows[0].text.strip().split('/')[0])
            toughness.append(statsRows[0].text.strip().split('/')[-1])
        
        # set
        cardSet.append(setAbbr)
    return manaCosts, cmc, cardType, subtype, rarity, power, toughness, cardSet, white, blue, black, red, green