import random
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
print(players_chips)

def saludar(nombre):
    mensaje = f"Hola, {nombre}!"
    return mensaje

# Llamar a la función y pasarle un argumento
nombre_usuario = input("Ingrese su nombre: ")
saludo = saludar(nombre_usuario)

# Utilizar el valor devuelto por la función
print(saludo)