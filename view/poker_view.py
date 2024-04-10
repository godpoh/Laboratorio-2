class PokerView:
    def __init__(self):
        self.main_options = {
            '1': self.start_game,
            '2': self.show_califications,
            '3': self.exit_game
        }

    def show_main_menu(self):
        print("----Bienvenido al juego POKER HOLD'EM----")
        print("1- Iniciar Juego")
        print("2- Mostrar puntuaciones")
        print("3- Salir")
        print("-----------------------------------------")

    def start_game(self):
        pass

    def show_califications(self):
        pass

    def exit_game(self):
        print("Saliendo del sistema")
        exit()

    def main(self):
        while True:
            self.show_main_menu()
            options = input("Ingrese la opcion que desee: ")
            accion = self.main_options.get(options)
            if accion:
                accion()
            else:
                print("Opcion no valida, intentelo de nuevo")

iniciator = PokerView()
iniciator.main()