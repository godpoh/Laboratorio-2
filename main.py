import json
import random

def show_main_menu():
    print("|------------------------------------------|")
    print("|    Bienvenido al juego POKER HOLD'EM     |")
    print("|        1. Iniciar Juego                  |")
    print("|        2. Mostrar puntuaciones           |")
    print("|        3. Salir                          |")
    print("|------------------------------------------|")

def main():
    while True:
        show_main_menu()
        selection = input("Ingrese la opcion que desee: ")
        options_menu(selection)

def options_menu(selection):
    if selection == "1":
        start_game()
    elif selection == "2":
        show_califications()
    elif selection == "3":
        exit_game()
    else:
        print("\nOpcion invalida. Intente de nuevo\n")

def start_game():
    player_name = validate_string_name_input("Ingrese su nombre: ")
    shuffle_deck = create_shuffle_deck()
    players, table = initial_deal_cards(shuffle_deck, player_name)

    for player, data in players.items():
        if player == player_name:
            show_player_cards(player, data["cartas"])  # Mostrar las cartas solo para el jugador humano

    play_game_round(players, table, shuffle_deck, player_name)

def show_califications():
    pass

def exit_game():
    print("Saliendo del sistema")
    exit()

def show_player_cards(player_name, cards):
    print(f"{player_name}, tus cartas son: ")
    for card in cards:
        print(card)

def validate_string_name_input(prompt):
    while True:
        user_input = input(prompt)
        if not user_input.replace(" ","").isalpha() or not user_input.istitle():
            print("Debe ser un nombre con solo letras, ademas debe empezar con una mayuscula inicial")
            continue
        return user_input

def create_shuffle_deck():
    with open("baraja.txt", "r") as file:
        cards = file.readlines()
        deck = [card.strip() for card in cards]
        random.shuffle(deck)
        return deck

def initial_deal_cards(deck, player_name):
    players = {}

    players[player_name] = {"fichas": 500, "cartas": []}
    players["Sheldon Cooper"] = {"fichas": 500, "cartas": []}

    for player, data in players.items():
        show_initial_chips(player, chip_conversion(data["fichas"]), data["cartas"])

    print("Se les quita a los jugadores $25 (1 ficha verde) como pago inicial")

    for player in players:
        players[player]["fichas"] -= 25
        for x in range(2):
            dealt_card = deck.pop()
            players[player]["cartas"].append(dealt_card)

    table = []
    for x in range(5):
        table.append(deck.pop())

    return players, table

def chip_conversion(player_fichas):
    denominations = {
        "blanca(1$)": 1,
        "roja(5$)": 5,
        "azul(10$)": 10,
        "verde(25$)": 25,
        "negra(100$)": 100
    }
    players_chips = {}

    remaining_chips = player_fichas
    for denomination, value in denominations.items():
        max_chips = min(remaining_chips // value, 20)
        chips = random.randint(0, max_chips)
        players_chips[denomination] = chips
        remaining_chips -= chips * value

    if remaining_chips > 0:
        min_denomination = min(denominations.values())
        players_chips["blanca(1$)"] += remaining_chips // min_denomination

    return players_chips

def show_initial_chips(player_name, initial_chips, cards ):
    print("\n|------------------------------------------|")
    print(f"|{player_name}, tiene las siguientes fichas ")
    for denomination, count in initial_chips.items():
        print(f"|{count} ficha(s) de {denomination:10}")
    print("|               TOTAL ($500)               ")
    print("|------------------------------------------|\n")
    if cards:
        print(f"{player_name}, tus cartas son: ")
        for card in cards:
            print(card)

def call_option_fold(last_move, player_data, player_name):
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
                call(player_data)
            else:
                check(player_data)
        elif option == "2":
            if last_move == "2":
                bet()
            else:
                raaise(player_data)
        elif option == "3":
            fold(player_data, player_name)
            break
        elif option == "4":
            all_in(player_data)
        else:
            print("Opción inválida")

        if option in ["1", "2", "3", "4"]:
            break

def evaluate_hands(cards_player, cards_opponent):
    values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}

    def has_pair(hand):
        card_values = [card[0] for card in hand]
        for value in card_values:
            if card_values.count(value) == 2:
                return True
        return False

    def has_two_pairs(hand):
        card_values = [card[0] for card in hand]
        pairs = 0
        for value in card_values:
            if card_values.count(value) == 2:
                pairs += 1
        return pairs == 2

    def has_three_of_a_kind(hand):
        card_values = [card[0] for card in hand]
        for value in card_values:
            if card_values.count(value) == 3:
                return True
        return False

    def has_straight(hand):
        sorted_values = sorted([values[card.split()[0]] if card.split()[0] in values else int(card.split()[0]) for card in hand])
        return len(set(sorted_values)) == 5 and (sorted_values[-1] - sorted_values[0] == 4)

    def has_flush(hand):
        suit = hand[0][1]
        return all(card[1] == suit for card in hand)

    def has_full_house(hand):
        return has_three_of_a_kind(hand) and has_pair(hand)

    def has_four_of_a_kind(hand):
        card_values = [card[0] for card in hand]
        for value in card_values:
            if card_values.count(value) == 4:
                return True
        return False

    def determine_best_hand(hand):
        if has_straight(hand) and has_flush(hand):
            return "Straight Flush"
        elif has_four_of_a_kind(hand):
            return "Four of a Kind"
        elif has_full_house(hand):
            return "Full House"
        elif has_flush(hand):
            return "Flush"
        elif has_straight(hand):
            return "Straight"
        elif has_three_of_a_kind(hand):
            return "Three of a Kind"
        elif has_two_pairs(hand):
            return "Two Pairs"
        elif has_pair(hand):
            return "Pair"
        else:
            return "High Card"

    best_hand_player = determine_best_hand(cards_player)
    best_hand_opponent = determine_best_hand(cards_opponent)

    if best_hand_player == best_hand_opponent:
        highest_card_player = max([values[card.split()[0]] if card.split()[0] in values else int(card.split()[0]) for card in cards_player])
        highest_card_opponent = max([values[card.split()[0]] if card.split()[0] in values else int(card.split()[0]) for card in cards_opponent])
        if highest_card_player > highest_card_opponent:
            return "Jugador Humano"
        elif highest_card_player < highest_card_opponent:
            return "Sheldon Cooper"
        else:
            return "Empate"
    elif best_hand_player > best_hand_opponent:
        return "Jugador Humano"
    else:
        return "Sheldon Cooper"

def play_betting_round(players, table, current_player, player_name):
    if 'apuesta' not in players[player_name]:
        players[player_name]['apuesta'] = 0

    is_player_turn = True
    while True:
        if is_player_turn:
            print("\nTu turno!\n")
            call_option_fold("1", players[player_name], player_name)
        else:
            print("\nTurno de Sheldon Cooper")
            sheldon_move = sheldon_decide_move(players["Sheldon Cooper"]["cartas"], table)
            print("Sheldon Cooper seleccionó:", sheldon_move)
            if sheldon_move == "3":
                fold_message = fold(players[player_name], current_player)
                if fold_message is None:
                    return current_player
                print(fold_message)
                return "Sheldon Cooper"
            call_option_fold(sheldon_move, players[player_name], player_name)
        is_player_turn = not is_player_turn

        # Verificar si el juego ha terminado
        if len(table) == 5:
            cards_player = players[player_name]["cartas"] + table
            cards_opponent = players["Sheldon Cooper"]["cartas"] + table
            winner = evaluate_hands(cards_player, cards_opponent)
            return winner

    # Una vez que ambos jugadores han tomado sus decisiones, procedemos a la ronda de apuestas del río
    river = []
    for round_name in ["Flop", "Turn", "River"]:
        if len(table) > 0:
            print(round_name + ":")
            if round_name == "River":
                river.append(table.pop())
            else:
                for _ in range(3 if round_name == "Flop" else 1):
                    river.append(table.pop())
            print("Cartas en el río después de", round_name + ":", river)
            call_option_fold("3", players[player_name], player_name)

    print("Cartas del río:", river)

def sheldon_decide_move():
    return random.choice(["1", "2", "3", "4"])

def call(player_data):
    player_bet = player_data.get("apuesta", 0)
    opponent_bet = 25

    amount_to_call = opponent_bet - player_bet

    if player_data["fichas"] < amount_to_call:
        print("No tienes suficientes fichas para igualar la apuesta.")
        return

    player_data["apuesta"] = opponent_bet
    player_data["fichas"] -= amount_to_call

    print(f"Has igualado la apuesta de {amount_to_call} fichas")

def check(player_data):
    if 'fichas' in player_data:
        maxbid = player_data["fichas"]
        print(f"Fichas del jugador: {maxbid}")
    else:
        print("Error: 'fichas' no está definido en el diccionario player_data")

def raaise(player_data):
    while True:
        try:
            raise_amount = int(input("Ingrese la cantidad que desea subir la apuesta: "))
            if raise_amount <= 0:
                print("La cantidad debe1 ser mayor que cero.")
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

    print(f"Has subido la apuesta en {raise_amount} fichas.")

def fold(player_data, player_name):
    if not player_name == "Sheldon Cooper":
        print("Sheldon Cooper se retiro del juego")
    else:
        print(f"{player_name} se retiro del juego")

def bet():
    print("El jugador hizo un Bet!")

def all_in(player_data):
    print("El jugador hizo un All-in!")
    player_data["fichas"] = 0

def play_game_round(players, table, deck, player_name):
    pre_flop_finished = False

    while True:
        if not pre_flop_finished:
            winner = play_betting_round(players, table, list(players.keys())[0], player_name)
            pre_flop_finished = True
        else:
            if len(table) < 5:
                for round_name in ["Flop", "Turn", "River"]:
                    if round_name == "River":
                        table.append(deck.pop())
                    else:
                        for x in range(3 if round_name == "Flop" else 1):
                            table.append(deck.pop())
                    print(f"{round_name}: {table}")
                winner = play_betting_round(players, table, list(players.keys())[0], player_name)
            else:
                break

        if winner == "Sheldon Cooper":
            print("\n¡Sheldon Cooper es el ganador!")
        elif winner == "Empate":
            print("Empate, ninguno de los 2 gana!")
        else:
            print(f"\n¡{winner} es el ganador!")

main()




