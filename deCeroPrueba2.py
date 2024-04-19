import random
from collections import Counter

class Player:
    def __init__(self, name):
        self.name = name
        self.chips = 500
        self.hand = []
        self.best_hand = None

    def receive_cards(self, cards):
        self.hand.extend(cards)

    def reset_hand(self):
        self.hand = []
        self.best_hand = None

class Game:
    def __init__(self):
        self.players = []
        self.deck = self.create_deck()
        self.pot = 0
        self.community_cards = []
        self.current_bet = 0
        self.small_blind = 5
        self.big_blind = 10

    def create_deck(self):
        with open("baraja.txt", "r") as file:
            cards = file.readlines()
            deck = [card.strip() for card in cards]
            random.shuffle(deck)
            return deck

    def deal_cards(self, num_cards):
        cards = [self.deck.pop() for _ in range(num_cards)]
        return cards

    def deal_initial_cards(self):
        for player in self.players:
            player.receive_cards(self.deal_cards(2))

    def deal_community_cards(self, num_cards):
        self.community_cards.extend(self.deal_cards(num_cards))

    def evaluate_hands(self):
        for player in self.players:
            player_hand = player.hand + self.community_cards
            player.best_hand = self.evaluate_best_hand(player_hand)

    def determine_winner(self):
        player_hands = [(player, player.best_hand) for player in self.players]
        best_hand_rank = max([hand[1] for hand in player_hands])
        winners = [player for player, hand in player_hands if hand == best_hand_rank]

        if len(winners) == 1:
            winner = winners[0]
            winner.chips += self.pot
            print(f"{winner.name} wins the pot of {self.pot} chips with {winner.best_hand}!")
        else:
            high_card_values = []
            for winner in winners:
                winner_hand = winner.hand + self.community_cards
                high_card_values.append(max([self.get_card_value(card) for card in winner_hand]))

            max_high_card_value = max(high_card_values)
            final_winners = [winner for winner, high_card_value in zip(winners, high_card_values) if high_card_value == max_high_card_value]

            if len(final_winners) == 1:
                winner = final_winners[0]
                winner.chips += self.pot
                print(f"{winner.name} wins the pot of {self.pot} chips with {winner.best_hand}!")
            else:
                split_pot = self.pot // len(final_winners)
                for winner in final_winners:
                    winner.chips += split_pot
                    print(f"{winner.name} wins {split_pot} chips with {winner.best_hand}!")

    def reset_game(self):
        self.deck = self.create_deck()
        self.pot = 0
        self.community_cards = []
        self.current_bet = 0
        for player in self.players:
            player.reset_hand()

    def betting_round(self, round_name):
        print(f"\n{round_name} betting round")
        self.current_bet = 0
        players_in_round = self.players.copy()

        # Blinds
        self.players[0].chips -= self.small_blind
        self.pot += self.small_blind
        self.players[1].chips -= self.big_blind
        self.pot += self.big_blind
        self.current_bet = self.big_blind

        # Player actions
        player_turn = 2
        while len(players_in_round) > 1:
            player = players_in_round[player_turn % len(players_in_round)]
            print(f"\n{player.name}'s turn. Chips: {player.chips}, Current bet: {self.current_bet}")
            action = self.get_player_action(player)

            if action == "fold":
                players_in_round.remove(player)
            elif action == "call":
                chips_to_call = self.current_bet - (self.big_blind if player_turn == 1 else 0)
                player.chips -= chips_to_call
                self.pot += chips_to_call
            elif action == "raise":
                raise_amount = int(input("Enter the raise amount: "))
                if raise_amount <= self.current_bet or player.chips < raise_amount:
                    print("Invalid raise amount. Please try again.")
                    continue
                player.chips -= raise_amount
                self.pot += raise_amount
                self.current_bet = raise_amount
                players_in_round = [player] + players_in_round[:player_turn]
            elif action == "all-in":
                all_in_amount = player.chips + (self.big_blind if player_turn == 1 else 0)
                player.chips = 0
                self.pot += all_in_amount
                players_in_round = [player] + players_in_round[:player_turn]

            player_turn += 1

        self.players = players_in_round

    def get_player_action(self, player):
        action = input(f"{player.name}, enter your action (call, raise, fold, all-in): ").lower()
        while action not in ["call", "raise", "fold", "all-in"]:
            action = input("Invalid action. Please enter call, raise, fold, or all-in: ").lower()
        return action

def play_game():
    game = Game()
    print("Welcome to Texas Hold'em Poker!")
    num_players = int(input("Enter the number of players (2-8): "))

    if num_players < 2 or num_players > 8:
        print("Invalid number of players. The game supports 2-8 players.")
        return

    player_names = []
    for i in range(num_players):
        player_name = input(f"Enter the name of player {i + 1}: ")
        player_names.append(player_name)
        game.players.append(Player(player_name))

    print("Let's play!")

    while True:
        game.deal_initial_cards()

        # Pre-flop betting round
        game.betting_round("Pre-flop")

        if len(game.players) == 1:
            print(f"{game.players[0].name} wins the pot of {game.pot} chips!")
            game.reset_game()
            continue

        game.deal_community_cards(3)  # Flop

        # Flop betting round
        game.betting_round("Flop")

        if len(game.players) == 1:
            print(f"{game.players[0].name} wins the pot of {game.pot} chips!")
            game.reset_game()
            continue

        game.deal_community_cards(1)  # Turn

        # Turn betting round
        game.betting_round("Turn")

        if len(game.players) == 1:
            print(f"{game.players[0].name} wins the pot of {game.pot} chips!")
            game.reset_game()
            continue

        game.deal_community_cards(1)  # River

        # River betting round
        game.betting_round("River")

        if len(game.players) == 1:
            print(f"{game.players[0].name} wins the pot of {game.pot} chips!")
            game.reset_game()
            continue

        game.evaluate_hands()
        game.determine_winner()
        game.reset_game()

play_game()
