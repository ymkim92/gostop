import copy
import random
import logging
from PIL import Image
from .build_a_image import get_concat_h, add_number


from .hand import TableCards, TakenCards, Hand
from .deck import Deck

logging.basicConfig(level=logging.INFO)

class GameStateException(Exception):
    pass


class GameState(object):
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
            self.player_hands = \
                [Hand(*cards) for cards in prev_state.player_hands]
            self.taken_cards = \
                [TakenCards(*cards) for cards in prev_state.taken_cards]
        else:
            self.current_player = 0
            self.deck = Deck()
            self.table_cards = TableCards()
            self.player_hands = \
            [Hand() for i in range(0, self.number_of_players)]
            self.taken_cards = \
                [TakenCards() for i in range(0, self.number_of_players)]

    def __eq__(self, other):
        if other is None:
            return False
        if not self.current_player == other.current_player:
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
        return hash((self.current_player, self.deck, self.table_cards,
                     zip(self.player_hands), zip(self.taken_cards)))

    def __str__(self):
        out = 'Table: {0}\n'.format(str(self.table_cards))
        create_image(self.table_cards, 'html/table.png', overlap=0)
        for i in range(0, self.number_of_players):
            out += 'Hand: {0}\n'.format(str(self.player_hands[i]))
            out += 'Taken cards: {0}\n'.format(str(self.taken_cards[i]))
            out += 'Score: {0}\n'.format(self.taken_cards[i].score)
            create_image(self.player_hands[i], f'html/hand{i}.png', number=True)
            create_image(self.taken_cards[i], f'html/taken{i}.png')
        
        return out

    @staticmethod
    def new_game(number_of_players=2):
        """Reset the game state for the beginning of a new game, and deal
        cards to each player.
        """
        state = GameStatePlay()
        state.deck.shuffle()

        for i in range(0, 2):
            for p in range(0, state.number_of_players):
                state.player_hands[p] += state.deck.pop()
                state.player_hands[p] += state.deck.pop()
                state.player_hands[p] += state.deck.pop()
                state.player_hands[p] += state.deck.pop()
                state.player_hands[p] += state.deck.pop()
            state.table_cards += state.deck.pop()
            state.table_cards += state.deck.pop()
            state.table_cards += state.deck.pop()
            state.table_cards += state.deck.pop()

        return state

    def copy_and_randomise(self, observer):
        """Returns a deep copy of the game state, randomising any information
        which is not visible to the specified observing player.
        """
        state = self.__class__(prev_state=self)

        # The observer can see his own hand, the cards on the table, and any
        # cards captured by other players
        seen_cards = [card for card in state.player_hands[observer]] + \
                     [card for card in state.table_cards] + \
                     [card for tc in state.taken_cards for card in tc]
        unseen_cards = [card for card in Deck()
                        if card not in seen_cards or seen_cards.remove(card)]

        # Randomly deal the unseen cards to the other players
        random.shuffle(unseen_cards)
        for player in range(0, self.number_of_players):
            if player != observer:
                num_cards = len(state.player_hands[player])
                state.player_hands[player] = Hand(*unseen_cards[:num_cards])
                unseen_cards = unseen_cards[num_cards:]

        return state

    def get_result(self, player):
        if self.winner == player:
            return 1
        elif self.winner is not None:
            return 0
        elif self.get_possible_actions() == []:
            return 0.5
        return 0

    def get_possible_actions(self):
        """Returns a list of possible actions for the current agent."""
        raise NotImplementedError()

    def generate_successor(self, action):
        """Returns the successor state after the current agent takes `action`.
        """
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
        """Returns the successor state after the current agent takes `action`.
        """
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
        print(state.top_card.month, state.top_card.order_in_month)
        create_image([state.top_card], 'html/top_card.png')
        return state


class GameAction(object):
    pass


class GameActionPlayCard(GameAction):
    def __init__(self, card, paired_card=None):
        super(GameActionPlayCard, self).__init__()
        self.card = card
        self.paired_card = paired_card

    def __eq__(self, other):
        if other is None:
            return False
        else:
            return self.card == other.card and \
                   self.paired_card == other.paired_card

    def __str__(self):
        if self.paired_card:
            out = '{}, {}'.format(str(self.card), str(self.paired_card))
        else:
            out = '{}'.format(str(self.card))
        return out


class GameActionGo(GameAction):
    def __eq__(self, other):
        if isinstance(other, GameActionGo):
            return True
        else:
            return False

    def __str__(self):
        return 'Go'


class GameActionStop(GameAction):
    def __eq__(self, other):
        if isinstance(other, GameActionStop):
            return True
        else:
            return False

    def __str__(self):
        return 'Stop'


class GameStateCapture(GameState):
    def __str__(self):
        out = super().__str__()
        out += 'Top card: {0}\n'.format(self.top_card)
        out += 'Paired cards: {0}\n'.format(self.paired_cards)
        return out

    def copy_and_randomise(self, observer):
        """Returns a deep copy of the game state, randomising any information
        which is not visible to the specified observing player.
        """
        state = self.__class__(prev_state=self)
        state.top_card = self.top_card
        state.paired_cards = self.paired_cards

        # The observer can see his own hand, the cards on the table, and any
        # cards captured by other players
        seen_cards = [card for card in state.player_hands[observer]] + \
                     [card for card in state.table_cards] + \
                     [card for tc in state.taken_cards for card in tc]
        unseen_cards = [card for card in Deck()
                        if card not in seen_cards or seen_cards.remove(card)]

        # Randomly deal the unseen cards to the other players
        random.shuffle(unseen_cards)
        for player in range(0, self.number_of_players):
            if player != observer:
                num_cards = len(state.player_hands[player])
                state.player_hands[player] = Hand(*unseen_cards[:num_cards])
                unseen_cards = unseen_cards[num_cards:]

        return state

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
        """Returns the successor state after the current agent takes `action`.
        """
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
            state.current_player = (state.current_player+1) % state.number_of_players
        return state


class GameStateGoStop(GameState):
    def get_possible_actions(self):
        """Returns a list of possible actions for the current agent."""
        if len(self.deck) > 0:
            return [GameActionGo(), GameActionStop()]
        else:
            return [GameActionStop()]

    def generate_successor(self, action):
        """Returns the successor state after the current agent takes `action`.
        """
        if type(action) == GameActionGo:
            state = GameStatePlay(prev_state=self)
            state.current_player = (state.current_player+1) % state.number_of_players
        else:
            state = GameStateEnd(prev_state=self)
            state.winner = self.current_player
        return state


class GameStateEnd(GameState):
    def get_possible_actions(self):
        """Returns a list of possible actions for the current agent."""
        return []

    def generate_successor(self, action):
        """Returns the successor state after the current agent takes `action`.
        """
        return None

def create_image(card_list, image_name="html/gostop.png", number=False, overlap=50):
    images = []
    for i, card in enumerate(card_list):
        img = Image.open(f"images/{card.month-1:x}{card.order_in_month}.png")
        if number:
            img = add_number(img, i) 
        images.append(img)
    
    if len(images) == 0:
        logging.warning("Empty image")
        dst_image = Image.new('RGB', (1,1))
    else:
        dst_image = images.pop(0)
        for i in images:
            dst_image = get_concat_h(dst_image, i, overlap)

    dst_image.save(image_name)