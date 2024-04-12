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
        print("\nOpcion invalida. Intente de nuevon\n")
def start_game():
    shuffle_deck = create_shuffle_deck()
    initial_deal_cards(shuffle_deck)
    call_option_fold()

def show_califications():
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
def initial_deal_cards(deck):
    players = {}
    player_name = input("Ingrese su nombre: ")

    players[player_name] = {"fichas": 500, "cartas": []}
    players["Sheldon Copper"] = {"fichas": 500, "cartas": []}

    for player, data in players.items():
        show_initial_chips(player, chip_conversion(data["fichas"]))

    for x in range(2):
        for player in players:
            players[player]["fichas"] -= 5
            players[player]["cartas"].append(deck.pop())

    table = []
    for x in range(5):
        table.append(deck.pop())

    return players, table
def chip_conversion(player_name):
    denominations = {
        "blanca": 1,
        "roja": 5,
        "azul": 10,
        "verde": 25,
        "negra": 100
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
        players_chips["blanca"] += remaining_chips // min_denomination

    return players_chips
def show_initial_chips(player_name, initial_chips ):
    print("\n|------------------------------------------|")
    print(f"|{player_name}, tiene las siguentes fichas|")
    print("|------------------------------------------|")
    for denomination, count in initial_chips.items():
        print(f"{count} ficha(s) de {denomination}")

def call_option_fold():
    while True:
        print("|------------------------------------------|")
        print("|                1. Call                   |")
        print("|                2. Raise                  |")
        print("|                3. Fold                   |")
        print("|------------------------------------------|")
#   PUEDE SER CALL, CHECK Y ALL IN EN PRIMER RONDA, AL ACABAR PRIMER RONDA SE MUESTREN 3 CARTAS,
        option = input("Ingrese el proximo movimiento: ")

        if option == "1":
            call()
        elif option == "2":
            raaise()
        elif option == "3":
            fold()
        else:
            print("Opcion invalida")


def call():
    pass

def raaise():
    pass

def fold():
    print("\nTe retiras con (agregar el numero de fichas en restantes)\n")
    main()


def post_flop():
    pass

def turn_betting_round():
    pass

def river_betting_round():
    pass

def handle_blinds():
    pass

def all_in():
    pass

main()
