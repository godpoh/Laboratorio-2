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
    players, table = initial_deal_cards(shuffle_deck)
    current_player = list(players.keys())[0]
    turn_players(players, table, current_player, {})
    river_betting_round(table, {})


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

bot = {
    "name": "Sheldon Cooper",
    "chips": 500,
    "cards": []
}

def initial_deal_cards(deck):
    players = {}
    player_name = input("Ingrese su nombre: ")

    players[player_name] = {"fichas": 500, "cartas": []}
    players[bot["name"]] = {"fichas": bot["chips"], "cartas": []}

    for player, data in players.items():
        show_initial_chips(player, chip_conversion(data["fichas"]))

    for x in range(1):
        for player in players:
            players[player]["fichas"] -= 25
            players[player]["cartas"].append(deck.pop())

    table = []
    for x in range(5):
        table.append(deck.pop())

    return players, table
def chip_conversion(player_name):
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
def show_initial_chips(player_name, initial_chips ):
    print("\n|------------------------------------------|")
    print(f"|{player_name}, tiene las siguentes fichas|")
    print("|               TOTAL ($500)               |")
    print("|------------------------------------------|")
    for denomination, count in initial_chips.items():
        print(f"{count} ficha(s) de {denomination}")


def call_option_fold(last_move, player_data):
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
#PUEDE SER CALL, CHECK Y ALL IN EN PRIMER RONDA, AL ACABAR PRIMER RONDA SE MUESTREN 3 CARTAS,
        option = input("Ingrese el proximo movimiento: ")

        if option == "1":
            if last_move == "1":
                call()
            else:
                check(player_data)

        elif option == "2":
            if last_move == "2":
                raaise()
            else:
                bet()
        elif option == "3":
            fold(player_data)
        elif option == "4":
            all_in(player_data)
        else:
            print("Opcion invalida")

        if option in ["1", "2", "3", "4"]:
            break



def turn_players(players, table, current_player, player_data):
    while True:
        if current_player == list(players.keys())[0]:
            print("\nTu turno!\n")
            call_option_fold("1", players[current_player])
        else:
            print("\nTurno de Sheldon Cooper")
            sheldon_move = sheldon_decide_move(bot["cards"], table)
            print("Sheldon Cooper selecciono: ",sheldon_move)
            call_option_fold(sheldon_move, players[bot["name"]])

        current_player = (int(current_player) + 1) % 2

        if current_player == 0:
            break
    river_betting_round(table, player_data)

def sheldon_decide_move(sheldon_cards, table_cards):
    return random.choice(["1", "2", "3", "4"])

def call():
    print("El jugador hizo un Call!")

def check(player_data):
    if 'fichas' in player_data:
        maxbid = player_data["fichas"]
        print("Holaa")
    else:
        print("Error: 'fichas' no esta definido en el diccionario player_data")
def raaise():
    print("El jugador hizo un raise!")

def fold(player_data):
    player_name = player_data
    print(f"\nSe retira {player_name['fichas']} fichas\n")
    main()

def bet():
    print("El jugador hizo un Bet!")

def all_in(player_data):
    print("El jugador hizo un All-in!")
    player_data["fichas"] = 0
def post_flop():
    pass

def river_betting_round(cards, player_data):
    river = []
    # Si aún no hay cartas en el río
    if len(cards) > 0:
        print("ronda1")
        # Agregar las primeras tres cartas al río
        for _ in range(3):
            river.append(cards.pop())
        print("Cartas en el río después del flop:", river)
        # Aquí puedes simular la ronda de apuestas después del flop
        call_option_fold("3", player_data)

    # Si ya hay 3 cartas en el río
    if len(cards) > 0:
        print("ronda2")
        # Agregar la cuarta carta al río
        river.append(cards.pop())
        print("Cartas en el río después del turn:", river)
        # Aquí puedes simular la ronda de apuestas después del turn
        call_option_fold("3", player_data)

    # Si ya hay 4 cartas en el río
    if len(cards) > 0:
        print("ronda3")
        # Agregar la quinta carta al río
        river.append(cards.pop())
        print("Cartas en el río después del river:", river)
        # Aquí puedes simular la última ronda de apuestas
        call_option_fold("3", player_data)  # Llamar
def turn_betting_round():
    pass

def handle_blinds():
    pass

main()