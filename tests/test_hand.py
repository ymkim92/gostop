"""test hand"""
import unittest
from itertools import combinations

from src.gostop.card import (
    BOAR,
    BRIDGE,
    BUSH_CLOVER,
    BUSH_CLOVER_RED,
    BUSH_WARBLER,
    BUTTERFLY,
    CHERRY,
    CHERRY_RED_POEM,
    CHRYSANTHEMUM,
    CHRYSANTHEMUM_BLUE_PEOM,
    CRANE,
    CUCKOO,
    CUP,
    CURTAIN,
    DEER,
    GEESE,
    IRIS,
    IRIS_RED,
    MAPLE,
    MAPLE_BLUE_POEM,
    MOON,
    PAMPAS_GRASS,
    PAULOWNIA,
    PAULOWNIA_2,
    PEONY,
    PEONY_BLUE_POEM,
    PHOENIX,
    PINE,
    PINE_RED_POEM,
    PLUM,
    PLUM_RED_POEM,
    RAIN,
    SWALLOW,
    WILLOW_2,
    WISTERIA,
    WISTERIA_RED,
    Group,
    Month,
)
from src.gostop.hand import CardList, Hand, TakenCards


class CardListTest(unittest.TestCase):
    """card list test"""

    def test_add_and_pop(self):
        """test add and pop"""
        cards = CardList()
        cards += CRANE
        self.assertEqual(len(cards), 1)

        card = cards.pop()
        self.assertEqual(card, CRANE)

        self.assertRaises(IndexError, cards.pop)

    def test_clear(self):
        """test clear"""
        cards = CardList(CRANE, CURTAIN, MOON, PHOENIX, RAIN, SWALLOW)
        cards.clear()

        self.assertEqual(len(cards), 0)

    def test_equal(self):
        """test equal"""
        _h1 = CardList(CRANE, PINE_RED_POEM, PINE, PINE)
        _h2 = CardList(PINE_RED_POEM, PINE, CRANE, PINE)
        self.assertEqual(_h1, _h2)

    def test_hash(self):
        """test hash"""
        _h1 = CardList(CRANE, PINE_RED_POEM, PINE, PINE)
        _h2 = CardList(PINE_RED_POEM, PINE, CRANE, PINE)
        self.assertEqual(hash(_h1), hash(_h2))

    def test_split_by_month(self):
        """test split by month"""
        cards = CardList(CRANE, CURTAIN, MOON, PHOENIX, RAIN, SWALLOW)
        month_cards = cards.split_by_month()

        self.assertEqual(
            month_cards[Month.JAN],
            [
                CRANE,
            ],
        )
        self.assertEqual(month_cards[Month.FEB], [])
        self.assertEqual(month_cards[Month.DEC], [RAIN, SWALLOW])

    def test_split_by_group(self):
        """test split by group"""
        cards = CardList(CRANE, CUCKOO, IRIS_RED, PAULOWNIA, WISTERIA, WILLOW_2)
        group_cards = cards.split_by_group()

        self.assertEqual(
            group_cards[Group.BRIGHT],
            [
                CRANE,
            ],
        )
        self.assertEqual(
            group_cards[Group.ANIMAL],
            [
                CUCKOO,
            ],
        )
        self.assertEqual(
            group_cards[Group.RIBBON],
            [
                IRIS_RED,
            ],
        )
        self.assertEqual(group_cards[Group.JUNK], [PAULOWNIA, WISTERIA])
        self.assertEqual(
            group_cards[Group.JUNK_2],
            [
                WILLOW_2,
            ],
        )


class HandTest(unittest.TestCase):
    """hand test"""

    def test_score(self):
        """test score"""
        _h1 = Hand(CRANE, PINE_RED_POEM, PINE, PINE)
        self.assertEqual(_h1.score, [("Four cards of a month", 1)])
        _h2 = Hand(CRANE, PINE_RED_POEM, PINE)
        self.assertEqual(_h2.score, [("Three cards of a month", 1)])


class TakenCardsTest(unittest.TestCase):
    """taken cards test"""

    # pylint: disable=missing-function-docstring

    def test_no_score(self):
        """test no score"""
        _h = TakenCards(CRANE, PINE, CUCKOO, WISTERIA, PEONY, MAPLE)
        self.assertEqual(_h.score, [])

    def test_five_brights(self):
        """test five brights"""
        _h = TakenCards(CRANE, CURTAIN, MOON, PHOENIX, RAIN)
        self.assertEqual(_h.score, [("Five brights", 15)])

    def test_four_brights(self):
        """test four brights"""
        bright_cards = (CRANE, CURTAIN, MOON, PHOENIX, RAIN)
        for cards in combinations(bright_cards, 4):
            _h = TakenCards(*cards)
            self.assertEqual(_h.score, [("Four brights", 4)])

    def test_three_brights_without_rain(self):
        bright_cards = (CRANE, CURTAIN, MOON, PHOENIX)
        for cards in combinations(bright_cards, 3):
            _h = TakenCards(*cards)
            self.assertEqual(_h.score, [("Three brights without rain", 3)])

    def test_three_brights_with_rain(self):
        bright_cards = (CRANE, CURTAIN, MOON, PHOENIX)
        for cards in combinations(bright_cards, 2):
            cards += (RAIN,)
            _h = TakenCards(*cards)
            self.assertEqual(_h.score, [("Three brights with rain", 2)])

    def test_five_or_more_animals(self):
        animal_cards = (
            BUSH_WARBLER,
            CUCKOO,
            BRIDGE,
            BUTTERFLY,
            BOAR,
            GEESE,
            CUP,
            DEER,
            SWALLOW,
        )
        for i in range(5, len(animal_cards)):
            for cards in combinations(animal_cards, i):
                _h = TakenCards(*cards)
                self.assertIn((f"{i} animals", i - 4), _h.score)

    def test_godori(self):
        _h = TakenCards(BUSH_WARBLER, CUCKOO, GEESE)
        self.assertEqual(_h.score, [("Godori", 5)])

    def test_five_or_more_ribbons(self):
        ribbon_cards = (
            PINE_RED_POEM,
            PLUM_RED_POEM,
            CHERRY_RED_POEM,
            WISTERIA_RED,
            IRIS_RED,
            BUSH_CLOVER_RED,
            PEONY_BLUE_POEM,
            CHRYSANTHEMUM_BLUE_PEOM,
            MAPLE_BLUE_POEM,
        )
        for i in range(5, len(ribbon_cards)):
            for cards in combinations(ribbon_cards, i):
                _h = TakenCards(*cards)
                self.assertIn((f"{i} ribbons", i - 4), _h.score)

    def test_three_red_ribbons_with_poem(self):
        _h = TakenCards(PINE_RED_POEM, PLUM_RED_POEM, CHERRY_RED_POEM)
        self.assertEqual(_h.score, [("Three red ribbons with poem", 3)])

    def test_three_red_ribbons(self):
        """test three red ribbons"""
        _h = TakenCards(WISTERIA_RED, IRIS_RED, BUSH_CLOVER_RED)
        self.assertEqual(_h.score, [("Three red ribbons", 3)])

    def test_three_blue_ribbons_with_poem(self):
        """test three blue ribbons with poem"""
        _h = TakenCards(PEONY_BLUE_POEM, CHRYSANTHEMUM_BLUE_PEOM, MAPLE_BLUE_POEM)
        self.assertEqual(_h.score, [("Three blue ribbons with poem", 3)])

    def test_ten_or_more_junk(self):
        """test ten or more junk"""
        junk_cards = (
            PINE,
            PINE,
            PLUM,
            PLUM,
            CHERRY,
            CHERRY,
            WISTERIA,
            WISTERIA,
            IRIS,
            IRIS,
            PEONY,
            PEONY,
            BUSH_CLOVER,
            BUSH_CLOVER,
            PAMPAS_GRASS,
            PAMPAS_GRASS,
            CHRYSANTHEMUM,
            CHRYSANTHEMUM,
            MAPLE,
            MAPLE,
            PAULOWNIA,
            PAULOWNIA,
        )
        # two_junk_cards = (PAULOWNIA_2, WILLOW_2, CUP)

        for i in range(10, len(junk_cards)):
            _h = TakenCards(*junk_cards[:i])
            self.assertEqual(_h.score, [(f"{i} junk cards", i - 9)])

            # for cards in combinations(junk_cards, i):
            #     h = TakenCards(*cards)
            #     self.assertEqual(h.score, [('{0} junk cards'.format(i), i-9)])
