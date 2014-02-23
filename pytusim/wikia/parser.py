from bs4 import BeautifulSoup
import urllib.request
import re
from os import remove
from pytusim.engine.pool    import getPool
from pytusim.decorators     import retries
from pytusim.cards.card     import Card
from pytusim.cards.skill    import Skill

home    = "http://tyrantunleashed.wikia.com"
rarity  = [ "Common", "Rare", "Epic", "Legendary" ]

def factionParser( faction ):
    response    = urllib.request.urlopen( home + "/wiki/" + faction )
    html        = response.read()
    soup        = BeautifulSoup( html, "html.parser" )
    pattern     = re.compile( "^/wiki/" )
    div         = soup.find( lambda x : x.name == "div" and x.has_attr("id") and x["id"] == "mw-pages" )
    links       = [ link["href"] for link in div.find_all(lambda x : x.name == "a" and re.match( pattern, x["href"]) and x.has_key("title") and x.parent.name == "li")]
    cards       = [None] * len(links)
    for index, link in enumerate( links ):
        cards[index] = cardParser( link )
    #~ POOL        = getPool()
    #~ handle      = POOL.imap_unordered( cardParser, links )
    #~ POOL.close()
    #~ POOL.join()
    #~ cards       = list( handle )
    return cards

@retries(2, delay=1, exceptions=(Exception,))
def cardParser( name ):
    card        = Card()
    skills      = [ None, None, None ]
    data        = [ None, None, None, None, None]
    response    = urllib.request.urlopen( home + name )
    level       = 0
    pattern     = re.compile(r"(\w+)\s(\w+)?\s?(\w+)?\s?(\d+)")
    html        = response.read()
    soup        = BeautifulSoup( html )
    tables      = soup.find_all( "table", "article-table" )
    img         = img         = soup.find(
                                            lambda x :
                                                x.name            == "img"       and
                                                x.has_key("data-image-key") and
                                                x.parent.name     == "a"         and
                                                x.parent.has_key("class")        and
                                                x.parent["class"] == ["image"] 
                                            )
    card.image      = img["data-image-key"]
    card.image_url  = img["src"]
    metaTitle       = soup.head.find( 
                                        lambda x :
                                            x is not None           and
                                            x.name == "meta"        and
                                            x.has_attr("property")  and
                                            x["property"] == "og:title"
                                    )
    card.name       = metaTitle["content"]
    spanFuseRequirement = soup.find( "span", "mw-headline", id="Fusion_Requirements" )
    
    for tag in tables[0].find_all( "tr" ):
        if tag.th.get_text().startswith( "Type:" ) :
            card.type = tag.a.get_text()
        elif tag.th.get_text().startswith( "Rarity:" ) :
            card.rarity = tag.a.get_text()
        elif tag.th.get_text().startswith( "Faction:" ) :
            card.faction = tag.a.get_text()
        elif tag.th.get_text().startswith( "Set:" ) :
            card.cardSet = tag.a.get_text()

    data = ["Attack", "Health", "Delay", "Skills"]
    
    card.maxLevel = len( [ None for x in tables[1].find_all( lambda x:  x.th is not None and x.th.get_text().isdigit() ) ] )

    for tag in tables[1].find_all( "tr" )[2:]:
        
        if tag.th is not None:
            card.level = tag.th.get_text()
            for i, td in enumerate( tag.find_all( 'td' ) ):
                if  data[i] == "Attack":
                    card.attack[level] = td.get_text()
                elif  data[i] == "Health":
                    card.health[level] = td.get_text()
                elif  data[i] == "Delay":
                    card.delay[level] = td.get_text()
                else:
                    raise Exception( "Unsuported data type: " + data[i] )
                #print( '++', data[i+1], td.get_text() )
        else:
            for i, td in enumerate( tag.find_all( 'td' ) ):
                skill  = Skill()
                result = re.search( pattern, td.get_text() )
                if result is not None:
                    skill.name                  = result.group( 1 )
                    skill.value                 = result.group( 4 )
                    skill.isFactionRestricted   = ( result.group( 3 ) is not None and result.group( 3 ) in Card.factionEnum )
                    skill.isApplyToAll          = ( result.group( 2 ) is not None and result.group( 2 ) == "All" )
                    skills[ i ] = skill
                #print( '**', i, td.get_text() )
            card.skills[level] = skills[:]
            #print( level, len(cards) )
            level += 1
            skills  = [ None, None, None ]

    if spanFuseRequirement is not None:
        card_name   = ""
        text        = spanFuseRequirement.findNext( "p" ).text.strip().split()
        cardFused   = []
        quantifier  = re.compile( "x(\d+)" )
        for word in text:
            result = re.search( quantifier, word )
            if result is not None:
                cardFused += [card_name] * int(result.group( 1 ))
                card_name = ""
            elif word == "+":
                cardFused += [card_name]
                card_name = ""
            else:
                card_name += " " + word if card_name != "" else word

        if card_name != "":
            cardFused += [card_name]
    
    return card



@retries(2, delay=1, exceptions=(Exception,))
def save_card( factionDir, card ):
    card_pickle = join(factionDir, card.name ) + ".pickle"
    card_image  = join(factionDir, card.image)
    if args.verbosity > 1:
        print( "  - {}".format( card.name ) )
    if not exists( card_image ):
        #~ request.urlretrieve( card.image_url, card_image )
        fp = request.urlopen( card.image_url )
        with open( card_image, "wb") as fo:
            fo.write(fp.read())
    with open( card_pickle, "wb" ) as f:
        dump( card, f, HIGHEST_PROTOCOL )

@retries(2, delay=1, exceptions=(Exception,))
def update_card( factionDir, card ):
    remote_card         = cardParser( card.name.replace( ' ', '_') )
    card_image          = join(factionDir, card.image)
    remote_card_image   = join(factionDir, card.image)
    if remote_card != card:
        save_card( factionDir, remote_card )
        card = remote_card
    if remote_card_image != card_image:
        remove( card_image )
    return 
