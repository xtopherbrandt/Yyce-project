import enum

class ExtendedEnum(enum.Enum):

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))
    
class Genres(ExtendedEnum):
    Alternative = 'Alternative'
    Blues = 'Blues'
    Classical = 'Classical'
    Country = 'Country'
    Electronic = 'Electronic'
    Folk = 'Folk'
    Funk = 'Funk'
    HipHop = 'Hip-Hop'
    HeavyMetal = 'Heavy Metal'
    Instrumental = 'Instrumental'
    Jazz = 'Jazz'
    MusicalTheatre = 'Musical Theatre'
    Pop = 'Pop'
    Punk = 'Punk'
    RnB = 'R & B'
    Reggae = 'Reggae'
    RocknRoll = 'Rock n Roll'
    Soul = 'Soul'
    Other = 'Other'
    Western = 'Western'
    DeathMetal = 'Death Metal'
    