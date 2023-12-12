# MTG_Set_Analysis

## Introduction

This project aims to compare Magic the Gathering standard sets over time, observing changes in the style and power of cards.  Magic the Gathering (MTG) was first released in August, 1993, and is still a popular trading card game today.  With over 30 years and over 25,000 cards printed to standard sets, the variability in games is massive and fascinating.  Within any long-running trading card game, there is a concept known as *power creep*[^1].  This is when new cards have to compete against old cards, both in gameplay and in marketability.  For new cards to sell as well as possible, they need to feel more powerful and desirable than the cards players already own, so the power level continutes to rise over the years.  Eventually, this can lead to games becoming unplayable and dying out.  

Mark Rosewater, the Head Designer for Magic since 2003[^2], made a comment in a 2013 interview[^3] about how he and his team are trying to address power creep: "Our development team has a process that I call the Escher Stairwell (named after a classic painting by the famous artist). Each set has things that go up in power while other things are brought down in power. This creates the illusion that the power is always going up because the focus is where we are pushing the power. This technique helps to create the illusion of the power increasing when, in fact, it actually stays pretty even."  Despite his comment and efforts, many players still believe power creep to be a real and genuine threat to the card game they love.

As such, I decided to attempt to look into it analytically.  The first stage of this project is looking at numerical and categorical card data, values that broker no argument as to their meaning or relevance.  These values are as follows:

  1. ***Converted Mana Cost (CMC)***: Mana is a resource produced by land cards that is used to play other cards and activate certain abilities.  The mana cost of a card includes the color(s) and value of mana required to play it.  CMC is the total value needed, disregarding color.  A common practice to judge the strength of a set is to look at the abilities and statistics of the cards with a CMC of 3.
  2. ***Color***: Most lands produce only one or two colors of mana, so most decks are also limited in which colors they play.  Each color and color pair support different play styles and have different synergies with each other.  Multicolor cards, colloquially known as 'gold cards,' are often the core of a deck, with other cards chosen to support and bolster those gold cards.
  3. ***Type***: Cards come in different categories, which each have their own rules for play.  The most common are as follows:
       - *Land*: Lands have no mana cost, and instead produce mana.  Only one land can be played a turn, unless there is a card in play that works around that rule.
       - *Creature*: Creatures are the most common card type in MTG.  These cards attack opponents and block opponents from attacking you.  Many also have additional abilities that will be included in this analysis in a later stage.
       - *Artifacts and Enchantments*: Artifacts and enchantments are cards that stay in play and have an effect (passive or activated) on players, cards, or the game state in general. These cards cannot attack or block.
       - *Instants*: Instants can be cast at any time, often in response to another action.  They do not remain in play, and their effect is short lived.
       - *Sorceries*:  Sorceries, like instants, have a short lived effect and do not remain in play.  Unlike instants, they can only be cast on your turn.
       - *Planeswalkers*: Planeswalkers are powerful commanders that can be targetted like a player.  They typically have two or three abilities, one of which can be activated on each of your turns.  These abilities affect a planeswalker's *loyalty*, either increasing or decreasing the loyalty.
  4. ***Supertype***: Supertypes are an additional descriptor added to the main card types, i.e. a _Legendary_ Creature.  The supertypes in MTG are: basic, legendary, snow, tribal, and world.  Snow, tribal, and world are limited in their use, but legendary cards are in nearly every set.  Legendary cards are typically more powerful, but a player can only have one copy in play at a time.  Basic applies only to lands, and refers to lands that produce a single color of mana with no additional abilities.
  5. ***Power***:  Power is the offensive capability of a creature card.  When a creature attacks, it deals damage equal to its power to a target planeswalker or player, or to a blocking creature used to defend the target.
  6. ***Toughness***: Toughness is the defensive capability of a creature card.  When a creature blocks or takes damage from another source, its toughness is reduced by that value until the end of the turn.  If the toughness is reduced to 0, the creature dies and is removed from play.
  7. ***Loyalty***: Loyalty is the value used by Planeswalkers.  Their abilities increase or decrease loyalty, and attacks against a planeswalker reduce its loyalty permanently.  If loyalty reaches 0, the planeswalker is removed from play.
  8. ***Rarity***:  Rarity indicates the frequency with which a card is printed, and is also a good way to approximate power level.  The rarities are common, uncommon, rare, and mythic rare.  Some older cards were printed at one rarity in their original set, and then reprinted or changed to a different rarity as card standards change and their effectiveness was seen in competitive play.

## Scraping the Data

I used Python's [Beautiful Soup](https://beautiful-soup-4.readthedocs.io/en/latest/) and [Splinter](https://splinter.readthedocs.io/en/stable/) libraries to scrape this data from [Scryfall](https://scryfall.com/sets), a website that indexes Magic cards.  I find Scryfall easy to navigate, with all the data I was looking for conveniently arranged.  In [set_scrape.py](set_scrape.py), I created two functions: `scrapeCardList` and `scrapeCards`.  `scrapeCardList` uses a link to a particular set, and scrapes the name, link, and release date of each card.  `scrapeCards` then uses the list of card links to collect the power, toughness, loyalty, mana cost, rarity, full card type, and text from each card.  Mana cost is expressed as {number}{color}{color}, so I was able to extract the CMC and the colors of each card within the `scrapeCards` function.  Loyalty and toughness were grouped together for convenience, as no card could have both and it prevented having a mostly empty Loyalty list.  The full card type was split into supertypes, types, and subtypes, which have not been used in this project but are simply subclassifications of creatures, such as dragon or wizard.

## Results

The final results of the scraping were exported to PostgreSQL using Python's Pandas library, and from Postgres were exported to an Excel file to be used with Tableau.  I used Tableau to analyze how these various card metrics have changed over time, the full results of which can be viewed through [Tableau Public here](https://public.tableau.com/app/profile/sjschmitt13/viz/MTG_Sets_Prelim/colorcountbyset), but I will review a few of the more interesting and relevant results below.

### Power and Toughness

Comparing the power and toughness of a 1 CMC creature to that of a 15 CMC creature is essentially meaningless, so many comparisons are made by looking at a single CMC value.  3 is the most common CMC value, so that is often what's used.  Here, for example, I compare the median and average powers and toughnesses of creatures over time. 



### Legendary Creatures

### Planeswalkers

### Color Distribution


[^1]: [MTG Wiki: Power Creep](https://mtg.fandom.com/wiki/Power_creep)
[^2]: [Mark Rosewater Wikipedia](https://en.wikipedia.org/wiki/Mark_Rosewater)
[^3]: [Mudrc (January 28, 2013) Interview with Mark Rosewater](http://www.mysticshop.cz/blog/interview-with-mark-rosewater/)
