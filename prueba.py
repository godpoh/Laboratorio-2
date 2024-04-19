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
        show_scores()
    elif selection == "3":
        exit_game()
    else:
        print("\nOpcion invalida. Intente de nuevo\n")

def start_game():
    human_player = validate_string_name_input("Ingrese su nombre: ")
    shuffle_deck = create_shuffled_deck()
    players, table = deal_initial_cards(shuffle_deck, human_player)

    for player, data in players.items():
        if player == human_player:
            show_player_cards(player, data["cartas"])

    current_player = next(iter(players))

    play_game_round(players, current_player)

def show_scores():
    pass

def exit_game():
    print("Saliendo del sistema")
    exit()

def show_player_cards(human_player, cards):
    print(f"{human_player}, tus cartas son: ")
    for card in cards:
        print(card)

def validate_string_name_input(prompt):
    while True:
        user_input = input(prompt)
        if not user_input.replace(" ", "").isalpha() or not user_input.istitle():
            print("Debe ser un nombre con solo letras, ademas debe empezar con una mayuscula inicial")
            continue
        return user_input

def create_shuffled_deck():
    with open("baraja.txt", "r") as file:
        cards = file.readlines()
        deck = [card.strip() for card in cards]
        random.shuffle(deck)
        return deck

def deal_initial_cards(deck, player_name):
    players = {}

    players[player_name] = {"fichas": 500, "cartas": []}
    players["Sheldon Cooper"] = {"fichas": 500, "cartas": []}

    for player, data in players.items():
        show_initial_chips(player, chip_conversion(data["fichas"]))

    for player in players:
        players[player]["fichas"] -= 25
        for _ in range(2):
            dealt_card = deck.pop()
            players[player]["cartas"].append(dealt_card)

    print("Se les otorgo a los jugadores 2 cartas y se les fue quitados $25, (1 ficha verde):\n ")

            # print(players) # Comprobar que se este entregando las 2 cartas a los jugadores

    table = [deck.pop() for _ in range(5)]

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


def show_initial_chips(human_player, initial_chips):
    print("\n|------------------------------------------|")
    print(f"|{human_player}, tiene las siguientes fichas ")
    for denomination, count in initial_chips.items():
        print(f"|{count} ficha(s) de {denomination:10}")
    print("|               TOTAL ($500)               ")
    print("|------------------------------------------|\n")


def evaluate_hands(cards_player, cards_opponent):
    values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
    def has_pair(hand):
        card_values = [card[0] for card in hand]
        for value in card_values:
            if card_values.count(value) == 2:
                return True
        return False

    def has_four_of_a_kind(hand):
        card_values = [card[0] for card in hand]
        for value in card_values:
            if card_values.count(value) == 4:
                return True
        return False

    def has_full_house(hand):
        return has_three_of_a_kind(hand) and has_pair(hand)

    def has_straight(hand):
        sorted_values = sorted([values[card.split()[0]] if card.split()[0] in values else int(card.split()[0]) for card in hand])
        return len(set(sorted_values)) == 5 and (sorted_values[-1] - sorted_values[0] == 4)
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

    def has_flush(hand):
        suit = hand[0][1]
        return all(card[1] == suit for card in hand)

    def determine_best_hand(hand):
        if has_straight(hand) and has_flush(hand):
            return "Escalera de Color!"
        elif has_three_of_a_kind(hand):
            return "Tres Iguales!"
        elif has_pair(hand):
            return "Par!"
        elif has_full_house(hand):
            return "Full House"
        elif has_two_pairs(hand):
            return "Dos par!"
        elif has_flush(hand):
            return "Color!"
        elif has_straight(hand):
            return "Escalera"
        elif has_four_of_a_kind(hand):
            return "Cuatro Iguales!"
        else:
            return "Carta Alta!"

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


def play_betting_round(players, current_player):
    # Obtener la cantidad de fichas del jugador actual
    player_chips = players[current_player]["fichas"]

    # Definir las opciones de apuesta
    options = ["1", "2", "3", "4"]
    # 1: Call - Igualar la apuesta actual
    # 2: Raise - Aumentar la apuesta
    # 3: Fold - Retirarse de la mano
    # 4: All in - Apostar todas las fichas restantes

    print("|------------------------------------------|")
    print("|             Ronda de apuestas            |")
    print("|------------------------------------------|")
    print(f"Jugador actual: {current_player}")
    print(f"Fichas disponibles: {player_chips}")

    while True:
        print("|------------------------------------------|")
        print("|          Opciones de apuesta             |")
        print("|                1. Call                   |")
        print("|                2. Raise                  |")
        print("|                3. Fold                   |")
        print("|                4. All in                 |")
        print("|------------------------------------------|")

        option = input("Ingrese su opción: ")

        if option not in options:
            print("Opción inválida. Por favor, elija nuevamente.")
            continue

        if option == "1":  # Call
            # Calcular la cantidad que el jugador necesita igualar
            # y restar esa cantidad de fichas del jugador
            # Implementar lógica para igualar la apuesta actual
            print("El jugador hace un call!")
            break
        elif option == "2":  # Raise
            # Implementar lógica para permitir al jugador aumentar la apuesta
            print("El jugador hace un raise!")
            break
        elif option == "3":  # Fold
            # Implementar lógica para que el jugador se retire de la mano
            print("El jugador se retira!")
            players[current_player]["cartas"] = []  # Retirar las cartas del jugador
            return "fold"  # Retorna "fold" para indicar que el jugador se retiró
        elif option == "4":  # All in
            # Implementar lógica para apostar todas las fichas restantes del jugador
            print("El jugador hace un All-in!")
            break

    # Actualizar la cantidad de fichas del jugador en el diccionario de jugadores
    # Implementar la lógica para transferir fichas, si es necesario

def next_player(players, current_player):
    players_list = list(players.keys())
    current_index = players_list.index(current_player)
    next_index = (current_index + 1) % len(players_list)
    return players_list[next_index]



# Lógica de la ronda de apuestas aquí...


def sheldon_move():
    return random.choice(["1", "2", "3", "4"])


def call():
    print("El jugador hace un call!")


def raaise():
    print("El jugador hizo un raise")


def fold(players, current_player):
    print(f"{current_player} se retiro")
    remaining_chips = players[current_player]["fichas"]
    print(f"Se retira con {remaining_chips} fichas restantes")
    return remaining_chips



def all_in():
    print("El jugador hizo un All-in!")


def play_game_round(players, current_player):
    play_betting_round(players, current_player)




# Lógica para la ronda de juego principal aquí...

main()
