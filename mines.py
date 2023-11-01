import tkinter as tk

import random

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

def revelar_celda(x, y):
    # Aquí puedes implementar la lógica para revelar la celda en la posición (x, y)
    print(f"Se ha revelado la celda en la posición ({x}, {y})")


def crear_botones_tablero(tablero, ventana):
    for i in range(len(tablero)):
        for j in range(len(tablero[i])):
            btn = tk.Button(ventana, width=3, height=1, command=lambda x=i, y=j: revelar_celda(x, y))
            btn.grid(row=i, column=j)

def iniciar_juego():
    global tablero
    filas = int(entry_filas.get())
    columnas = int(entry_columnas.get())
    num_minas = int(entry_minas.get())
    tablero = crear_tablero(filas, columnas, num_minas)

    # Crear tablero
    board_window= tk.Toplevel(root)
    board_window.title("Buscaminas")
    crear_botones_tablero(tablero, board_window)

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
