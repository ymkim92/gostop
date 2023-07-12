"""test deck"""
import unittest

from src.gostop.deck import Deck


class DeckTest(unittest.TestCase):
    """deck test"""

    def test_deck(self):
        """test deck"""
        _d = Deck()
        self.assertGreaterEqual(48, len(_d))
