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

    for player, data in players.items():
        show_player_cards(player, data["cartas"])

    play_game_round(players, table)

    return players, table




def show_califications():
    pass
def exit_game():
    print("Saliendo del sistema")
    exit()
def show_player_cards(player_name ,cards):
    print(f"{player_name} tus cartas son: ")
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



def initial_deal_cards(deck):
    players = {}
    player_name = validate_string_name_input("Ingrese su nombre: ")


    players[player_name] = {"fichas": 500, "cartas": []}
    players["Sheldon Cooper"] = {"fichas": 500, "cartas": []}

    for player, data in players.items():
        show_initial_chips(player, chip_conversion(data["fichas"]), data["cartas"])

    print("Se te quitaron $25 (1 ficha verde) como pago inicial")

    for player in players:
        players[player]["fichas"] -= 25
        for x in range(2):
            dealt_card = deck.pop()
            players[player]["cartas"].append(dealt_card)

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
def show_initial_chips(player_name, initial_chips, cards ):
    print("\n|------------------------------------------|")
    print(f"|{player_name},tiene las siguentes fichas ")
    for denomination, count in initial_chips.items():
        print(f"|{count} ficha(s) de {denomination:10}")
    print("|               TOTAL ($500)               ")
    print("|------------------------------------------|\n")
    if cards:
        print(f"{player_name} tus cartas son: ")
        for card in cards:
            print(card)


def call_option_fold(last_move, player_data, opponent_data):
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
                 player_data = call(player_data, opponent_data)
            else:
                check(player_data)

        elif option == "2":
            if last_move == "2":
                raaise()
            else:
                bet()
        elif option == "3":
            fold(player_data)
            break
        elif option == "4":
            all_in(player_data)
        else:
            print("Opcion invalida")

        if option in ["1", "2", "3", "4"]:
            break

def turn_players(players, table, current_player, player_data):
    is_player_turn = True
    while True:
        if is_player_turn:
            print("\nTu turno!\n")
            call_option_fold("1", player_data, players["Sheldon Cooper"])
        else:
            print("\nTurno de Sheldon Cooper")
            sheldon_move = sheldon_decide_move(players["Sheldon Cooper"]["cartas"], table)
            print("Sheldon Cooper selecciono: ",sheldon_move)
            # if sheldon_move == "1":
            #     player_data, opponent_data = call(player_data, opponent_data)

            if sheldon_move == "3":
                fold_message = fold(players["Sheldon Cooper"])
                if fold_message is None:
                    return list(players.keys())[0]
                print(fold_message)
                return "Sheldon Cooper"

            call_option_fold(sheldon_move, players["Sheldon Cooper"], player_data)

        is_player_turn = not is_player_turn

def sheldon_decide_move(sheldon_cards, table_cards):
    # return random.choice(["1", "2", "3", "4"])
    return "3"

def call(player_data, opponent_data):
    print("El jugador hizo un Call!")
    player_name = list(player_data.keys())[0]
    opponent_name = list(opponent_data.keys())[0]

    if 'fichas' in player_data:
        player_chips = player_data['fichas']
        opponent_chips = opponent_data['fichas']
    else:
        print("Error: 'fichas' no esta definido en player_data")

    call_amount = opponent_chips - player_chips

    if call_amount > 0:
        if player_chips >= call_amount:
            player_data["fichas"] -= call_amount
            opponent_data["fichas"] -= call_amount
            print(f"{player_name} igualo la apuesta de {opponent_name} de {call_amount} fichas")
        else:
            print(f"{player_name} no tiene suficientes fichas para igualar la apuesta")
    else:
        print(f"{player_name} ya ha igualado la apuesta{opponent_name}, {player_data} fichas")

    return player_data, opponent_data

def check(player_data):
    if 'fichas' in player_data:
        maxbid = player_data["fichas"]
        print(f"Fichas del jugador: {maxbid}")
    else:
        print("Error: 'fichas' no esta definido en el diccionario player_data")

def raaise():
    print("El jugador hizo un raise!")

def fold(player_data):
    player_name = list(player_data.keys())[0]
    if player_data["fichas"] == 0:
        print(f"{player_name} se retiró del juego.")
    else:
        print(f"{player_name} se retiró del juego con {player_data['fichas']} fichas.")
    return None

def bet():
    print("El jugador hizo un Bet!")

def all_in(player_data):
    print("El jugador hizo un All-in!")
    player_data["fichas"] = 0

def river_betting_round(cards, player_data):
    river = []

    # Si aún no hay cartas en el río
    if len(cards) > 0:
        print("Flop:")
        # Agregar las primeras tres cartas al río
        for _ in range(3):
            river.append(cards.pop())
        print("Cartas en el río después del flop:", river)
        # Aquí puedes simular la ronda de apuestas después del flop
        call_option_fold("3", player_data, {})

        # Mostrar las cartas del río después del flop
        print("Cartas en el río:", river)

    # Si ya hay 3 cartas en el río
    if len(cards) > 0:
        print("Turn:")
        # Agregar la cuarta carta al río
        river.append(cards.pop())
        print("Cartas en el río después del turn:", river)
        # Aquí puedes simular la ronda de apuestas después del turn
        call_option_fold("3", player_data, {})

        # Mostrar las cartas del río después del turn
        print("Cartas en el río:", river)

    # Si ya hay 4 cartas en el río
    if len(cards) > 0:
        print("River:")
        # Agregar la quinta carta al río
        river.append(cards.pop())
        print("Cartas en el río después del river:", river)
        # Aquí puedes simular la última ronda de apuestas
        call_option_fold("3", player_data, {})  # Llamar
        # Mostrar las cartas del río después del river
        print("Cartas en el río:", river)
    else:
        print("No hay cartas en el river")

    print("Cartas del río:", river)

def play_game_round(players, table):
    pre_flop_finished = False

    while True:
        if not pre_flop_finished:
            turn_players(players, table, list(players.keys())[0], players[list(players.keys())[0]])
            pre_flop_finished = True
        else:
            river_betting_round(table, players)
            break

main()
