import random

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return f"{self.rank} of {self.suit}"

class CardDeck:
    def __init__(self):
        self.cards = []

    def create_deck(self):
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        self.cards = [Card(rank, suit) for suit in suits for rank in ranks]
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop()

class Player:
    def __init__(self, name):
        self.name = name
        self.chips = 500
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def remove_chips(self, amount):
        self.chips -= amount

class PokerHoldem:
    def __init__(self):
        self.players = []
        self.table = []
        self.deck = CardDeck()
        self.pre_flop_finished = False

    def start_game(self):
        self.deck.create_deck()
        self.initial_deal_cards()
        self.show_initial_chips()

        while True:
            self.turn_players()
            if self.pre_flop_finished:
                self.river_betting_round()
                break
            self.pre_flop_finished = True

    def initial_deal_cards(self):
        player_name = self.validate_string_name_input("Ingrese su nombre: ")
        player = Player(player_name)
        self.players.append(player)
        sheldon = Player("Sheldon Cooper")
        self.players.append(sheldon)

        for _ in range(2):
            for player in self.players:
                card = self.deck.deal_card()
                player.add_card(card)

        self.table = [self.deck.deal_card() for _ in range(5)]

    def show_initial_chips(self):
        print("\n|------------------------------------------|")
        for player in self.players:
            print(f"|{player.name}, tiene las siguientes fichas:")
        print("|               TOTAL ($500)               ")
        print("|------------------------------------------|\n")

    def turn_players(self):
        for player in self.players:
            print(f"\nTurno de {player.name}")
            if player.name == "Sheldon Cooper":
                sheldon_move = self.sheldon_decide_move(player.cards, self.table)
                print("Sheldon Cooper seleccionó:", sheldon_move)
                if sheldon_move == "Fold":
                    self.fold(player)
                else:
                    self.call_option_fold(sheldon_move, player)
            else:
                option = input("Ingrese el próximo movimiento (1: Call, 2: Bet, 3: Fold, 4: All in): ")
                if option == "1":
                    self.call_option_fold("Call", player)
                elif option == "2":
                    self.call_option_fold("Bet", player)
                elif option == "3":
                    self.fold(player)
                elif option == "4":
                    self.all_in(player)
                else:
                    print("Opción inválida.")

    def call_option_fold(self, move, player):
        if move == "Call":
            opponent = self.players[0] if player.name == "Sheldon Cooper" else self.players[1]
            player_bet = player.chips
            opponent_bet = opponent.chips
            amount_to_call = opponent_bet - player_bet
            if player.chips < amount_to_call:
                print("No tienes suficientes fichas para igualar la apuesta.")
                return
            player.remove_chips(amount_to_call)
            opponent.remove_chips(amount_to_call)
            print(f"{player.name} igualó la apuesta de {amount_to_call} fichas.")
        elif move == "Bet":
            while True:
                try:
                    raise_amount = int(input("Ingrese la cantidad que desea subir la apuesta: "))
                    if raise_amount <= 0:
                        print("La cantidad debe ser mayor que cero.")
                        continue
                    elif raise_amount > player.chips:
                        print("No tienes suficientes fichas para subir esa cantidad.")
                        continue
                    else:
                        player.remove_chips(raise_amount)
                        print(f"{player.name} subió la apuesta en {raise_amount} fichas.")
                        break
                except ValueError:
                    print("Por favor, ingrese un número entero.")
        elif move == "Fold":
            self.fold(player)
        else:
            print("Movimiento inválido.")

    def fold(self, player):
        print(f"{player.name} se retiró del juego con {player.chips} fichas.")
        player.chips = 0

    def all_in(self, player):
        print(f"{player.name} hizo un All-in!")
        player.chips = 0

    def sheldon_decide_move(self, sheldon_cards, table_cards):
        # Implementa la lógica para que Sheldon decida su movimiento
        # Puedes utilizar el valor de las cartas de Sheldon y las cartas en la mesa
        # Por ahora, siempre devuelve "Fold"
        return "Fold"

    def river_betting_round(self):
        # Implementa la ronda de apuestas después de que se muestren las cartas del río
        pass

    def validate_string_name_input(self, prompt):
        while True:
            user_input = input(prompt)
            if not user_input.replace(" ","").isalpha() or not user_input.istitle():
                print("Debe ser un nombre con solo letras, ademas debe empezar con una mayuscula inicial")
                continue
            return user_input

if __name__ == "__main__":
    game = PokerHoldem()
    game.start_game()
