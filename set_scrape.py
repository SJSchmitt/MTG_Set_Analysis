# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager

# import pandas
import pandas as pd

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# function to scrape a list of all cards in set and links to those cards
def scrapeCardList(setLink):
    browser.visit(setLink)
    # create empty lists
    # card names in set
    cardNames = []
    # link to more card details
    cardLinks = []
    releaseDate = []

    # gather html from url
    html = browser.html
    setSoup = soup(html, 'html.parser')

    # get the release date
    dateRows = setSoup.select('p.set-header-title-subline')
    release = dateRows[0].text.split('\xa0')[-1].strip()

    # scrape card names and links
    rows = setSoup.select('a.card-grid-item-card')
    for row in rows:
        cardNames.append(row.text.strip())
        cardLinks.append(row['href'])
        releaseDate.append(release)

    return cardNames, cardLinks, releaseDate

# function to scrape further card details
# mana costs, cmc, colors, card type, subtype, and supertype, rarity, power, and toughness
def scrapeCards(cardLinks, setAbbr):
    # create empty lists
    manaCosts = []
    cmc = []
    white = []
    blue = []
    black = []
    red = []
    green = []
    superType = []
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
        
        # card type, subtype, and supertype
        fullType = cardSoup.select('p.card-text-type-line')[0].text.strip()
        super = ''
        if 'Snow ' in fullType:
            super += 'Snow '
            fullType = fullType.replace('Snow ', '')
        if 'Legendary ' in fullType:
            super += 'Legendary '
            fullType = fullType.replace('Legendary ', '')
        if 'Ongoing ' in fullType:
            super += 'Ongoing '
            fullType = fullType.replace('Ongoing ', '')
        if 'Snow ' in fullType:
            super += 'Snow '
            fullType = fullType.replace('Snow ', '')
        if 'World ' in fullType: 
            super += 'World'
            fullType = fullType.replace('World ', '')
        superType.append(super)

        mainType = fullType.split(' — ')
        cardType.append(mainType[0])
        if len(mainType) == 1:
            subtype.append('')
        else:
            subtype.append(mainType[1])
        
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
    return manaCosts, cmc, superType, cardType, subtype, rarity, power, toughness, cardSet, white, blue, black, red, green

def setScrape(setAbbr):
    setLink = "https://scryfall.com/sets/" + setAbbr
    # scrape card names and links for the set
    names, cardLinks, release = scrapeCardList(setLink)
    # scrape card details
    manaCosts, cmc, superType, cardType, subtype, rarity, power, toughness, cardSet, white, blue, black, red, green = scrapeCards(cardLinks, setAbbr)
    df = pd.DataFrame({'Card': names, 'Set': cardSet, 'Release': release, 'Supertype': superType, 'Type': cardType, 'Subtype': subtype, 'Mana_Cost': manaCosts, 
                    'CMC': cmc, 'Power': power, 'Toughness': toughness, 'Rarity': rarity, 
                   'White': white, 'Blue': blue, 'Black': black, 'Red': red, 'Green': green, 'Link': cardLinks})
    
    newDf = df.drop_duplicates(subset=['Card'])
    return newDf

