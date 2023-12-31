import tkinter as tk
from tkinter import ttk
import time
import random
from PIL import Image, ImageTk

def cargar_imagen(ruta, ancho, alto):
    imagen = Image.open(ruta)
    imagen = imagen.resize((ancho, alto), Image.LANCZOS)
    imagen = ImageTk.PhotoImage(imagen)
    return imagen

def contar_minas_alrededor(tablero, x, y):
    count = 0
    for i in range(max(0, x - 1), min(len(tablero), x + 2)):
        for j in range(max(0, y - 1), min(len(tablero[i]), y + 2)):
            if tablero[i][j] == '*' and (i, j) != (x, y):
                count += 1
    return count

def contadorBanderas(label, simbol, tablero, buttons):
    global banderas_puestas
    if simbol == "+":
        banderas_puestas += 1
    elif simbol == "-":
        banderas_puestas -= 1
    label.config(text=f"Banderas: {banderas_puestas}")
    hasGanado(tablero, buttons)

def salir_accion(root):
    global board_window
    board_window.destroy()
    root.destroy()

def mostrarMinas(tablero, buttons):
    for i in range(len(tablero)):
        for j in range(len(tablero[i])):
            if tablero[i][j] == '*':
                buttons[i][j].config(text="M")

def hasGanado(tablero, buttons):
    global num_minas
    banderas_correctas = 0
    for i in range(len(tablero)):
        for j in range(len(tablero[i])):
            if tablero[i][j] == '*' and buttons[i][j]['text'] == 'B':
                banderas_correctas += 1

    celdas_sin_mina = sum(row.count('') for row in tablero)
    if banderas_correctas == num_minas and celdas_sin_mina == 0:
        root = tk.Tk()
        root.title("¡Felicidades!")
        root.geometry("200x100")
        tk.Label(root, text="¡Felicidades, has ganado!").pack()
        tk.Button(root, text="Salir", command=lambda: salir_accion(root)).pack()
        root.mainloop()


def hasPerdido():
    # Mostar mensaje de que has perdido
    root = tk.Tk()
    root.title("Has perdido")
    root.geometry("200x100")
    tk.Label(root, text="Has perdido").pack()
    tk.Button(root, text="Salir", command=lambda: salir_accion(root)).pack()
    root.mainloop()

def desbloquear_celdas(tablero, buttons, x, y):
    if x < 0 or y < 0 or x >= len(tablero) or y >= len(tablero[0]):
        return
    if buttons[x][y]['state'] == tk.DISABLED:
        return
    minas_cercanas = contar_minas_alrededor(tablero, x, y)
    if minas_cercanas in (0, 1, 2, 3):
        buttons[x][y].config(text=str(minas_cercanas), state=tk.DISABLED)
        if minas_cercanas == 0:  # Solo se propagará la recursión si es una celda sin minas cercanas
            for i in range(-1, 2):
                for j in range(-1, 2):
                    desbloquear_celdas(tablero, buttons, x + i, y + j)


def revelar_celda(tablero, buttons, x, y, event):
    if event == 'left':  # Si el evento es un clic izquierdo
        if buttons[x][y]['text'] == "B":  # Verificar si hay una bandera
            return  # No hacer nada si hay una bandera en la celda

        if tablero[x][y] == '*':
            print("¡Has encontrado una mina!")
            #buttons[x][y].config(image=imagenBomba)
            mostrarMinas(tablero, buttons)
            hasPerdido()
        else:
            minas_cercanas = contar_minas_alrededor(tablero, x, y)
            desbloquear_celdas(tablero, buttons, x, y)  
    elif event == 'right':  # Si el evento es un clic derecho
        if buttons[x][y]['text'] == '':  # Si la celda está sin revelar, coloca una bandera
            buttons[x][y].config(text='B')
            contadorBanderas(contador_banderas, "+", tablero, buttons)
        elif buttons[x][y]['text'] == 'B':  # Si la celda tiene una bandera, quítala
            buttons[x][y].config(text='')
            contadorBanderas(contador_banderas, "-", tablero, buttons)

def crear_botones_tablero(tablero, ventana):
    buttons = []

    # Funciones para manejar los clics en los botones
    def left_click_handler(x, y):
        revelar_celda(tablero, buttons, x, y, 'left')
    
    def right_click_handler(x, y):
        revelar_celda(tablero, buttons, x, y, 'right')
    
    for i in range(len(tablero)):
        row = []
        for j in range(len(tablero[i])):
            btn = tk.Button(ventana, width=5, height=2)
            btn.grid(row=i+1, column=j, sticky="nsew")
            row.append(btn)
            btn.bind('<Button-1>', lambda e, x=i, y=j: left_click_handler(x, y), add='+')
            btn.bind('<Button-3>', lambda e, x=i, y=j: right_click_handler(x, y), add='+')
        buttons.append(row)

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

def reiniciar_accion(board_window):
    board_window.destroy()  # Cerrar la ventana actual
    iniciar_juego()  # Volver a iniciar el juego

def interfaz_tablero(tablero, board_window, alto_ventana, ancho_ventana, num_minas):
    # Contador de minas restantes
    contador_minas = tk.Label(board_window, text=f"Minas restantes: {num_minas}")
    contador_minas.grid(row=0, column=0)

    # Contador de banderas puestas
    global banderas_puestas  # Inicialmente no hay banderas puestas
    banderas_puestas = 0
    global contador_banderas
    contador_banderas = tk.Label(board_window, text=f"Banderas: {banderas_puestas}")
    contador_banderas.grid(row=0, column=1)

    # Cronómetro
    cronometro = tk.Label(board_window, text="Tiempo: 00:00")
    cronometro.grid(row=0, column=2)
    tiempo_inicio = time.time()
    actualizar_cronometro(cronometro, tiempo_inicio, board_window)

    # Reiniciar juego y cerrar la ventana actual
    reiniciar = tk.Button(board_window, text="Reiniciar", command=lambda: reiniciar_accion(board_window))
    reiniciar.grid(row=0, column=3)

    # Agregar espacio entre el tablero y la interfaz
    tk.Label(board_window, text=" ").grid(row=1, columnspan=4, pady=5)

    buttons_frame = tk.Frame(board_window)
    buttons_frame.grid(row=1, column=0, columnspan=ancho_ventana, pady=5)

    buttons = crear_botones_tablero(tablero, buttons_frame)

def actualizar_cronometro(cronometro, tiempo_inicio, board_window):
    cronometro.config(text=time.strftime("Tiempo: %H:%M:%S", time.gmtime(time.time() - tiempo_inicio)))
    board_window.after(1000, lambda: actualizar_cronometro(cronometro, tiempo_inicio, board_window))
        
def iniciar_juego():
    filas = int(entry_filas.get())
    columnas = int(entry_columnas.get())
    global num_minas
    num_minas = int(entry_minas.get())
    tablero = crear_tablero(filas, columnas, num_minas)

    # Crear tablero
    global board_window
    board_window = tk.Toplevel(root)
    board_window.title("Buscaminas")
    tablero_frame = tk.Frame(root)

    # Tamaño de la ventana
    tamano = 80
    ancho_ventana = tamano * columnas
    alto_ventana = tamano * filas
    board_window.geometry(str(ancho_ventana) + "x" + str(alto_ventana))

    # Interfaz del tablero
    interfaz_tablero(tablero, board_window, alto_ventana, ancho_ventana, num_minas)

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
