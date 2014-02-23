class Card:
    costList    = [ 5, 15, 30, 75, 150, 300 ]
    factionEnum = [ "Imperial", "Raider", "Xeno", "Bloodthirsty", "Righteous", "Progenitor" ]
    rarityEnum  = [ "Common", "Rare", "Epic", "Legendary" ]
    
    def __init__( self ):
        self.name         = ""
        self.type         = ""
        self.rarity       = ""
        self.faction      = ""
        self.cardSet      = ""
        self.image        = ""
        self.image_url    = ""
        self.maxLevel     = 0
        self.currentLevel = 0
        self.cardFused    = []
        self.attack       = [ None, None, None, None, None, None ]
        self.health       = [ None, None, None, None, None, None ]
        self.delay        = [ None, None, None, None, None, None ]
        self.skills       = [ None, None, None, None, None, None ]
    
    def __eq__(self, other): 
        return self.__dict__ == other.__dict__
    
    def get_cost( self ):
        cost = sum( Card.costList[ 0 : currentLevel ] )
        if cardFused is not None:
            self.cost += sum( [ x.get_cost() for x in cardFused ] )
    
    def dup( self ):
        card = Card()
        card.name         = self.name
        card.type         = self.type
        card.rarity       = self.rarity
        card.faction      = self.faction
        card.cardSet      = self.cardSet
        card.cardFused    = self.cardFused
        card.image        = self.image
        card.image_url    = self.image_url
        card.maxLevel     = self.maxLevel
        card.currentLevel = self.currentLevel
        card.attack       = self.attack
        card.health       = self.health
        card.delay        = self.delay
        card.skills       = self.skills
        return card
