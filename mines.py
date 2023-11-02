import tkinter as tk
import time
import random



def contar_minas_alrededor(tablero, x, y):
    count = 0
    for i in range(max(0, x - 1), min(len(tablero), x + 2)):
        for j in range(max(0, y - 1), min(len(tablero[i]), y + 2)):
            if tablero[i][j] == '*' and (i, j) != (x, y):
                count += 1
    return count

def revelar_celda(tablero, buttons, x, y):
    if tablero[x][y] == '*':
        print("¡Has encontrado una mina!")
    else:
        minas_cercanas = contar_minas_alrededor(tablero, x, y)
        buttons[x][y].config(text=str(minas_cercanas))

def crear_botones_tablero(tablero, ventana):
    buttons = []
    for i in range(len(tablero)):
        row = []
        for j in range(len(tablero[i])):
            btn = tk.Button(ventana, width=3, height=1, command=lambda x=i, y=j: revelar_celda(tablero, buttons, x, y))
            btn.grid(row=i + 1, column=j, sticky="nsew")
            row.append(btn)
        buttons.append(row)

    # Configurar filas adicionales para dar espacio arriba del tablero
    for _ in range(1):
        tk.Grid.rowconfigure(ventana, len(tablero) + 1, weight=1)

    return buttons

def crear_tablero(filas, columnas, minas):
    tablero = [[' ' for _ in range(columnas)] for _ in range(filas)]

    # Colocar minas aleatorias
    minas_colocadas = 0
    while minas_colocadas < minas:
        x = random.randint(0, filas - 1)
        y = random.randint(0, columnas - 1)
        if tablero[x][y] != '*':
            tablero[x][y] = '*'
            minas_colocadas += 1

    return tablero

def interfaz_tablero(tablero, board_window, filas, columnas, num_minas):
    # Contador de minas restantes
    contador_minas = tk.Label(board_window, text=f"Minas restantes: {num_minas}")
    contador_minas.grid(row=0, column=0, columnspan=columnas)

    # Contador de banderas puestas
    banderas_puestas = 0  # Inicialmente no hay banderas puestas
    contador_banderas = tk.Label(board_window, text={banderas_puestas})
    contador_banderas.grid(row=1, column=0, columnspan=columnas)

    # Cronometro
    cronometro = tk.Label(board_window, text="Tiempo: 00:00")
    cronometro.grid(row=2, column=0, columnspan=columnas)
    tiempo_inicio = time.time()
    actualizar_cronometro(cronometro, tiempo_inicio, board_window)

    # Reiniciar juego y cerrar la ventana actual
    reiniciar = tk.Button(board_window, text="Reiniciar", command=iniciar_juego)
    reiniciar.grid(row=3, column=0, columnspan=columnas)

    # Agregar espacio entre el tablero y la interfaz
    tk.Label(board_window, text=" ").grid(row=4)   

def actualizar_cronometro(cronometro, tiempo_inicio, board_window):
        cronometro.config(text=time.strftime("Tiempo: %H:%M:%S", time.gmtime(time.time() - tiempo_inicio)))
        board_window.after(1000, actualizar_cronometro)
        
def iniciar_juego():
    filas = int(entry_filas.get())
    columnas = int(entry_columnas.get())
    num_minas = int(entry_minas.get())
    tablero = crear_tablero(filas, columnas, num_minas)

    # Crear tablero
    board_window = tk.Toplevel(root)
    board_window.title("Buscaminas")
    tablero_frame = tk.Frame(root)

    # Tamaño de la ventana
    tamano = 80
    ancho_ventana = tamano * columnas
    alto_ventana = tamano * filas
    board_window.geometry(str(ancho_ventana) + "x" + str(alto_ventana))

    # Crear botones
    buttons = crear_botones_tablero(tablero, board_window)

    # Interfaz del tablero
    interfaz_tablero(tablero, board_window, filas, columnas, num_minas)

if __name__ == "__main__":
    # Crear ventana
    root = tk.Tk()
    root.title("Buscaminas")

    # Etiquetas y entradas para filas, columnas y minas
    tk.Label(root, text="Filas:").grid(row=0, column=0)
    entry_filas = tk.Entry(root)
    entry_filas.insert(0, "5")  # Valor por defecto para filas
    entry_filas.grid(row=0, column=1)

    tk.Label(root, text="Columnas:").grid(row=1, column=0)
    entry_columnas = tk.Entry(root)
    entry_columnas.insert(0, "5")  # Valor por defecto para columnas
    entry_columnas.grid(row=1, column=1)

    tk.Label(root, text="Minas:").grid(row=2, column=0)
    entry_minas = tk.Entry(root)
    entry_minas.insert(0, "5")  # Valor por defecto para minas
    entry_minas.grid(row=2, column=1)

    # Botón para iniciar el juego
    start_button = tk.Button(root, text="Iniciar Juego", command=iniciar_juego)
    start_button.grid(row=3, columnspan=2)

    root.mainloop()
