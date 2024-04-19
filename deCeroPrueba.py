import random

human_player = input("Ingrese su nombre: ")
player = []
bot = []
table = []
big_blind = 25
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

def show_scores():
    pass

def exit_game():
    print("Saliendo del sistema")
    exit()


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
    player.extend(cards_table)
    bot.extend(cards_table)

#Tanto PLAY_GAME,PLAY_ROUND,deal_cards_for_players CONFORMAN LAS RONDAS Y AGREGAR CARTAS A LOS JUGADORES

def play_game():
    play_round(1, 2, 2, 0)
    play_round(2, 0, 0, 3)
    play_round(3, 0, 0, 1)
    play_round(4, 0, 0, 1)

def play_round(round_num, num_player, num_bot, num_table):
    print(f"{round_num} ronda")
    deal_cards_for_players(num_player, num_bot, num_table)
    print(f"{human_player}:", player)
    print("Sheldon Cooper:", bot)

#chip_conversion y show_initial_chips son los encargados de otorgar las fichas y de mostrarlas
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

def show_initial_chips(human_player):
    initial_chips = 500  # Cantidad inicial de fichas para cada jugador
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

def evaluate_hands(cards_player, cards_opponent):
    card_values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
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
        sorted_values = sorted([card_values[card.split()[0]] if card.split()[0] in card_values else int(card.split()[0]) for card in hand])
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

    best_hand_human_player = evaluate_best_hand(cards_player)
    best_hand_bot_opponent = evaluate_best_hand(cards_opponent)

    if best_hand_human_player == best_hand_bot_opponent:
        highest_card_human_player = max([card_values[card.split()[0]] if card.split()[0] in card_values else int(card.split()[0]) for card in cards_player])
        highest_card_bot_opponent = max([card_values[card.split()[0]] if card.split()[0] in card_values else int(card.split()[0]) for card in cards_opponent])
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
    play_game()
    show_initial_chips(human_player)
    winner = evaluate_hands(player, bot)
    print(f"Ganador de la partida: {winner}")
    exit_game()





def call():
    global player_chips, current_bet, pot
    if player_chips < current_bet:
        print("No tienes suficientes fichas para igualar la apuesta.")
    else:
        chips_to_call = current_bet - big_blind
        player_chips -= chips_to_call
        pot += chips_to_call
        print(f"{human_player} hace call.")


def raisee(amount):
    global player_chips, current_bet, pot
    if player_chips < amount:
        print("No tienes suficientes fichas para subir la apuesta.")
    else:
        player_chips -= amount
        current_bet += amount
        pot += amount
        print(f"{human_player} hace raise de {amount}.")


def fold():
    print(f"{human_player} se retira.")


def all_in():
    global player_chips, current_bet, pot
    if player_chips < current_bet:
        all_in_amount = player_chips
    else:
        all_in_amount = player_chips + current_bet
    player_chips = 0
    pot += all_in_amount
    print(f"{human_player} va All In con {all_in_amount} fichas.")


main()