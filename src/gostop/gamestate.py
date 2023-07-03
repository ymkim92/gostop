"""game state"""

from .deck import Deck
from .hand import Hand, TableCards, TakenCards


# TODO split this into game state and game action
class GameStateException(Exception):
    """game state exception"""


class GameState:
    """The GameState specifies the complete state of the game, including the
    player's hands, cards on the table and scoring.
    """

    def __init__(self, prev_state=None):
        self.number_of_players = 2
        self.winner = None

        if prev_state is not None:
            self.current_player = prev_state.current_player
            self.deck = Deck(cards=prev_state.deck)
            self.table_cards = TableCards(*prev_state.table_cards)
            self.player_hands = [Hand(*cards) for cards in prev_state.player_hands]
            self.taken_cards = [TakenCards(*cards) for cards in prev_state.taken_cards]
        else:
            self.current_player = 0
            self.deck = Deck()
            self.table_cards = TableCards()
            self.player_hands = [Hand() for i in range(0, self.number_of_players)]
            self.taken_cards = [TakenCards() for i in range(0, self.number_of_players)]

    def __eq__(self, other):
        if other is None or not self.current_player == other.current_player:
            return False
        if not self.deck == other.deck:
            return False
        if not self.table_cards == other.table_cards:
            return False
        for i in range(self.number_of_players):
            if not set(self.player_hands[i].cards) == set(other.player_hands[i].cards):
                return False
            if not set(self.taken_cards[i].cards) == set(other.taken_cards[i].cards):
                return False
        return True

    def __hash__(self):
        return hash(
            (
                self.current_player,
                self.deck,
                self.table_cards,
                zip(self.player_hands),
                zip(self.taken_cards),
            )
        )

    def __str__(self):
        out = f"Table: {str(self.table_cards)}\n"
        for i in range(0, self.number_of_players):
            out += f"Hand: {str(self.player_hands[i])}\n"
            out += f"Taken cards: {str(self.taken_cards[i])}\n"
            out += f"Score: {self.taken_cards[i].score}\n"
        return out

    @staticmethod
    def new_game():
        """Reset the game state for the beginning of a new game, and deal
        cards to each player.
        """
        state = GameStatePlay()
        state.deck.shuffle()

        for _ in range(0, 2):
            for _p in range(0, state.number_of_players):
                state.player_hands[_p] += state.deck.pop()
                state.player_hands[_p] += state.deck.pop()
                state.player_hands[_p] += state.deck.pop()
                state.player_hands[_p] += state.deck.pop()
                state.player_hands[_p] += state.deck.pop()
            state.table_cards += state.deck.pop()
            state.table_cards += state.deck.pop()
            state.table_cards += state.deck.pop()
            state.table_cards += state.deck.pop()

        return state

    def get_result(self, player):
        """get result"""
        if self.winner == player:
            return 1

        if self.winner is not None:
            return 0

        # no winner here
        if self.get_possible_actions() == []:
            # no possible actions
            return 0.5

        return 0

    def get_possible_actions(self):
        """Returns a list of possible actions for the current agent."""
        raise NotImplementedError()

    def generate_successor(self, action):
        """Returns the successor state after the current agent takes `action`."""
        raise NotImplementedError()


class GameStatePlay(GameState):
    """In this state the player plays one card to the table layout.

    An action consists of a card from the player's hand and a matching card
    on the table.

    If the card does not match any card in the table layout the paired card
    is `None` and the card is added to the table. If the card matches one or
    two cards in the table layout, the paired card may be either of the
    matching cards. If the card matches three cards in the table layout, the
    player captures all four cards."""

    def get_possible_actions(self):
        """Returns a list of possible actions for the current agent."""
        possible_actions = []
        for card in self.player_hands[self.current_player]:
            paired_cards = self.table_cards.get_paired_cards(card)
            if paired_cards == []:
                possible_actions.append(GameActionPlayCard(card))
            else:
                for paired_card in paired_cards:
                    possible_actions.append(GameActionPlayCard(card, paired_card))
        return possible_actions

    def generate_successor(self, action):
        """Returns the successor state after the current agent takes `action`."""
        state = GameStateCapture(prev_state=self)

        if action is not None:
            # Remove the played card from the player's hand
            state.player_hands[state.current_player].remove(action.card)

            if action.paired_card is not None:
                # Remove paired card from the table
                state.table_cards.remove(action.paired_card)
            else:
                # No match; add the card to the table
                state.table_cards += action.card

        state.paired_cards = action
        state.top_card = state.deck.pop()
        return state


class GameStateCapture(GameState):
    """game state: capture"""

    def __init__(self, prev_state=None):
        super().__init__(prev_state)
        self.paired_cards = None
        self.top_card = None

    def __str__(self):
        out = super().__str__()
        out += f"Top card: {0}\n".format(self.top_card)
        out += f"Paired cards: {0}\n".format(self.paired_cards)
        return out

    def get_possible_actions(self):
        """Returns a list of possible actions for the current agent."""
        possible_actions = []
        paired_cards = self.table_cards.get_paired_cards(self.top_card)
        if paired_cards == []:
            possible_actions.append(GameActionPlayCard(self.top_card))
        else:
            for paired_card in paired_cards:
                possible_actions.append(GameActionPlayCard(self.top_card, paired_card))
        return possible_actions

    def generate_successor(self, action):
        """Returns the successor state after the current agent takes `action`."""
        state = GameStatePlay(prev_state=self)

        # Capture from last turn
        if action is None:
            raise GameStateException("No action from this turn")
        if self.paired_cards is None:
            raise GameStateException("No action from last turn")

        # If the card is paired with one from the table, add cards to captures
        # Otherwise just add the played card to the table
        if self.paired_cards.paired_card is not None:
            state.taken_cards[state.current_player] += self.paired_cards.card
            state.taken_cards[state.current_player] += self.paired_cards.paired_card

        # Deck card and table cards
        if action is not None:
            if action.paired_card is not None:
                # Remove paired card from the table
                state.table_cards.remove(action.paired_card)

                # Add matching cards to captures
                state.taken_cards[state.current_player] += action.card
                state.taken_cards[state.current_player] += action.paired_card
            else:
                # Add the card to the table
                state.table_cards += action.card

        total_score = 0
        for i, s in state.taken_cards[state.current_player].score:
            total_score += s
        if total_score >= 5:
            state = GameStateGoStop(prev_state=state)
        else:
            # Next player's turn
            state.current_player = (state.current_player + 1) % state.number_of_players
        return state


class GameStateGoStop(GameState):
    """game state: gostop"""

    def get_possible_actions(self):
        """Returns a list of possible actions for the current agent."""
        if len(self.deck) > 0:
            return [GameActionGo(), GameActionStop()]

        return [GameActionStop()]

    def generate_successor(self, action):
        """Returns the successor state after the current agent takes `action`."""
        if isinstance(action) == GameActionGo:
            state = GameStatePlay(prev_state=self)
            state.current_player = (state.current_player + 1) % state.number_of_players
        else:
            state = GameStateEnd(prev_state=self)
            state.winner = self.current_player
        return state


class GameStateEnd(GameState):
    def get_possible_actions(self):
        """Returns a list of possible actions for the current agent."""
        return []

    def generate_successor(self, action):
        """Returns the successor state after the current agent takes `action`."""
        return None


# pylint: disable=too-few-public-methods
class GameAction:
    """game action"""


class GameActionPlayCard(GameAction):
    """game action: play card"""

    def __init__(self, card, paired_card=None):
        super().__init__()
        self.card = card
        self.paired_card = paired_card

    def __eq__(self, other):
        if other is None:
            return False

        return self.card == other.card and self.paired_card == other.paired_card

    def __str__(self):
        if self.paired_card:
            out = f"{str(self.card)}, {str(self.paired_card)}"
        else:
            out = f"{str(self.card)}"
        return out


class GameActionGo(GameAction):
    """game action: go"""

    def __eq__(self, other):
        if isinstance(other, GameActionGo):
            return True

        return False

    def __str__(self):
        return "Go"


class GameActionStop(GameAction):
    """game action: stop"""

    def __eq__(self, other):
        if isinstance(other, GameActionStop):
            return True

        return False

    def __str__(self):
        return "Stop"
