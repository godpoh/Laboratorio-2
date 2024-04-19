import itertools
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
    pass
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
main()

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
    players[bot["name"]] = {"fichas": bot["chips"], "cartas": []}

    for player, data in players.items():
        show_initial_chips(player, chip_conversion(data["fichas"]), data["cartas"])

    print("Se te quitaron $25 (1 ficha verde) como pago inicial")

    for player in players:
        players[player]["fichas"] -= 25
        for x in range(2):
            dealt_card = deck.pop()
            players[player]["cartas"].append(deck.pop())
            if player == bot["name"]:
                bot["cards"].append(dealt_card)

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


class Players:

    def __init__(self, stack):

        self.stack = stack
        self.last_action = "none"  ## last action taken (check, call etc).
        self.street_bets = 0       ## total bets on current street

    def holecards(self):

## pop cards from list and pritifying their display. Cards will later be
## run through a function for checking value of hands:

        card1 = create_shuffle_deck.pop(len(create_shuffle_deck)-1)
        card2 = create_shuffle_deck.pop(len(create_shuffle_deck)-1)
        self.card1 = (card1[0]+"["+card1[1]+"]")
        self.card2 = (card2[0]+"["+card2[1]+"]")
        self.cards = self.card1+ " - " +self.card2
        print (self.cards)

class Table:

    def __init__(self):

        self.total_pot = 0

    def flop(self):

        card1 = create_shuffle_deck.pop(len(create_shuffle_deck)-1)
        card2 = create_shuffle_deck.pop(len(create_shuffle_deck)-1)
        card2 = create_shuffle_deck.pop(len(create_shuffle_deck)-1)
        self.card1 = (card1[0]+"["+card1[1]+"]")
        self.card2 = (card2[0]+"["+card2[1]+"]")
        self.card3 = (card2[0]+"["+card2[1]+"]")
        self.flop = self.card1+ " - " + self.card2 + " - " + self.card3
        print (self.flop)

    def turn(self):

        card = create_shuffle_deck.pop(len(create_shuffle_deck)-1)
        self.card = (card[0]+"["+card[1]+"]")
        self.turn = self.card
        print (self.turn)

    def river(self):

        card = create_shuffle_deck.pop(len(create_shuffle_deck)-1)
        self.card = (card[0]+"["+card[1]+"]")
        self.river = self.card
        print (self.river)



# Add player stacks and distribute holecards:

for i in range(player_count):
    players.append(i)
    players[i] = Players(100)
    players[i].holecards()

# Add dealer to table:

dealer = table()

dealer.flop()
dealer.turn()
dealer.river()