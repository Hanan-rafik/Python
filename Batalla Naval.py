# Hanan Rafik, Luis Aguado
import random
import time
from colorama import Fore, Style

# Configuración del tablero
TAMANO_TABLERO = 10

# Barcos y sus tamaños
barcos = {
    4: 1,
    3: 2,
    2: 3,
    1: 4
}

# Colores y símbolos
COLOR_RESET = Style.RESET_ALL
COLOR_AGUA = Fore.BLACK
COLOR_TOCADO = Fore.YELLOW
COLOR_HUNDIDO =Fore.RED
COLOR_AGUA_ATACADA = Fore.GREEN
COLOR_NUMERO_BARCO = Fore.CYAN + Style.BRIGHT
COLOR_MENU = Fore.YELLOW
COLOR_TITULO = Fore.MAGENTA + Style.BRIGHT
COLOR_BLANCO = Fore.WHITE

SIMBOLO_AGUA = "~"
SIMBOLO_TOCADO = "T"
SIMBOLO_HUNDIDO = "H"
SIMBOLO_AGUA_ATACADA = "A"

# Crear tablero vacío
def crear_tablero():
    return [[SIMBOLO_AGUA] * TAMANO_TABLERO for _ in range(TAMANO_TABLERO)]

# Mostrar tableros juntos
def mostrar_tableros_juntos(tablero_ataque, tablero_jugador):
    print(f"\n    {COLOR_MENU}" + "   ".join(str(i+1) for i in range(TAMANO_TABLERO)) + f"{COLOR_RESET}     " +
          f"    {COLOR_MENU}" + "   ".join(str(i+1) for i in range(TAMANO_TABLERO)) + f"{COLOR_RESET}")
    print("  +" + "────" * TAMANO_TABLERO + "+     " + "  +" + "────" * TAMANO_TABLERO + "+")
    for i, (fila_ataque, fila_jugador) in enumerate(zip(tablero_ataque, tablero_jugador)):
        letra_fila = chr(ord('A') + i)
        fila_ataque_mostrar = " │ ".join(colorear_celda(celda, False) for celda in fila_ataque)
        fila_jugador_mostrar = " │ ".join(colorear_celda(celda, True) for celda in fila_jugador)
        print(f"{COLOR_BLANCO}{letra_fila} │ {fila_ataque_mostrar} │{COLOR_RESET}     "
              f"{COLOR_BLANCO}{letra_fila} │ {fila_jugador_mostrar} │{COLOR_RESET}")
        if i < TAMANO_TABLERO - 1:
            print("  ├" + "───┼" * (TAMANO_TABLERO - 1) + "───┤     " + "  ├" + "───┼" * (TAMANO_TABLERO - 1) + "───┤")
    print("  +" + "────" * TAMANO_TABLERO + "+     " + "  +" + "────" * TAMANO_TABLERO + "+")

# Colorear celdas para que sean más visibles
def colorear_celda(celda, mostrar_barcos):
    if celda == SIMBOLO_AGUA:
        return f"{COLOR_AGUA}{celda}{COLOR_RESET}"
    elif celda == SIMBOLO_TOCADO:
        return f"{COLOR_TOCADO}{celda}{COLOR_RESET}"
    elif celda == SIMBOLO_HUNDIDO:
        return f"{COLOR_HUNDIDO}{celda}{COLOR_RESET}"
    elif celda == SIMBOLO_AGUA_ATACADA:
        return f"{COLOR_AGUA_ATACADA}{celda}{COLOR_RESET}"
    elif celda in ['1', '2', '3', '4'] and mostrar_barcos:  
        return f"{COLOR_NUMERO_BARCO}{celda}{COLOR_RESET}"
    return celda

# Verifica si se puede colocar un barco en la posición deseada, dejando un espacio
def puedo_colocar_barco(tablero, tamano_barco, fila, col, direccion):
    # Verificar en horizontal
    if direccion == 'H':
        if col + tamano_barco > TAMANO_TABLERO:
            return False
        # Verificar las celdas donde se coloca el barco y las adyacentes
        for i in range(tamano_barco):
            if tablero[fila][col + i] != SIMBOLO_AGUA:
                return False
            # Verificar las celdas diagonales
            if fila > 0:  # Fila superior
                if col + i > 0 and tablero[fila - 1][col + i - 1] != SIMBOLO_AGUA:  # Superior izquierda
                    return False
                if col + i < TAMANO_TABLERO - 1 and tablero[fila - 1][col + i + 1] != SIMBOLO_AGUA:  # Superior derecha
                    return False
            if fila < TAMANO_TABLERO - 1:  # Fila inferior
                if col + i > 0 and tablero[fila + 1][col + i - 1] != SIMBOLO_AGUA:  # Inferior izquierda
                    return False
                if col + i < TAMANO_TABLERO - 1 and tablero[fila + 1][col + i + 1] != SIMBOLO_AGUA:  # Inferior derecha
                    return False
        # Verificar la celda a la izquierda y derecha (si existen)
        if col > 0 and tablero[fila][col - 1] != SIMBOLO_AGUA:  # Izquierda
            return False
        if col + tamano_barco < TAMANO_TABLERO and tablero[fila][col + tamano_barco] != SIMBOLO_AGUA:  # Derecha
            return False
            
    else:  # Direccion 'V'
        if fila + tamano_barco > TAMANO_TABLERO:
            return False
        # Verificar las celdas donde se coloca el barco y las adyacentes
        for i in range(tamano_barco):
            if tablero[fila + i][col] != SIMBOLO_AGUA:
                return False
            # Verificar las celdas diagonales
            if col > 0:  # Columna izquierda
                if fila + i > 0 and tablero[fila + i - 1][col - 1] != SIMBOLO_AGUA:  # Superior izquierda
                    return False
                if fila + i < TAMANO_TABLERO - 1 and tablero[fila + i + 1][col - 1] != SIMBOLO_AGUA:  # Inferior izquierda
                    return False
            if col < TAMANO_TABLERO - 1:  # Columna derecha
                if fila + i > 0 and tablero[fila + i - 1][col + 1] != SIMBOLO_AGUA:  # Superior derecha
                    return False
                if fila + i < TAMANO_TABLERO - 1 and tablero[fila + i + 1][col + 1] != SIMBOLO_AGUA:  # Inferior derecha
                    return False
        # Verificar la celda superior e inferior (si existen)
        if fila > 0 and tablero[fila - 1][col] != SIMBOLO_AGUA:  # Superior
            return False
        if fila + tamano_barco < TAMANO_TABLERO and tablero[fila + tamano_barco][col] != SIMBOLO_AGUA:  # Inferior
            return False

    return True

# Coloca el barco en el tablero
def colocar_barco(tablero, tamano_barco):
    colocado = False
    while not colocado:
        fila = random.randint(0, TAMANO_TABLERO - 1)
        col = random.randint(0, TAMANO_TABLERO - 1)
        direccion = random.choice(['H', 'V'])
        if puedo_colocar_barco(tablero, tamano_barco, fila, col, direccion):
            if direccion == 'H':
                for i in range(tamano_barco):
                    tablero[fila][col + i] = str(tamano_barco)  # Cambiado para mostrar el tamaño del barco
            else:
                for i in range(tamano_barco):
                    tablero[fila + i][col] = str(tamano_barco)  # Cambiado para mostrar el tamaño del barco
            colocado = True


# Configura el tablero con todos los barcos
def configurar_tablero():
    tablero = crear_tablero()
    for tamano_barco, cantidad in barcos.items():
        for _ in range(cantidad):
            colocar_barco(tablero, tamano_barco)
    return tablero

# Convertir letras de columnas a índices
def letra_a_indice(fila):
    return ord(fila.upper()) - ord('A')

# Verifica si un barco está hundido
def esta_hundido(tablero, fila, col):
    for i in range(max(0, fila - 1), min(TAMANO_TABLERO, fila + 2)):
        for j in range(max(0, col - 1), min(TAMANO_TABLERO, col + 2)):
            if tablero[i][j] in ['1', '2', '3', '4']:
                return False
    return True

# Mostrar menú del juego
def mostrar_menu():
    print(f"\n{COLOR_MENU}==============================")
    print("        Menú de Batalla Naval")
    print("==============================")
    print(f"{COLOR_BLANCO}💥  1. Iniciar batalla (colocar barcos)")
    print(f"{COLOR_BLANCO}🎯  2. Atacar")
    print(f"{COLOR_BLANCO}📡  3. Recibir ataque")
    print(f"{COLOR_BLANCO}🗺️  4. Visualizar mapas")
    print(f"{COLOR_BLANCO}🚪  5. Salir del juego{COLOR_RESET}")
    print("==============================")

# Juego principal
def main():
    tablero_jugador = crear_tablero()
    tablero_ataque = crear_tablero()
    juego_iniciado = False

    print(f"{COLOR_TITULO}¡Bienvenido a Batalla Naval!{COLOR_RESET}")
    
    while True:
        mostrar_menu()
        opcion = input("Selecciona una opción (1-5): ")

        if opcion == '1':
            print("\nConfigurando tu tablero... ¡Listo para la batalla!")
            tablero_jugador = configurar_tablero()
            juego_iniciado = True
            print("Barcos colocados. ¡Que comience la batalla!")

        elif opcion == '2' and juego_iniciado:
            fila = input("Introduce columna (A-J) para atacar: ")
            col = int(input("Introduce fila (1-10) para atacar: ")) - 1
            fila_index = letra_a_indice(fila)
            resultado = input("¿Cuál fue el resultado (agua, tocado, hundido)?: ").strip().lower()
            if resultado == "agua":
                tablero_ataque[fila_index][col] = SIMBOLO_AGUA_ATACADA
            elif resultado == "tocado":
                tablero_ataque[fila_index][col] = SIMBOLO_TOCADO
            elif resultado == "hundido":
                tablero_ataque[fila_index][col] = SIMBOLO_HUNDIDO
            print("\nMapa de tus ataques:")
        
        elif opcion == '3' and juego_iniciado:
            fila = input("Introduce la fila donde te atacaron (A-J): ")
            col = int(input("Introduce la columna donde te atacaron (1-10): ")) - 1
            fila_index = letra_a_indice(fila)
            if tablero_jugador[fila_index][col] in ['1', '2', '3', '4']:
                tablero_jugador[fila_index][col] = SIMBOLO_TOCADO
                if esta_hundido(tablero_jugador, fila_index, col):
                    print(f"{COLOR_TOCADO}¡Uno de tus barcos ha sido hundido!{COLOR_RESET}")
                    tablero_jugador[fila_index][col] = SIMBOLO_HUNDIDO
                else:
                    print(f"{COLOR_TOCADO}¡Uno de tus barcos ha sido tocado!{COLOR_RESET}")
            else:
                tablero_jugador[fila_index][col] = SIMBOLO_AGUA_ATACADA
                print(f"{COLOR_AGUA}El ataque enemigo cayó en el agua.{COLOR_RESET}")

        elif opcion == '4' and juego_iniciado:
            print("\nMostrando mapas lado a lado:")

        elif opcion == '5':
            print("¡Gracias por jugar! ¡Hasta la próxima!")
            break
        else:
            print("Opción inválida. Por favor selecciona una opción entre 1 y 5.")
        
        # Mostrar tableros después de cada acción
        mostrar_tableros_juntos(tablero_ataque, tablero_jugador)

# Ejecuta el juego
if __name__ == "__main__":
    main()
