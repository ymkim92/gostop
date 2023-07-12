"""test card"""
import unittest

from src.gostop.card import Card, Group, Month


class CardTest(unittest.TestCase):
    """card test"""

    def test_cards_equal(self):
        """test cards equal"""
        card1 = Card("Pine and Crane", Month.JAN, Group.BRIGHT)
        card2 = Card("Pine and Crane", Month.JAN, Group.BRIGHT)
        self.assertEqual(card1, card2)

    def test_hash_equal(self):
        """test hash equal"""
        card1 = Card("Pine and Crane", Month.JAN, Group.BRIGHT)
        card2 = Card("Pine and Crane", Month.JAN, Group.BRIGHT)
        self.assertEqual(hash(card1), hash(card2))
