import unittest
from poker_mcts import (
    eval_hand, evaluate_best_hand, compare_hands, mcts
)

class TestPokerFunctions(unittest.TestCase):

    def test_hand_ranking_flush(self):
        cards = ['2H', '4H', '6H', '8H', 'JH']
        rank = eval_hand(cards)[0]
        self.assertEqual(rank, 5)  #flush

    def test_hand_ranking_straight(self):
        cards = ['3D', '4S', '5C', '6H', '7D']
        rank = eval_hand(cards)[0]
        self.assertEqual(rank, 4)  #straight

    def test_hand_ranking_four_of_a_kind(self):
        cards = ['9C', '9D', '9H', '9S', '2D']
        rank = eval_hand(cards)[0]
        self.assertEqual(rank, 7)  #four of a kind

    def test_hand_ranking_full_house(self):
        cards = ['KH', 'KC', 'KS', '2D', '2C']
        rank = eval_hand(cards)[0]
        self.assertEqual(rank, 6)  #full house

    def test_hand_ranking_two_pair(self):
        cards = ['5C', '5S', '8D', '8H', 'JD']
        rank = eval_hand(cards)[0]
        self.assertEqual(rank, 2)  #two pair

    def test_best_hand_eval(self):
        cards = ['AH', 'KH', 'QH', 'JH', 'TH', '3C', '2D']  #royal flush
        score = evaluate_best_hand(cards)[0]
        self.assertEqual(score, 8)

    def test_compare_hands_win(self):
        player = ['AH', 'KH', 'QH', 'JH', 'TH']
        opponent = ['9C', '9D', '9H', '9S', '2D']
        result = compare_hands(player, opponent)
        self.assertEqual(result, 1)  #player wins

    def test_compare_hands_lose(self):
        player = ['2H', '3H', '4H', '5H', '7D']
        opponent = ['KH', 'KC', 'KS', '2D', '2C']
        result = compare_hands(player, opponent)
        self.assertEqual(result, 0)  #opponent wins

    def test_compare_hands_tie(self):
        player = ['3H', '3D', '4S', '5C', '6H']
        opponent = ['3C', '3S', '4D', '5H', '6C']
        result = compare_hands(player, opponent)
        self.assertEqual(result, 0.5)  #tie

    def test_mcts_output_range(self):
        hole_cards = ['AH', 'KH']
        win_rate = mcts(hole_cards, num_simulations=100)
        self.assertTrue(0.0 <= win_rate <= 1.0)

if __name__ == '__main__':
    unittest.main()
