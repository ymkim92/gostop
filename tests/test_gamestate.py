"""test for gamestate"""

import unittest

from gostop.core.card import CHERRY, CRANE, PINE, PINE_RED_POEM, PLUM
from gostop.core.gamestate import GameActionPlayCard, GameStatePlay
from gostop.core.hand import Hand, TableCards


class GameStatePlayTest(unittest.TestCase):
    """gamestate play test"""

    def setUp(self):
        self.state = GameStatePlay()

    @unittest.skip("Need to implement support for 3 card stacks")
    def test_card_matches_three_stack_on_table(self):
        """test"""
        self.state.table_cards = TableCards(CRANE, PINE_RED_POEM, PINE)
        self.state.player_hands = [Hand(PINE), Hand()]
        actions = self.state.get_possible_actions()
        self.assertIn(GameActionPlayCard(PINE, (CRANE, PINE_RED_POEM, PINE)), actions)
        self.assertEqual(1, len(actions))

    def test_card_matches_two_on_table(self):
        """test"""
        self.state.table_cards = TableCards(PINE, CRANE, PLUM)
        self.state.player_hands = [Hand(PINE), Hand()]
        actions = self.state.get_possible_actions()
        self.assertIn(GameActionPlayCard(PINE, PINE), actions)
        self.assertIn(GameActionPlayCard(PINE, CRANE), actions)
        self.assertEqual(2, len(actions))

    def test_card_matches_none_on_table(self):
        """test"""
        self.state.table_cards = TableCards(PINE, CRANE, PLUM)
        self.state.player_hands = [Hand(CHERRY), Hand()]
        actions = self.state.get_possible_actions()
        self.assertIn(GameActionPlayCard(CHERRY), actions)
        self.assertEqual(1, len(actions))
