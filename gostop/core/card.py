from .utils import _


class Card(object):
    def __init__(self, name, month, group, order_in_month=0):
        self.name = name
        self.month = month
        self.group = group
        self.order_in_month = order_in_month

    def __repr__(self):
        return "{__class__.__name__}(name='{name}', month={month}, group={group})" \
            .format(__class__=self.__class__, **self.__dict__)

    def __str__(self):
        return self.name

    def __eq__(self, other):
        if other is None:
            return False
        elif isinstance(other, self.__class__):
            return self.month == other.month and \
                   self.group == other.group
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, self.__class__):
            return self.group < other.group
        return NotImplemented

    def __hash__(self):
        return hash(self.month) ^ hash(self.group)


class Month(object):
    JAN = 1
    FEB = 2
    MAR = 3
    APR = 4
    MAY = 5
    JUN = 6
    JUL = 7
    AUG = 8
    SEP = 9
    OCT = 10
    NOV = 11
    DEC = 12


class Group(object):
    BRIGHT = 1
    ANIMAL = 2
    RIBBON = 3
    JUNK = 4
    JUNK_2 = 5


CRANE = Card(_(u'Pine and Crane'), Month.JAN, Group.BRIGHT, 0)
PINE_RED_POEM = Card(_(u'Pine and Red Poem Ribbon'), Month.JAN, Group.RIBBON, 1)
PINE = Card(_(u'Pine'), Month.JAN, Group.JUNK, 2)

BUSH_WARBLER = Card(_(u'Plum Blossom and Bush Warbler'), Month.FEB, Group.ANIMAL, 0)
PLUM_RED_POEM = Card(_(u'Plum Blossom and Red Poem Ribbon'), Month.FEB, Group.RIBBON, 1)
PLUM = Card(_(u'Plum Blossom'), Month.FEB, Group.JUNK, 2)

CURTAIN = Card(_(u'Cherry Blossom and Curtain'), Month.MAR, Group.BRIGHT, 0)
CHERRY_RED_POEM = Card(_(u'Cherry Blossom and Red Poem Ribbon'), Month.MAR, Group.RIBBON, 1)
CHERRY = Card(_(u'Cherry Blossom'), Month.MAR, Group.JUNK, 2)

CUCKOO = Card(_(u'Wisteria and Cuckoo'), Month.APR, Group.ANIMAL, 0)
WISTERIA_RED = Card(_(u'Wisteria and Red Ribbon'), Month.APR, Group.RIBBON, 1)
WISTERIA = Card(_(u'Wisteria'), Month.APR, Group.JUNK, 2)

BRIDGE = Card(_(u'Iris and Bridge'), Month.MAY, Group.ANIMAL, 0)
IRIS_RED = Card(_(u'Iris and Red Ribbon'), Month.MAY, Group.RIBBON, 1)
IRIS = Card(_(u'Iris'), Month.MAY, Group.JUNK, 2)

BUTTERFLY = Card(_(u'Peony and Butterfly'), Month.JUN, Group.ANIMAL, 0)
PEONY_BLUE_POEM = Card(_(u'Peony and Blue Poem Ribbon'), Month.JUN, Group.RIBBON, 1)
PEONY = Card(_(u'Peony'), Month.JUN, Group.JUNK, 2)

BOAR = Card(_(u'Bush Clover and Boar'), Month.JUL, Group.ANIMAL, 0)
BUSH_CLOVER_RED = Card(_(u'Bush Clover and Red Ribbon'), Month.JUL, Group.RIBBON, 1)
BUSH_CLOVER = Card(_(u'Bush Clover'), Month.JUL, Group.JUNK, 2)

MOON = Card(_(u'Pampas Grass and Moon'), Month.AUG, Group.BRIGHT, 0)
GEESE = Card(_(u'Pampas Grass and Geese'), Month.AUG, Group.ANIMAL, 1)
PAMPAS_GRASS = Card(_(u'Pampas Grass'), Month.AUG, Group.JUNK, 2)

CUP = Card(_(u'Chrysanthemum and Cup'), Month.SEP, (Group.ANIMAL, Group.JUNK_2), 0)
CHRYSANTHEMUM_BLUE_PEOM = Card(_(u'Chrysanthemum and Blue Poem Ribbon'), Month.SEP, Group.RIBBON, 1)
CHRYSANTHEMUM = Card(_(u'Chrysanthemum'), Month.SEP, Group.JUNK, 2)

DEER = Card(_(u'Maple and Deer'), Month.OCT, Group.ANIMAL, 0)
MAPLE_BLUE_POEM = Card(_(u'Maple and Blue Poem Ribbon'), Month.OCT, Group.RIBBON, 1)
MAPLE = Card(_(u'Maple'), Month.OCT, Group.JUNK, 2)

PHOENIX = Card(_(u'Paulownia and Phoenix'), Month.NOV, Group.BRIGHT, 0)
PAULOWNIA = Card(_(u'Paulownia'), Month.NOV, Group.JUNK, 1)
PAULOWNIA_2 = Card(_(u'Paulownia 2'), Month.NOV, Group.JUNK_2, 2)

RAIN = Card(_(u'Willow and Rain'), Month.DEC, Group.BRIGHT, 0)
SWALLOW = Card(_(u'Willow and Swallow'), Month.DEC, Group.ANIMAL, 1)
WILLOW_RED = Card(_(u'Willow and Red Ribbon'), Month.DEC, Group.RIBBON, 2)
WILLOW_2 = Card(_(u'Willow'), Month.DEC, Group.JUNK_2, 3)


ALL_CARDS = (
    CRANE, PINE_RED_POEM, PINE, PINE,
    BUSH_WARBLER, PLUM_RED_POEM, PLUM, PLUM,
    CURTAIN, CHERRY_RED_POEM, CHERRY, CHERRY,
    CUCKOO, WISTERIA_RED, WISTERIA, WISTERIA,
    BRIDGE, IRIS_RED, IRIS, IRIS,
    BUTTERFLY, PEONY_BLUE_POEM, PEONY, PEONY,
    BOAR, BUSH_CLOVER_RED, BUSH_CLOVER, BUSH_CLOVER,
    MOON, GEESE, PAMPAS_GRASS, PAMPAS_GRASS,
    CUP, CHRYSANTHEMUM_BLUE_PEOM, CHRYSANTHEMUM, CHRYSANTHEMUM,
    DEER, MAPLE_BLUE_POEM, MAPLE, MAPLE,
    PHOENIX, PAULOWNIA_2, PAULOWNIA, PAULOWNIA,
    RAIN, SWALLOW, WILLOW_RED, WILLOW_2
)
