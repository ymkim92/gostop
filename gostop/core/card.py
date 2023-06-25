"""card"""

from .utils import _


class Card(object):
    def __init__(self, name, month, group):
        self.name = name
        self.month = month
        self.group = group

    def __repr__(self):
        return (
            "{__class__.__name__}(name='{name}', month={month}, group={group})".format(
                __class__=self.__class__, **self.__dict__
            )
        )

    def __str__(self):
        return self.name

    def __eq__(self, other):
        if other is None:
            return False
        elif isinstance(other, self.__class__):
            return self.month == other.month and self.group == other.group
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


CRANE = Card(_("Pine and Crane"), Month.JAN, Group.BRIGHT)
PINE_RED_POEM = Card(_("Pine and Red Poem Ribbon"), Month.JAN, Group.RIBBON)
PINE = Card(_("Pine"), Month.JAN, Group.JUNK)

BUSH_WARBLER = Card(_("Plum Blossom and Bush Warbler"), Month.FEB, Group.ANIMAL)
PLUM_RED_POEM = Card(_("Plum Blossom and Red Poem Ribbon"), Month.FEB, Group.RIBBON)
PLUM = Card(_("Plum Blossom"), Month.FEB, Group.JUNK)

CURTAIN = Card(_("Cherry Blossom and Curtain"), Month.MAR, Group.BRIGHT)
CHERRY_RED_POEM = Card(_("Cherry Blossom and Red Poem Ribbon"), Month.MAR, Group.RIBBON)
CHERRY = Card(_("Cherry Blossom"), Month.MAR, Group.JUNK)

CUCKOO = Card(_("Wisteria and Cuckoo"), Month.APR, Group.ANIMAL)
WISTERIA_RED = Card(_("Wisteria and Red Ribbon"), Month.APR, Group.RIBBON)
WISTERIA = Card(_("Wisteria"), Month.APR, Group.JUNK)

BRIDGE = Card(_("Iris and Bridge"), Month.MAY, Group.ANIMAL)
IRIS_RED = Card(_("Iris and Red Ribbon"), Month.MAY, Group.RIBBON)
IRIS = Card(_("Iris"), Month.MAY, Group.JUNK)

BUTTERFLY = Card(_("Peony and Butterfly"), Month.JUN, Group.ANIMAL)
PEONY_BLUE_POEM = Card(_("Peony and Blue Poem Ribbon"), Month.JUN, Group.RIBBON)
PEONY = Card(_("Peony"), Month.JUN, Group.JUNK)

BOAR = Card(_("Bush Clover and Boar"), Month.JUL, Group.ANIMAL)
BUSH_CLOVER_RED = Card(_("Bush Clover and Red Ribbon"), Month.JUL, Group.RIBBON)
BUSH_CLOVER = Card(_("Bush Clover"), Month.JUL, Group.JUNK)

MOON = Card(_("Pampas Grass and Moon"), Month.AUG, Group.BRIGHT)
GEESE = Card(_("Pampas Grass and Geese"), Month.AUG, Group.ANIMAL)
PAMPAS_GRASS = Card(_("Pampas Grass"), Month.AUG, Group.JUNK)

CUP = Card(_("Chrysanthemum and Cup"), Month.SEP, (Group.ANIMAL, Group.JUNK_2))
CHRYSANTHEMUM_BLUE_PEOM = Card(
    _("Chrysanthemum and Blue Poem Ribbon"), Month.SEP, Group.RIBBON
)
CHRYSANTHEMUM = Card(_("Chrysanthemum"), Month.SEP, Group.JUNK)

DEER = Card(_("Maple and Deer"), Month.OCT, Group.ANIMAL)
MAPLE_BLUE_POEM = Card(_("Maple and Blue Poem Ribbon"), Month.OCT, Group.RIBBON)
MAPLE = Card(_("Maple"), Month.OCT, Group.JUNK)

PHOENIX = Card(_("Paulownia and Phoenix"), Month.NOV, Group.BRIGHT)
PAULOWNIA = Card(_("Paulownia"), Month.NOV, Group.JUNK)
PAULOWNIA_2 = Card(_("Paulownia 2"), Month.NOV, Group.JUNK_2)

RAIN = Card(_("Willow and Rain"), Month.DEC, Group.BRIGHT)
SWALLOW = Card(_("Willow and Swallow"), Month.DEC, Group.ANIMAL)
WILLOW_RED = Card(_("Willow and Red Ribbon"), Month.DEC, Group.RIBBON)
WILLOW_2 = Card(_("Willow"), Month.DEC, Group.JUNK_2)


ALL_CARDS = (
    CRANE,
    PINE_RED_POEM,
    PINE,
    PINE,
    BUSH_WARBLER,
    PLUM_RED_POEM,
    PLUM,
    PLUM,
    CURTAIN,
    CHERRY_RED_POEM,
    CHERRY,
    CHERRY,
    CUCKOO,
    WISTERIA_RED,
    WISTERIA,
    WISTERIA,
    BRIDGE,
    IRIS_RED,
    IRIS,
    IRIS,
    BUTTERFLY,
    PEONY_BLUE_POEM,
    PEONY,
    PEONY,
    BOAR,
    BUSH_CLOVER_RED,
    BUSH_CLOVER,
    BUSH_CLOVER,
    MOON,
    GEESE,
    PAMPAS_GRASS,
    PAMPAS_GRASS,
    CUP,
    CHRYSANTHEMUM_BLUE_PEOM,
    CHRYSANTHEMUM,
    CHRYSANTHEMUM,
    DEER,
    MAPLE_BLUE_POEM,
    MAPLE,
    MAPLE,
    PHOENIX,
    PAULOWNIA_2,
    PAULOWNIA,
    PAULOWNIA,
    RAIN,
    SWALLOW,
    WILLOW_RED,
    WILLOW_2,
)
