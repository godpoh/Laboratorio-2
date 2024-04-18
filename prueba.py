import random

class PokerGame:
    def __init__(self):
        self.players = {}
        self.deck = []

    def show_main_menu(self):
        print("|------------------------------------------|")
        print("|    Bienvenido al juego POKER HOLD'EM     |")
        print("|        1. Iniciar Juego                  |")
        print("|        2. Mostrar puntuaciones           |")
        print("|        3. Salir                          |")
        print("|------------------------------------------|")

    def options_menu(self, selection):
        if selection == "1":
            self.start_game()
        elif selection == "2":
            self.show_califications()
        elif selection == "3":
            self.exit_game()
        else:
            print("\nOpcion invalida. Intente de nuevo\n")

    def start_game(self):
        community_cards = self.initial_deal_cards()

        for player, data in self.players.items():
            self.show_initial_chips(player, self.chip_conversion(data["fichas"]), data["cartas"])

        self.play_game_round(community_cards)

    def show_califications(self):
        pass

    def exit_game(self):
        print("Saliendo del sistema")
        exit()

    def show_player_cards(self, player_name, cards):
        print(f"{player_name} tus cartas son: ")
        for card in cards:
            print(card)

    def validate_string_name_input(self, prompt):
        while True:
            user_input = input(prompt)
            if not user_input.replace(" ", "").isalpha() or not user_input.istitle():
                print("Debe ser un nombre con solo letras, ademas debe empezar con una mayuscula inicial")
                continue
            return user_input

    def create_shuffle_deck(self):
        with open("baraja.txt", "r") as file:
            cards = file.readlines()
            deck = [card.strip() for card in cards]
            random.shuffle(deck)
            return deck

    def initial_deal_cards(self):
        self.deck = self.create_shuffle_deck()
        player_name = self.validate_string_name_input("Ingrese su nombre: ")
        self.players[player_name] = {"fichas": 500, "cartas": []}
        self.players["Sheldon Cooper"] = {"fichas": 500, "cartas": []}

        for player, data in self.players.items():
            self.show_initial_chips(player, self.chip_conversion(data["fichas"]), data["cartas"])

        print("Se les quita a los jugadores $25 (1 ficha verde) como pago inicial")

        for player in self.players:
            self.players[player]["fichas"] -= 25
            for _ in range(2):
                dealt_card = self.deck.pop()
                self.players[player]["cartas"].append(dealt_card)

        table = []
        for _ in range(5):
            table.append(self.deck.pop())

        return table

    def chip_conversion(self, player_name):
        denominations = {
            "blanca(1$)": 1,
            "roja(5$)": 5,
            "azul(10$)": 10,
            "verde(25$)": 25,
            "negra(100$)": 100
        }
        players_chips = {}

        remaining_chips = 500
        for denomination, value in denominations.items():
            max_chips = min(remaining_chips // value, 20)
            chips = random.randint(0, max_chips)
            players_chips[denomination] = chips
            remaining_chips -= chips * value

        if remaining_chips > 0:
            min_denomination = min(denominations.values())
            players_chips["blanca(1$)"] += remaining_chips // min_denomination

        return players_chips

    def show_initial_chips(self, player_name, initial_chips, cards):
        print("\n|------------------------------------------|")
        print(f"|{player_name}, tiene las siguientes fichas ")
        for denomination, count in initial_chips.items():
            print(f"|{count} ficha(s) de {denomination:10}")
        print("|               TOTAL ($500)               ")
        print("|------------------------------------------|\n")
        if cards:
            print(f"{player_name} tus cartas son: ")
            for card in cards:
                print(card)

    def call_option_fold(self, last_move, player_data, opponent_data):
        while True:
            print("|------------------------------------------|")
            if last_move == "1":
                print("|                1. Call                   |")
            else:
                print("|                1. Check                  |")
            if last_move == "2":
                print("|                2. Raise                  |")
            else:
                print("|                2. Bet                    |")
            print("|                3. Fold                   |")
            print("|                4. All in                 |")
            print("|------------------------------------------|")

            option = input("Ingrese el próximo movimiento: ")

            if option == "1":
                if last_move == "1":
                    self.call(player_data, opponent_data)
                else:
                    self.check(player_data)
            elif option == "2":
                if last_move == "2":
                    self.raaise(player_data, opponent_data)
                else:
                    self.bet()
            elif option == "3":
                self.fold(player_data)
                break
            elif option == "4":
                self.all_in(player_data)
            else:
                print("Opcion invalida")

            if option in ["1", "2", "3", "4"]:
                break

    def turn_players(self, current_player, player_data, opponent_data):
        if 'apuesta' not in player_data:
            player_data['apuesta'] = 0

        is_player_turn = True
        while True:
            if is_player_turn:
                print("\nTu turno!\n")
                self.call_option_fold("1", player_data, opponent_data)
            else:
                print("\nTurno de Sheldon Cooper")
                sheldon_move = self.sheldon_decide_move(opponent_data["cartas"])
                print("Sheldon Cooper selecciono: ", sheldon_move)
                if sheldon_move == "3":
                    fold_message = self.fold(opponent_data)
                    if fold_message is None:
                        return current_player
                    print(fold_message)
                    return "Sheldon Cooper"

                self.call_option_fold(sheldon_move, opponent_data, player_data)

            is_player_turn = not is_player_turn

    def sheldon_decide_move(self, sheldon_cards):
        return random.choice(["1", "2", "3", "4"])

    def call(self, player_data, opponent_data):
        player_bet = player_data.get("apuesta", 0)
        opponent_bet = opponent_data.get("apuesta", 0)
        amount_to_call = opponent_bet - player_bet

        if player_data["fichas"] < amount_to_call:
            print("No tienes suficientes fichas para igualar la apuesta:")
            return

        player_data["apuesta"] = opponent_bet
        player_data["fichas"] -= amount_to_call

        opponent_data["fichas"] -= amount_to_call

        print(f"Has igualado la apuesta de {amount_to_call} fichas")

    def check(self, player_data):
        if 'fichas' in player_data:
            maxbid = player_data["fichas"]
            print(f"Fichas del jugador: {maxbid}")
        else:
            print("Error: 'fichas' no esta definido en el diccionario player_data")

    def raaise(self, player_data, opponent_data):
        while True:
            try:
                raise_amount = int(input("Ingrese la cantidad que desea subir la apuesta: "))
                if raise_amount <= 0:
                    print("La cantidad debe ser mayor que cero.")
                    continue
                elif raise_amount > player_data["fichas"]:
                    print("No tienes suficientes fichas para subir esa cantidad.")
                    continue
                else:
                    break
            except ValueError:
                print("Por favor, ingrese un número entero.")

        player_data["apuesta"] += raise_amount
        player_data["fichas"] -= raise_amount

        opponent_data["fichas"] += raise_amount

        print(f"Has subido la apuesta en {raise_amount} fichas.")

    def fold(self, player_data):
        for player_name, player_info in player_data.items():
            if isinstance(player_info, dict) and "fichas" in player_info:
                if player_info["fichas"] == 0:
                    print(f"{player_name} se retiró del juego.")
                else:
                    print(f"{player_name} se retiró del juego con {player_info['fichas']} fichas.")

        if "Sheldon Cooper" in player_data:
            sheldon_chips = player_data["Sheldon Cooper"]["fichas"]
            player_data["Sheldon Cooper"]["fichas"] = 0
            player_data[player_name]["fichas"] += sheldon_chips

        return None

    def bet(self):
        print("El jugador hizo un Bet!")

    def all_in(self, player_data):
        print("El jugador hizo un All-in!")
        player_data["fichas"] = 0

    def river_betting_round(self, cards, player_data):
        river = []

        if len(cards) > 0:
            print("Flop:")
            for _ in range(3):
                river.append(cards.pop())
            print("Cartas en el río después del flop:", river)
            self.call_option_fold("3", player_data, {})

            print("Cartas en el río:", river)

        if len(cards) > 0:
            print("Turn:")
            river.append(cards.pop())
            print("Cartas en el río después del turn:", river)
            self.call_option_fold("3", player_data, {})

            print("Cartas en el río:", river)

        if len(cards) > 0:
            print("River:")
            river.append(cards.pop())
            print("Cartas en el río después del river:", river)
            self.call_option_fold("3", player_data, {})

            print("Cartas en el río:", river)
        else:
            print("No hay cartas en el river")

        print("Cartas del río:", river)

    def play_game_round(self, community_cards):
        pre_flop_finished = False
        round_count = 0

        while round_count < 4:
            round_count += 1
            if not pre_flop_finished:
                winner = self.turn_players(list(self.players.keys())[0], self.players[list(self.players.keys())[0]],
                                           self.players["Sheldon Cooper"])
                pre_flop_finished = True
            else:
                cards_on_table = []
                if round_count == 1:
                    print("\nFlop:")
                    for _ in range(3):
                        if self.deck:
                            cards_on_table.append(self.deck.pop())
                    if cards_on_table:
                        print("Cartas en el río:", cards_on_table)
                        self.river_betting_round(cards_on_table, self.players)
                        # Después del flop, turno de Sheldon Cooper
                        winner = self.turn_players("Sheldon Cooper", self.players["Sheldon Cooper"], self.players["J"])
                elif round_count == 2:
                    print("\nTurn:")
                    if self.deck:
                        cards_on_table.append(self.deck.pop())
                    if cards_on_table:
                        print("Cartas en el río:", cards_on_table)
                        self.river_betting_round(cards_on_table, self.players)
                elif round_count == 3:
                    print("\nRiver:")
                    if self.deck:
                        cards_on_table.append(self.deck.pop())
                    if cards_on_table:
                        print("Cartas en el río:", cards_on_table)
                        self.river_betting_round(cards_on_table, self.players)

        if winner == "Sheldon Cooper":
            print("\n¡Sheldon Cooper es el ganador!")
        else:
            print(f"\n¡{winner} es el ganador!")

        return winner

game = PokerGame()
while True:
    game.show_main_menu()
    selection = input("Ingrese la opcion que desee: ")
    game.options_menu(selection)
