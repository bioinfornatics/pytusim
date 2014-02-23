class Skill:

    skills   =  [   'antiair'   , 'armored' , 'augment' , 'berserk'     ,
                    'burst'     , 'counter' , 'crush'   , 'enfeeble'    ,
                    'flurry'    , 'heal'    , 'leech'   , 'legion'      ,
                    'pierce'    , 'poison'  , 'protect' , 'regenerate'  ,
                    'rally'     , 'siege'   , 'siphon'  , 'strike'      ,
                    'supply'    , 'weaken'  , 'valor' ]

    def __init__( self, name = "", value = "", isFactionRestricted = True, isApplyToAll = False ):
        self.name                 = name
        self.value                = value
        self.isFactionRestricted  = isFactionRestricted
        self.isApplyToAll         = isApplyToAll

    def dup( self ):
        return Skill( self.name, self.value, self.isFactionRestricted, self.isApplyToAll )
