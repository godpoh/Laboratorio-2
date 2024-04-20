import random
import time

#Funcion para validar el input human_player
def validate_string(prompt):
    while True:
        user_input = input(prompt)
        #Si human_player no son letras, y ni empieza con mayuscula se volvera a iterar
        if not user_input.replace(" ", "").isalpha() or not user_input.istitle():
            print("Se debe empezar con Mayuscula y  deben ser letras ")
        else:
            return user_input
#Pregunta nombre del usuario
human_player = validate_string("Ingrese su nombre: ")

player = [] #Guarda las cartas del jugador humano
bot = [] #Guarda las cartas del bot
table = [] #Guarda las cartas de la mesa
player_chips = {} #Guarda las fichas del jugador
bot_chips = {} #Guarda las fichas del bot
current_bet = 0 #Apuesta actual
pot = 0 #Bote o cantidad total de fichas en juego
big_blind = 10 #Apuesta ciega grande
small_blind = 10 #Apuesta ciega pequeña

#Menu principal, en este se muestra las 3 opciones principales
def show_main_menu():
    print("|------------------------------------------|")
    print("|    Bienvenido al juego POKER HOLD'EM     |")
    print("|        1. Iniciar Juego                  |")
    print("|        2. Mostrar puntuaciones           |")
    print("|        3. Salir                          |")
    print("|------------------------------------------|")
#Funcion para agregar un input y ejecutarlo el meu desde otra funcion
def main():
    while True:
        show_main_menu()
        selection = input("Ingrese la opcion que desee: ")
        options_menu(selection)
#Funcion que toma la opcion digitada por el usuario y ejecuta diferentes funciones
def options_menu(selection):
    if selection == "1":
        start_game()
    elif selection == "2":
        show_scores()
    elif selection == "3":
        exit_game()
    else:
        print("\nOpcion invalida. Intente de nuevo\n")
#Funcion que guarda las puntuaciones de los jugadores
def save_scores(winner, chips_won):
    try:
        #Añade a los jugadores, tanto nombre como fichas ganadas
        with open("score.txt", "a") as file:
            file.write(f"Nombre: {winner}, Fichas: {chips_won}\n")
    except FileNotFoundError:
        print("Error: No se pudo guardar la puntuación.")
#Funcion que muestra las puntuaciones previamente agregadas por save_scores
def show_scores():
    try:
        #Abre el archivo txt y muestra las puntuaciones
        with open("score.txt", "r") as file:
            print("----- Puntuaciones -----")
            for line in file:
                print(line.strip())
    except FileNotFoundError:
        print("No hay puntuaciones guardadas.")
#Funcion que se utiliza de atajo para cerrar el programa
def exit_game():
    print("Saliendo del sistema")
    exit()
#Funcion que se utiliza para convertir los 500$ en fichas de Poker
def chip_conversion(player_chips):
    denominations = {
        "blanca(1$)": 1,
        "roja(5$)": 5,
        "azul(10$)": 10,
        "verde(25$)": 25,
        "negra(100$)": 100
    }
    #Se utiliza un diccionario vacio para guardar los diferentes tipos de fichas
    chips_dict = {}
    #remaining_chips se utiliza para llevar seguimiento a las fichas restantes que no han sido convertidas
    remaining_chips = player_chips
    for denomination, value in denominations.items():
        max_chips = min(remaining_chips // value, 20)
        chips = random.randint(0, max_chips)
        chips_dict[denomination] = chips
        remaining_chips -= chips * value
    #Si remaining_chips es mayor a 0 es que sobro dinero, el dinero sobrante se almacenara en fichas de blancas
    if remaining_chips > 0:
        min_denomination = min(denominations.values())
        chips_dict["blanca(1$)"] += remaining_chips // min_denomination
    #Devuelve el diccionario chips pero ahora con datos
    return chips_dict
#Funcion en la que se muestra las fichas de los jugadores
def show_initial_chips(human_player):
    initial_chips = 500  # Cantidad inicial de fichas para cada jugador
    #Se llaman a las variables globales
    global player_chips, bot_chips
    #Se guarda en una variable local la funcion chip_conversion y chip_conversion
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
    print("Empezando el juego en 2 segundos...\n")
    #Se utiliza un time.sleep para que de tiempo de leer y que no sea tan brusco el cambio o la transicion
    time.sleep(2)
#Funcion que abre la baraja.txt y la aleatoriza
def create_shuffle_deck():
    #Abre la baraja.txt
    with open("baraja.txt", "r") as file:
        cards = file.readlines()
        #Se guardara en variable deck las cartas
        deck = [card.strip() for card in cards]
        random.shuffle(deck)
        #Devuelve la variable deck
        return deck
#Funcion que se utiliza para sacar las cartas de un mazo mezclado
def deal_cards_for_player(num_cards):
    deck = create_shuffle_deck()
    return [deck.pop() for _ in range(num_cards)]  # Saca las cartas del mazo mezclado
#Funciones que se usa de complemento para play_game(), permite colocar las cartas y rondas
def deal_cards_for_players(num_player, num_bot, num_table):
    #Se llama a las variables globales
    global player, bot
    cards_player = deal_cards_for_player(num_cards=num_player)
    player.extend(cards_player)
    cards_cpu = deal_cards_for_player(num_cards=num_bot)
    bot.extend(cards_cpu)
    cards_table = deal_cards_for_player(num_cards=num_table)
    table.extend(cards_table)
#Funcion que contiene todas las rondas del juego
def play_game():
    #Ronda 1, agrega 2 fichas a ambos jugadores y no agrega ninguna a la mesa
    play_round(1, 2, 2, 0)
    #Ronda 2, agrega 3 fichas a la mesa
    play_round(2, 0, 0, 3)
    play_round(3, 0, 0, 1)
    play_round(4, 0, 0, 1)
#Funcion que muestra las rondas, fichas de los jugadores, cartas de los jugadores y cartas de mesa
def play_round(round_num, num_player, num_bot, num_table):
    #Se llama a las variables globales
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
    #Muestra las cartas de la mesa
    print("Cartas comunitarias:", table)
    print(f"Fichas en juego: {pot}")
    print("--------------------------------------------")
    #Actualiza el pot
    pot += current_bet

    #Esto aplica las ciegas
    if round_num == 1:
        apply_blinds()

    #Turno del jugador real
    print("             Turno de", human_player)
    while True:
        print("|------------------------------------------|")
        print("|          Opciones de apuesta             |")
        print("|               1. Call                    |")
        print("|               2. Raise                   |")
        print("|               3. Fold                    |")
        print("|               4. All-In                  |")
        print("|------------------------------------------|")
        #Implementacion para llamar las funciones cuando el jugador digite un numero
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
            print("Opción no valida. Intente nuevamente.")
    #Turno del bot
    print("\n           Turno de Sheldon Cooper")
    #Accion random del bot
    bot_action = random.choice(["1", "2", "3", "4"])
    print("Sheldon Cooper selecciono:", bot_action)
    #Implementacion para que las acciones del bot surten efecto
    if bot_action == "1":
        call("Sheldon Cooper")
    elif bot_action == "2":
        amount = random.randint(current_bet, current_bet + sum(bot_chips.values()))
        raisee(amount, "Sheldon Cooper")
    elif bot_action == "3":
        fold("Sheldon Cooper")
    elif bot_action == "4":
        all_in("Sheldon Cooper")
#Funcion que se utiliza para igualar una apuesta del oponente
def call(player):
    #Se llama a las variables globales
    global player_chips, bot_chips, current_bet, pot
    #Calcula la cantidad de fichas que se deben igualar para hacer la llamada
    if player == human_player:
        chips_to_call = current_bet - player_chips["blanca(1$)"]
    else:
        chips_to_call = current_bet - bot_chips["blanca(1$)"]
    #Verificar si ya se ha igualuado la apuesta actual
    if chips_to_call <= 0:
        print(f"{player} ya ha igualado la apuesta(Check).")
        print(f"Fichas en juego: {pot}")
        return
    #Verifica si el jugador tiene las suficientes fichas para igualar la apuesta
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
#Esta funcion permite subir la apuesta durante el juego
def raisee(amount, player):
    #Se llama a las variables globales
    global player_chips, current_bet, pot
    max_raise_amount = min(current_bet + sum(player_chips.values()), sum(player_chips.values()))
    # Verifica si el jugador tiene las suficientes fichas para subir la apuesta
    if player_chips["blanca(1$)"] < amount:
        print("No tienes suficientes fichas para subir la apuesta.")
        #Si no se tienen suficientes fichas se va a All-in para continuar jugando
        all_in_amount = player_chips["blanca(1$)"]
        player_chips["blanca(1$)"] = 0
        current_bet += all_in_amount
        pot += all_in_amount
        print(f"{player} va All-In con {all_in_amount} fichas para seguir jugando.")
        print(f"Fichas en juego: {pot}\n")
    else:
        #Asegurarse que el all_in no exceda el maximo posible
        amount = min(amount, max_raise_amount - current_bet)
        player_chips["blanca(1$)"] -= amount
        current_bet += amount
        pot += amount
        print(f"{player} hace raise de {amount}.")
        print(f"Fichas en juego: {pot}\n")
#Funcion para retirarse del juego
def fold(player_name):
    #Se llama la las variables globales
    global player_chips, bot_chips, pot, current_bet
    total_winnings = pot
    #Si el jugador es igual al jugador humano se imprimiran los mensajes correspondientes
    if player_name == human_player:
        print(f"{player_name} se retira. Sheldon Cooper gana la partida.")
        bot_chips["blanca(1$)"] += pot
        print(f"Suma de lo apostado por ambos jugadores: {total_winnings}")
        total_assets_bot = sum(bot_chips.values()) + pot
        print(f"Sheldon Cooper gano un total de {total_winnings} fichas.")
        print("El jugador obtuvo un total de fichas de", total_assets_bot)
        # Se guarda el puntaje en score.txt
        save_scores("Sheldon Cooper", total_assets_bot)
    else:
        print(f"{player_name} se retira. {human_player} gana la partida.")
        player_chips["blanca(1$)"] += pot
        print(f"Suma de lo apostado por ambos jugadores: {total_winnings}")
        print(f"{human_player} gano un total de {total_winnings} fichas.")
        total_assets_human = sum(player_chips.values()) + pot
        print("El jugador obtuvo un total de fichas de", total_assets_human)
        #Se guarda el puntaje en score.txt
        save_scores(human_player, total_assets_human)
    exit_game()
#Funcion para apostar todas las fichas de una vez
def all_in(player):
    #Se llama a las variables globales
    global pot, player_chips, bot_chips, current_bet
    #Se suman todas las fichas de los jugadores que colocan all-in
    all_in_amount = sum(player_chips.values()) if player == human_player else sum(bot_chips.values())
    if player == human_player:
        player_chips = {denomination: 0 for denomination in player_chips}
    else:
        bot_chips = {denomination: 0 for denomination in bot_chips}
    pot += all_in_amount
    current_bet += all_in_amount
    print(f"{player} va All In con {all_in_amount} fichas.")
    print(f"Fichas en juego: {pot}")
#Funcion en la que se aplica la ronda a ciegas
def apply_blinds():
    #Se llama a la variables globales
    global player_chips, current_bet, pot
   #Aplica la ciega pequeña al jugador humano
    player_chips["blanca(1$)"] -= small_blind
    current_bet = small_blind
    pot += small_blind
    print(f"{human_player} pone la ciega pequeña de {small_blind} fichas.")

    #Aplica la ciega grande al jugador bot
    bot_chips["blanca(1$)"] -= big_blind
    current_bet = big_blind
    pot += big_blind
    print(f"Sheldon Cooper pone la ciega grande de {big_blind} fichas.")
    print(f"Fichas en juego: {pot}")
    print("--------------------------------------------")
#Funcion en la que se implementa la logica en la que se elige el ganador por medio de las cartas
def evaluate_hands(cards_player, cards_opponent):
    card_values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13,'A': 14}
    #Esta funcion implementa la logica de la mano de parejas
    def pair(hand):
        card_values = [card[0] for card in hand]
        for value in card_values:
            if card_values.count(value) == 2:
                return True
        return False
    # Esta funcion implementa la logica de la mano 4 cartas iguales
    def four_of_a_kind(hand):
        card_values = [card[0] for card in hand]
        for value in card_values:
            if card_values.count(value) == 4:
                return True
        return False
    # Esta funcion implementa la logica de la mano de cartas 3 mismo tipo y 1 pareja
    def full_house(hand):
        return three_of_a_kind(hand) and pair(hand)

    # Esta funcion implementa la logica de la mano de cartas en escalera
    def straight(hand):
        sorted_values = sorted([card_values[card.split()[0]] if card.split()[0] in card_values else int(card.split()[0]) for card in hand])
        return len(set(sorted_values)) == 5 and (sorted_values[-1] - sorted_values[0] == 4)

    # Esta funcion implementa la logica de la mano de cartas de 2 pares
    def two_pairs(hand):
        card_values = [card[0] for card in hand]
        pairs = 0
        for value in card_values:
            if card_values.count(value) == 2:
                pairs += 1
        return pairs == 2

    # Esta funcion implementa la logica de la mano de cartas 3 iguales
    def three_of_a_kind(hand):
        card_values = [card[0] for card in hand]
        for value in card_values:
            if card_values.count(value) == 3:
                return True
        return False
    # Esta funcion implementa la logica de la mano de cartas de Color
    def flush(hand):
        suit = hand[0][1]
        return all(card[1] == suit for card in hand)
    #Funcion para llamar las funciones anterior e imprimir el mensaje
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
        highest_card_human_player = max([card_values[card.split()[0]] if card.split()[0] in card_values else int(card.split()[0]) for card in cards_player + table])
        highest_card_bot_opponent = max([card_values[card.split()[0]] if card.split()[0] in card_values else int(card.split()[0]) for card in cards_opponent + table])
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
#Funcion que ejecuta todas las funciones anteriores para que el juego funcione correctamente
def start_game():
    global pot, current_bet
    show_initial_chips(human_player)
    play_game()
    winner = evaluate_hands(player, bot)
    print(f"\n{human_player}: {player}")
    print(f"Sheldon Cooper: {bot} ")
    print(f"Cartas Comunitarias: {table}\n")
    print(f"Ganador de la partida: {winner}")
    if winner == "Sheldon Cooper":
        total_assets_bot = sum(bot_chips.values()) + pot
        print(f"Sheldon Cooper gano un total de {pot} fichas.")
        print("El jugador obtuvo un total de fichas de", total_assets_bot)
        save_scores("Sheldon Cooper", total_assets_bot)

    elif winner == human_player:
        print(f"{human_player} gano un total de {pot} fichas.")
        total_assets_human = sum(player_chips.values()) + pot
        print("El jugador obtuvo un total de fichas de", total_assets_human)
        save_scores(human_player, total_assets_human)
    elif winner == "Empate":
        save_scores("Empate", 0)
    exit_game()

main()