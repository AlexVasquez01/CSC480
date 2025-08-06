import random
import math
import itertools
from collections import Counter

SUITS = ['C', 'D', 'H', 'S']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
ALL_CARDS = [r + s for r in RANKS for s in SUITS]

def random_cards(deck, k):
    return random.sample(deck, k)

def remove_cards(deck, cards_to_remove):
    return [card for card in deck if card not in cards_to_remove]

def eval_hand(cards):
    ranks = '23456789TJQKA'
    values = [card[0] for card in cards]
    suits = [card[1] for card in cards]
    count = Counter(values)
    is_flush = len(set(suits)) == 1
    is_straight = False
    rank_values = sorted([ranks.index(v) for v in set(values)])
    for i in range(len(rank_values) - 4 + 1):
        if rank_values[i+4] - rank_values[i] == 4:
            is_straight = True
    if not is_straight and set(['A', '2', '3', '4', '5']).issubset(values):
        is_straight = True
    score = 0
    if is_flush and is_straight:
        score = 8
    elif 4 in count.values():
        score = 7
    elif sorted(count.values()) == [2, 3]:
        score = 6
    elif is_flush:
        score = 5
    elif is_straight:
        score = 4
    elif 3 in count.values():
        score = 3
    elif list(count.values()).count(2) == 2:
        score = 2
    elif 2 in count.values():
        score = 1
    return score, sorted([ranks.index(v) for v in values], reverse=True)

def evaluate_best_hand(cards):
    best_score = (-1, [])
    for combo in itertools.combinations(cards, 5):
        score = eval_hand(combo)
        if score > best_score:
            best_score = score
    return best_score

def compare_hands(player_hand, opponent_hand):
    p_score = evaluate_best_hand(player_hand)
    o_score = evaluate_best_hand(opponent_hand)
    if p_score > o_score:
        return 1
    elif p_score < o_score:
        return 0
    return 0.5

class MCTSNode:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.wins = 0
        self.visits = 0

def ucb1(node, c=math.sqrt(2)):
    if node.visits == 0:
        return float('inf')
    return (node.wins / node.visits) + c * math.sqrt(math.log(node.parent.visits) / node.visits)

def select(node):
    while node.children:
        node = max(node.children, key=ucb1)
    return node

def expand(node, deck):
    if len(node.state) == 5:
        return node  #river
    for _ in range(5 - len(node.state)):
        new_card = random.choice(deck)
        new_state = node.state + [new_card]
        deck = remove_cards(deck, [new_card])
        child = MCTSNode(new_state, node)
        node.children.append(child)
    return node.children[-1]

def simulate(state, player_cards, opponent_cards):
    community = state
    player_full = player_cards + community
    opponent_full = opponent_cards + community
    return compare_hands(player_full, opponent_full)

def backpropagate(node, result):
    while node:
        node.visits += 1
        node.wins += result
        node = node.parent

def estimate_win_rate(hole_cards, num_simulations=1000):
    wins = 0
    for _ in range(num_simulations):
        deck = remove_cards(ALL_CARDS, hole_cards)
        opponent = random_cards(deck, 2)
        deck = remove_cards(deck, opponent)
        community = random_cards(deck, 5)

        player_hand = hole_cards + community
        opponent_hand = opponent + community

        result = compare_hands(player_hand, opponent_hand)
        wins += result
    return wins / num_simulations

