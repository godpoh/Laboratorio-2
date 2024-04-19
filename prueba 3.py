import random
#MENU
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
    deck = create_shuffled_deck()
    flop_turn_river_table(deck)

def show_scores():
    pass

def exit_game():
    print("Saliendo del sistema")
    exit()

#Revolver el mazo
def create_shuffled_deck():
    with open("baraja.txt", "r") as file:
        cards = file.readlines()
        deck = [card.strip() for card in cards]
        random.shuffle(deck)
        return deck

def chip_conversion(player_chips):
    denominations = {
        "blanca(1$)": 1,
        "roja(5$)": 5,
        "azul(10$)": 10,
        "verde(25$)": 25,
        "negra(100$)": 100
    }
    players_chips = {}

    remaining_chips = player_chips
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


def distributor_card_players(deck):
    players = []
    human_player = input("Ingrese su nombre")

    players[human_player] = {"fichas": 500, "cartas_jugadores": []}
    players["Sheldon Cooper"] = {"fichas": 500, "cartas_jugadores": []}

    for player, data in players.items():
        show_initial_chips(player, chip_conversion(data["fichas"]))


def flop_turn_river_table(deck):
    river = []

    if len(deck) >= 3:
        print("Flop:")
        for _ in range(3):
            river.append(deck.pop())
        print("Cartas en el río:", river)

    if len(deck) >= 1:
        print("Turn:")
        river.append(deck.pop())
        print("Cartas en el río:", river)

    if len(deck) >= 1:
        print("River:")
        river.append(deck.pop())
        print("Cartas en el río:", river)
    else:
        print("No hay cartas en el river")

    return river





main()