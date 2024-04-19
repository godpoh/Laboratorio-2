import random

# Constantes del juego
initial_chips = 500
big_blind = 25

# Variables globales
human_player = input("Ingrese su nombre: ")
player = []
bot = []
table = []
current_bet = 0
pot = 0
player_chips = initial_chips
bot_chips = initial_chips

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
    return [deck.pop() for _ in range(num_cards)]

def deal_cards_for_players(num_player, num_bot, num_table):
    global player, bot
    cards_player = deal_cards_for_player(num_cards=num_player)
    player.extend(cards_player)
    cards_cpu = deal_cards_for_player(num_cards=num_bot)
    bot.extend(cards_cpu)
    cards_table = deal_cards_for_player(num_cards=num_table)
    player.extend(cards_table)
    bot.extend(cards_table)

def play_game():
    global player, bot, table, current_bet
    while True:
        play_round(1, 2, 2, 0)
        player_decision()
        # Verificar si el jugador ha quedado sin fichas
        if player_chips == 0:
            print(f"{human_player} se ha quedado sin fichas. ¡Juego terminado!")
            exit_game()
        # Verificar si el bot ha quedado sin fichas
        if bot_chips == 0:
            print("Sheldon Cooper se ha quedado sin fichas. ¡Felicidades, has ganado!")
            exit_game()
        # Verificar si el jugador quiere salir del juego
        if input("¿Desea salir del juego? (s/n): ").lower() == 's':
            exit_game()
        # Reiniciar la apuesta para el siguiente round
        current_bet = 0
def play_round(round_num, num_player, num_bot, num_table):
    print(f"{round_num} ronda")
    deal_cards_for_players(num_player, num_bot, num_table)
    print(f"{human_player}:", player)
    print("Sheldon Cooper:", bot)

def player_decision():
    global current_bet, pot
    print(f"Apuesta actual: {current_bet}")
    print(f"Sus fichas: {player_chips}")
    print(f"Apuesta de Sheldon Cooper: {current_bet - big_blind}")
    print("Su turno:")
    print("1. Call")
    print("2. Raise")
    print("3. Fold")
    print("4. All In")
    decision = input("Ingrese su decisión: ")
    if decision == "1":
        call()
    elif decision == "2":
        amount = int(input("Ingrese la cantidad para aumentar la apuesta: "))
        raisee(amount)
    elif decision == "3":
        fold()
    elif decision == "4":
        all_in()

def start_game():
    play_game()

def call():
    global player_chips, current_bet, pot
    if player_chips < current_bet:
        print("No tienes suficientes fichas para igualar la apuesta.")
    else:
        chips_to_call = current_bet - big_blind
        player_chips -= chips_to_call
        pot += chips_to_call
        print(f"{human_player} hace call.")
        next_round()

def raisee(amount):
    global player_chips, current_bet, pot
    if player_chips < amount:
        print("No tienes suficientes fichas para subir la apuesta.")
    else:
        player_chips -= amount
        current_bet += amount
        pot += amount
        print(f"{human_player} hace raise de {amount}.")
        next_round()

def fold():
    print(f"{human_player} se retira.")
    next_round()

def all_in():
    global player_chips, current_bet, pot
    if player_chips < current_bet:
        all_in_amount = player_chips
    else:
        all_in_amount = player_chips + current_bet
    player_chips = 0
    pot += all_in_amount
    print(f"{human_player} va All In con {all_in_amount} fichas.")
    next_round()

def next_round():
    global current_bet
    if len(table) == 0:
        # Ronda de preflop
        play_round(2, 2, 0, 0)  # Por ejemplo, 2 cartas para cada jugador y ninguna para la mesa
    elif len(table) == 3:
        # Ronda de flop
        play_round(0, 0, 3, 0)  # Por ejemplo, 3 cartas para la mesa
    elif len(table) == 4:
        # Ronda de turn
        play_round(0, 0, 1, 0)  # Por ejemplo, 1 carta adicional para la mesa
    elif len(table) == 5:
        # Ronda de river
        play_round(0, 0, 1, 0)  # Igual que la ronda de turn, solo con una carta más en la mesa
    else:
        # Finalizar juego o lógica adicional
        return

main()
