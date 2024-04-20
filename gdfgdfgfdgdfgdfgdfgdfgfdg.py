import random
import time
import json

def validate_string(prompt):
    while True:
        user_input = input(prompt)
        if not user_input.replace(" ", "").isalpha() or not user_input.istitle():
            print("Se debe empezar con Mayuscula y  deben ser letras ")
        else:
            return user_input

human_player = validate_string("Ingrese su nombre: ")

player = []
bot = []
table = []
player_chips = {}
bot_chips = {}
current_bet = 0
pot = 0
big_blind = 10
small_blind = 5
dealer_position = 0  # Posición del dealer (boton del dealer), inicia en el jugador 0


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


def save_scores(winner, chips_won):
    try:
        with open("score.json", "r") as file:
            scores = json.load(file)
            print("Puntuaciones cargadas:", scores)  # Agrega esta línea para depurar
    except FileNotFoundError:
        print("Archivo 'score.json' no encontrado.")
        scores = []

    scores.append({"nombre": winner, "fichas": chips_won})

    with open("score.json", "w") as file:
        json.dump(scores, file)

def show_scores():
    try:
        with open("score.json", "r") as file:
            scores = json.load(file)
            print("----- Puntuaciones -----")
            for score in scores:
                print(f"Nombre: {score['nombre']}, Fichas: {score['fichas']}")
    except FileNotFoundError:
        print("No hay puntuaciones guardadas.")


def exit_game():
    print("Saliendo del sistema")
    exit()


def chip_conversion(player_fichas):
    denominations = {
        "blanca(1$)": 1,
        "roja(5$)": 5,
        "azul(10$)": 10,
        "verde(25$)": 25,
        "negra(100$)": 100
    }
    chips_dict = {}

    remaining_chips = player_fichas
    for denomination, value in denominations.items():
        max_chips = min(remaining_chips // value, 20)
        chips = random.randint(0, max_chips)
        chips_dict[denomination] = chips
        remaining_chips -= chips * value

    if remaining_chips > 0:
        min_denomination = min(denominations.values())
        chips_dict["blanca(1$)"] += remaining_chips // min_denomination

    return chips_dict


def show_initial_chips(human_player):
    initial_chips = 500  # Cantidad inicial de fichas para cada jugador
    global player_chips, bot_chips
    player_chips = chip_conversion(initial_chips)
    bot_chips = chip_conversion(initial_chips)
    print("\n|------------------------------------------|")
    print(f"|{human_player}, tiene las siguientes fichas ")
    for key, value in player_chips.items():
        print(f"|{key}: {value} ficha(s)")
    print("|               TOTAL ($500)               ")
    print("|------------------------------------------|")

    print("\n|------------------------------------------|")
    print("|Sheldon Cooper, tiene las siguientes fichas ")
    for key, value in bot_chips.items():
        print(f"|{key}: {value} ficha(s)")
    print("|               TOTAL ($500)               ")
    print("|------------------------------------------|\n")
    print("Empezando el juego en 1 segundo...\n")
    time.sleep(1)

def create_shuffle_deck():
    with open("baraja.txt", "r") as file:
        cards = file.readlines()
        deck = [card.strip() for card in cards]
        random.shuffle(deck)
        return deck


def deal_cards_for_player(num_cards):
    deck = create_shuffle_deck()
    return [deck.pop() for _ in range(num_cards)]  # Saca las cartas del mazo mezclado


def deal_cards_for_players(num_player, num_bot, num_table):
    global player, bot
    cards_player = deal_cards_for_player(num_cards=num_player)
    player.extend(cards_player)
    cards_cpu = deal_cards_for_player(num_cards=num_bot)
    bot.extend(cards_cpu)
    cards_table = deal_cards_for_player(num_cards=num_table)
    table.extend(cards_table)


def play_game():
    play_round(1, 2, 2, 0)
    play_round(2, 0, 0, 3)
    play_round(3, 0, 0, 1)
    play_round(4, 0, 0, 1)


def play_round(round_num, num_player, num_bot, num_table):
    global pot, current_bet
    print("--------------------------------------------")
    print(f"                 RONDA {round_num} ")
    print("--------------------------------------------")
    deal_cards_for_players(num_player, num_bot, num_table)
    print(f"Cartas de {human_player}: {player}")
    print(f"Fichas de {human_player}: {player_chips}")
    print("--------------------------------------------")
    print("Cartas de Sheldon Cooper: Incognito, Incognito", )
    print(f"Fichas de Sheldon Cooper: {bot_chips}")
    print("--------------------------------------------")
    # Mostrar las cartas comunitarias
    print("Cartas comunitarias:", table)
    print(f"Fichas en juego: {pot}")
    print("--------------------------------------------")
    # Actualizar el bote (pot)
    pot += current_bet

    # Aplicar las ciegas (blinds)
    if round_num == 1:
        apply_blinds()

    # Turno del jugador humano
    print("\n             Turno de", human_player)
    while True:
        print("\n|------------------------------------------|")
        print("|          Opciones de apuesta             |")
        print("|               1. Call                    |")
        print("|               2. Raise                   |")
        print("|               3. Fold                    |")
        print("|               4. All-In                  |")
        print("|------------------------------------------|")

        action = input("Seleccione una acción (1-4): ").lower()
        if action == "1":
            call(human_player)
            break
        elif action == "2":
            amount = int(input("Ingrese la cantidad para subir: "))
            raisee(amount, human_player)
            break
        elif action == "3":
            fold(human_player)
            break
        elif action == "4":
            all_in(player)
            break
        else:
            print("Opción no válida. Intente nuevamente.")

        # Turno del bot
    print("\n           Turno de Sheldon Cooper")
    bot_action = random.choice(["1", "2", "3", "4"])
    print("Sheldon Cooper seleccionó:", bot_action)

    if bot_action == "1":
        call("Sheldon Cooper")
    elif bot_action == "2":
        max_raise_amount = min(current_bet + sum(player_chips.values()), sum(player_chips.values()))
        if current_bet == 0:  # Asegurarse de que current_bet tenga un valor válido
            current_bet = big_blind  # Asignar la ciega grande como apuesta inicial
        amount = random.randint(current_bet, max_raise_amount)
        raisee(amount, "Sheldon Cooper")

    elif bot_action == "4":
        all_in("Sheldon Cooper")


def call(player):
    global player_chips, bot_chips, current_bet, pot
    if player == human_player:
        chips_to_call = current_bet - player_chips["blanca(1$)"]
    else:
        chips_to_call = current_bet - bot_chips["blanca(1$)"]

    if chips_to_call <= 0:
        print(f"{player} ya ha igualado la apuesta.")
        print(f"Fichas en juego: {pot}")
        return


    if player_chips["blanca(1$)"] < chips_to_call:
        print("No tienes suficientes fichas para igualar la apuesta.")
        all_in_amount = player_chips["blanca(1$)"]
        player_chips["blanca(1$)"] = 0
        pot += all_in_amount
        print(f"{player} va All-In con {all_in_amount} fichas para seguir jugando.")
        print(f"Fichas en juego: {pot}")
    else:
        player_chips["blanca(1$)"] -= chips_to_call
        pot += chips_to_call
        print(f"{player} iguala la apuesta de {chips_to_call} fichas.")
        print(f"Fichas en juego: {pot}")

def raisee(amount, player):
    global player_chips, current_bet, pot
    if player_chips["blanca(1$)"] < amount:
        print("No tienes suficientes fichas para subir la apuesta.")
        all_in_amount = player_chips["blanca(1$)"]
        player_chips["blanca(1$)"] = 0
        current_bet += all_in_amount
        pot += all_in_amount
        print(f"{player} va All-In con {all_in_amount} fichas para seguir jugando.")
        print(f"Fichas en juego: {pot}\n")
    else:
        player_chips["blanca(1$)"] -= amount
        current_bet += amount
        pot += amount
        print(f"{player} hace raise de {amount}.")
        print(f"Fichas en juego: {pot}\n")

def fold(player_name):
    global player_chips, bot_chips, pot, current_bet
    if player_name == human_player:
        print(f"{player_name} se retira. Sheldon Cooper gana la partida.")
        bot_chips["blanca(1$)"] += pot
    else:
        print(f"{player_name} se retira. {human_player} gana la partida.")
        player_chips["blanca(1$)"] += pot
    print(f"Suma de lo apostado por ambos jugadores: {pot + current_bet}")
    total_winnings = sum(player_chips.values())
    print(f"{player_name} ganó un total de {total_winnings} fichas.")
    exit_game()

def all_in(player):
    global pot, player_chips, bot_chips, current_bet
    all_in_amount = sum(player_chips.values()) if player == human_player else sum(bot_chips.values())
    if player == human_player:
        player_chips = {denomination: 0 for denomination in player_chips}
    else:
        bot_chips = {denomination: 0 for denomination in bot_chips}
    pot += all_in_amount
    current_bet += all_in_amount
    print(f"{player} va All In con {all_in_amount} fichas.")
    print(f"Fichas en juego: {pot}")

def apply_blinds():
    global player_chips, current_bet, pot
    # Aplicar la ciega pequeña (small blind)
    player_chips["blanca(1$)"] -= small_blind
    current_bet = small_blind
    pot += small_blind
    print(f"{human_player} pone la ciega pequeña de {small_blind} fichas.")

    # Aplicar la ciega grande (big blind)
    bot_chips["blanca(1$)"] -= big_blind
    current_bet = big_blind
    pot += big_blind
    print(f"Sheldon Cooper pone la ciega grande de {big_blind} fichas.")
    print(f"Fichas en juego: {pot}")
    print("--------------------------------------------")


def evaluate_hands(cards_player, cards_opponent):
    card_values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13,
                   'A': 14}

    def pair(hand):
        card_values = [card[0] for card in hand]
        for value in card_values:
            if card_values.count(value) == 2:
                return True
        return False

    def four_of_a_kind(hand):
        card_values = [card[0] for card in hand]
        for value in card_values:
            if card_values.count(value) == 4:
                return True
        return False

    def full_house(hand):
        return three_of_a_kind(hand) and pair(hand)

    def straight(hand):
        sorted_values = sorted(
            [card_values[card.split()[0]] if card.split()[0] in card_values else int(card.split()[0]) for card in hand])
        return len(set(sorted_values)) == 5 and (sorted_values[-1] - sorted_values[0] == 4)

    def two_pairs(hand):
        card_values = [card[0] for card in hand]
        pairs = 0
        for value in card_values:
            if card_values.count(value) == 2:
                pairs += 1
        return pairs == 2

    def three_of_a_kind(hand):
        card_values = [card[0] for card in hand]
        for value in card_values:
            if card_values.count(value) == 3:
                return True
        return False

    def flush(hand):
        suit = hand[0][1]
        return all(card[1] == suit for card in hand)

    def evaluate_best_hand(hand):
        if straight(hand) and flush(hand):
            return "Escalera de Color!"
        elif three_of_a_kind(hand):
            return "Tres Iguales!"
        elif pair(hand):
            return "Par!"
        elif full_house(hand):
            return "Full House"
        elif two_pairs(hand):
            return "Dos par!"
        elif flush(hand):
            return "Color!"
        elif straight(hand):
            return "Escalera"
        elif four_of_a_kind(hand):
            return "Cuatro Iguales!"
        else:
            return "Carta Alta!"

    best_hand_human_player = evaluate_best_hand(cards_player + table)
    best_hand_bot_opponent = evaluate_best_hand(cards_opponent + table)

    if best_hand_human_player == best_hand_bot_opponent:
        highest_card_human_player = max(
            [card_values[card.split()[0]] if card.split()[0] in card_values else int(card.split()[0]) for card in
             cards_player + table])
        highest_card_bot_opponent = max(
            [card_values[card.split()[0]] if card.split()[0] in card_values else int(card.split()[0]) for card in
             cards_opponent + table])
        if highest_card_human_player > highest_card_bot_opponent:
            return human_player
        elif highest_card_human_player < highest_card_bot_opponent:
            return "Sheldon Cooper"
        else:
            return "Empate"
    elif best_hand_human_player > best_hand_bot_opponent:
        return human_player
    else:
        return "Sheldon Cooper"


def start_game():
    global pot, current_bet
    show_initial_chips(human_player)
    play_game()
    winner = evaluate_hands(player, bot)
    print(f"\n{human_player}: {player}")
    print(f"Sheldon Cooper: {bot} ")
    print(f"Fichas Comunitarias: {table}\n")
    print(f"Ganador de la partida: {winner}")
    exit_game()


main()