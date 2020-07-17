from tkinter import *
import random
import sqlite3
from clases import *

#FUNCIONES

def salir():
	miConexion.close()
	root.destroy()

def destruirHijos(infoFrame):
	for child in infoFrame.winfo_children():
		child.destroy()

def volver():
	frameJuego.pack_forget()
	inicio()

def reiniciar():
	volver()
	juego(len(tab))


def imprimir():
	global tab
	for row in tab:
		a = []
		for cas in row:
			a.append(cas.get())
		print(a)

def finJuego():
	global tab
	n = len(tab)

	es = True
	i = 0

	list_corr = []
	for num in range(1, n * n):
		list_corr.append(str(num))
	list_corr.append("")

	list_prueba = []
	for row in tab:
		for cas in row:
			list_prueba.append(cas.get())
	
	while (es and i < n * n):
		es = (list_corr[i] == list_prueba[i])
		i = i + 1

	if(es):
		return n
	else:
		return 0

def actualizar(f, c):
	global void

	vf = void['f']
	vc = void['c']

	if(not (f == vf and c == vc) and (f == vf or c == vc)):
		if(f == vf):
			if(c < vc):
				while(c < vc):
					tab[f][vc].set(tab[f][vc - 1].get())
					vc = vc - 1
			else:
				while(c > vc):
					tab[f][vc].set(tab[f][vc + 1].get())
					vc = vc + 1
		else:
			if(f < vf):
				while(f < vf):
					tab[vf][c].set(tab[vf - 1][c].get())
					vf = vf - 1
			else:
				while(f > vf):
					tab[vf][c].set(tab[vf + 1][c].get())
					vf = vf + 1

		tab[f][c].set("")
		void['f'] = f
		void['c'] = c
		return 1
	else:
		print("Movimiento invalido.")
		return 0

def jugada(f, c):
	global pasos
	pasos = pasos + actualizar(f, c)
	score.set(str(pasos))
	n = finJuego()
	if(n):
		stats(n + 1)

def movAleatorio(n):
	global void
	f = n
	c = n
	pos = random.randrange(n)

	if(random.randrange(2)):
		#COL FIJA
		f = random.randrange(n - 1)
		if(f == void['f']):
			f = n - 1
		c = void['c']
	else:
		#ROW FIJA
		c = random.randrange(n - 1)
		if(c == void['c']):
			c = n - 1
		f = void['f']
	actualizar(f, c)

def buscarPos(list, elem):
	i = 0
	es = False
	while not es:
		if(i < len(list)):
			if(int(list[i]) < elem):
				i = i + 1
			else:
				es = True
		else:
			es = True
	return i

def ubicar(orden):

	miCursor.execute("SELECT * FROM PARTICIPANTES WHERE ORDEN = ?", str(orden))
	scores = miCursor.fetchall() #NOMBRE, PASOS, ORDEN

	top1['nom'].set("")
	top1['pasos'].set("")
	top2['nom'].set("")
	top2['pasos'].set("")
	top3['nom'].set("")
	top3['pasos'].set("")
	top4['nom'].set("")
	top4['pasos'].set("")
	top5['nom'].set("")
	top5['pasos'].set("")

	topJug = []
	topPas = []

	for score in scores:
		pos = buscarPos(topPas, score[1])
		topJug.insert(pos, score[0])
		topPas.insert(pos, score[1])
		if(len(topJug) == 6):
			topJug.pop()
			topPas.pop()

	if(len(topJug) >= 1):
		top1['nom'].set(topJug[0])
		top1['pasos'].set(str(topPas[0]))
		if(len(topJug) >= 2):
			top2['nom'].set(topJug[1])
			top2['pasos'].set(str(topPas[1]))
			if(len(topJug) >= 3):
				top3['nom'].set(topJug[2])
				top3['pasos'].set(str(topPas[2]))
				if(len(topJug) >= 4):
					top4['nom'].set(topJug[3])
					top4['pasos'].set(str(topPas[3]))
					if(len(topJug) >= 5):
						top5['nom'].set(topJug[4])
						top5['pasos'].set(str(topPas[4]))
	
def cargar(orden):
	global botonGuardar

	insert = (nombre.get(), score.get(), str(orden))
	miCursor.execute("INSERT INTO PARTICIPANTES VALUES (?, ?, ?)", insert)
	miConexion.commit()
	botonGuardar.config(state = "disabled")
	ubicar(orden)

def borrarHighscore(orden):
	miCursor.execute("DELETE FROM PARTICIPANTES WHERE ORDEN = ?", str(orden))
	ubicar(orden)

#VARIABLES

title = "Quince"
bg_root = "#442200"
bg_frame = "#FFEECC"
pad = 10

tab = []
void = {'f': 0, 'c': 0}

#BBDD

miConexion = sqlite3.connect("Highscores")
miCursor = miConexion.cursor()

#CREAR UNA TABLA
try:
	miCursor.execute("CREATE TABLE PARTICIPANTES (NOMBRE VARCHAR(50), PASOS INTEGER, ORDEN INTEGER)")
except:
	pass

root = Tk()

root.title(title)
root.config(bg = bg_frame)

Button(root, text = "X", cursor = "hand2", bg = bg_root, width = 2, fg = "white", font = ("Comic Sans MS", 7), relief = "groove", command = salir).pack(anchor = "e", padx = pad, pady = pad)

frameInicio = Frame(root, bg = bg_frame)


frameJuego = Frame(root, bg = bg_frame)

botAtras = Button(frameJuego, text = "←", cursor = "hand2", command = volver)
botAtras.grid(row = 0, column = 0, padx = pad / 2, pady = pad / 2)

score = StringVar()
labPasos = Label(frameJuego, textvariable = score, bg = bg_root, width = 5, fg = "white", font = ("Comic Sans MS", 14))
labPasos.grid(row = 0, column = 1)

botReiniciar = Button(frameJuego, text = "⟲", cursor = "hand2", command = reiniciar)
botReiniciar.grid(row = 0, column = 2, padx = pad / 2, pady = pad / 2)

frameTablero = Frame(frameJuego, bg = bg_frame)
frameTablero.grid(row = 1, column = 0, columnspan = 3)

frameStats = Frame(root, bg = bg_frame)

botonGuardar = None

#INICIO

def inicio():
	global bg_frame
	global bg_root
	global pad
	
	frameStats.pack_forget()
	frameInicio.pack()

	Label(frameInicio, text = "Elija el tablero", font = ("Comic Sans MS", 18), bg = bg_frame).grid(column = 0, row = 0, columnspan = 2, padx = pad / 2, pady = pad / 2)
	BotonNivel(frameInicio, "3x3", lambda: juego(3), bg_root).grid(0, 0, pad)
	BotonNivel(frameInicio, "4x4", lambda: juego(4), bg_root).grid(0, 1, pad)
	BotonNivel(frameInicio, "5x5", lambda: juego(5), bg_root).grid(1, 0, pad)
	BotonNivel(frameInicio, "6x6", lambda: juego(6), bg_root).grid(1, 1, pad)
	BotonNivel(frameInicio, "7x7", lambda: juego(7), bg_root).grid(2, 0, pad)
	BotonNivel(frameInicio, "8x8", lambda: juego(8), bg_root).grid(2, 1, pad)
	BotonNivel(frameInicio, "9x9", lambda: juego(9), bg_root).grid(3, 0, pad)
	BotonNivel(frameInicio, "10x10", lambda: juego(10), bg_root).grid(3, 1, pad)

inicio()

#JUEGO

def juego(orden):
	global bg_frame
	global bg_root
	global pad

	global tab

	global void

	global pasos

	tab = []
	aux = []
	pasos = 0
	score.set(str(pasos))
	size = 2

	destruirHijos(frameTablero)

	#CREACION
	for i in range(orden):
		for j in range(orden):
			valor = StringVar()
			valor.set(str(orden * i + j + 1))
			aux.append(valor)
		tab.append(aux)
		aux = []
	tab[orden - 1][orden - 1].set("")
	

	void['f'] = orden - 1
	void['c'] = orden - 1

	for count in range(200):
		movAleatorio(orden)

	frameInicio.pack_forget()
	frameJuego.pack(padx = pad, pady = pad, anchor = "center")

	for i in range(orden):
		for j in range(orden):
			boton = Casillero(frameTablero, tab, i, j, bg_root, jugada)


#STATS

top1 = {'nom' : StringVar(), 'pasos' : StringVar()}
top2 = {'nom' : StringVar(), 'pasos' : StringVar()}
top3 = {'nom' : StringVar(), 'pasos' : StringVar()}
top4 = {'nom' : StringVar(), 'pasos' : StringVar()}
top5 = {'nom' : StringVar(), 'pasos' : StringVar()}

nombre = StringVar()


def stats(n):
	global bg_root
	global bg_frame
	global pad
	global botonGuardar

	pad = pad / 2

	frameJuego.pack_forget()
	frameStats.pack(padx = pad, pady = pad)

	Label(frameStats, text = str(n) + "x" + str(n), bg = bg_root, fg = "white", font = ("Comic Sans MS", 12)).pack(padx = pad, pady = pad)
	Label(frameStats, text = score.get() + " pasos", bg = bg_root, fg = "white", font = ("Comic Sans MS", 12)).pack(padx = pad, pady = pad)
	frameGuardar = Frame(frameStats, bg = bg_frame)
	frameGuardar.pack()

	Label(frameGuardar, text = "Nombre:" ,bg = bg_frame, fg = "black", font = ("Comic Sans MS", 12)).grid(row = 0, column = 0, padx = pad / 2, pady = pad / 2)
	
	Entry(frameGuardar, textvariable = nombre, font = 16, width = 12).grid(row = 0, column = 1, padx = pad / 2, pady = pad / 2)
	botonGuardar = Button(frameGuardar, text = "Enviar", cursor = "hand2", state = 'normal', command = lambda: cargar(n))
	botonGuardar.grid(row = 0, column = 2, padx = pad / 2, pady = pad / 2)

	framePosiciones = Frame(frameStats, bg = bg_frame)
	framePosiciones.pack()

	#TITULO
	Label(framePosiciones, text = "Pos" ,bg = bg_frame, fg = "black", font = ("Comic Sans MS", 12)).grid(row = 0, column = 0, padx = pad, pady = pad)
	Label(framePosiciones, text = "Nombre" ,bg = bg_frame, fg = "black", font = ("Comic Sans MS", 12)).grid(row = 0, column = 1, padx = pad, pady = pad)
	Label(framePosiciones, text = "Pasos" ,bg = bg_frame, fg = "black", font = ("Comic Sans MS", 12)).grid(row = 0, column = 2, padx = pad, pady = pad)
	

	#POS1
	Label(framePosiciones, text = "1", width = 3, bg = bg_root, fg = "white", font = ("Comic Sans MS", 12)).grid(row = 1, column = 0, padx = pad, pady = pad)
	# top1 = {'nom' : StringVar(), 'pasos' : StringVar()}
	Label(framePosiciones, textvariable = top1['nom'], width = 10, bg = bg_root, fg = "white", font = ("Comic Sans MS", 12)).grid(row = 1, column = 1, padx = pad, pady = pad)
	Label(framePosiciones, textvariable = top1['pasos'], width = 4, bg = bg_root, fg = "white", font = ("Comic Sans MS", 12)).grid(row = 1, column = 2, padx = pad, pady = pad)

	#POS2
	Label(framePosiciones, text = "2", width = 3, bg = bg_root, fg = "white", font = ("Comic Sans MS", 12)).grid(row = 2, column = 0, padx = pad, pady = pad)
	# top2 = {'nom' : StringVar(), 'pasos' : StringVar()}
	Label(framePosiciones, textvariable = top2['nom'], width = 10, bg = bg_root, fg = "white", font = ("Comic Sans MS", 12)).grid(row = 2, column = 1, padx = pad, pady = pad)
	Label(framePosiciones, textvariable = top2['pasos'], width = 4, bg = bg_root, fg = "white", font = ("Comic Sans MS", 12)).grid(row = 2, column = 2, padx = pad, pady = pad)

	#POS3
	Label(framePosiciones, text = "3", width = 3, bg = bg_root, fg = "white", font = ("Comic Sans MS", 12)).grid(row = 3, column = 0, padx = pad, pady = pad)
	# top3 = {'nom' : StringVar(), 'pasos' : StringVar()}
	Label(framePosiciones, textvariable = top3['nom'], width = 10, bg = bg_root, fg = "white", font = ("Comic Sans MS", 12)).grid(row = 3, column = 1, padx = pad, pady = pad)
	Label(framePosiciones, textvariable = top3['pasos'], width = 4, bg = bg_root, fg = "white", font = ("Comic Sans MS", 12)).grid(row = 3, column = 2, padx = pad, pady = pad)

	#POS4
	Label(framePosiciones, text = "4", width = 3, bg = bg_root, fg = "white", font = ("Comic Sans MS", 12)).grid(row = 4, column = 0, padx = pad, pady = pad)
	# top4 = {'nom' : StringVar(), 'pasos' : StringVar()}
	Label(framePosiciones, textvariable = top4['nom'], width = 10, bg = bg_root, fg = "white", font = ("Comic Sans MS", 12)).grid(row = 4, column = 1, padx = pad, pady = pad)
	Label(framePosiciones, textvariable = top4['pasos'], width = 4, bg = bg_root, fg = "white", font = ("Comic Sans MS", 12)).grid(row = 4, column = 2, padx = pad, pady = pad)

	#POS5
	Label(framePosiciones, text = "5", width = 3, bg = bg_root, fg = "white", font = ("Comic Sans MS", 12)).grid(row = 5, column = 0, padx = pad, pady = pad)
	# top5 = {'nom' : StringVar(), 'pasos' : StringVar()}
	Label(framePosiciones, textvariable = top5['nom'], width = 10, bg = bg_root, fg = "white", font = ("Comic Sans MS", 12)).grid(row = 5, column = 1, padx = pad, pady = pad)
	Label(framePosiciones, textvariable = top5['pasos'], width = 4, bg = bg_root, fg = "white", font = ("Comic Sans MS", 12)).grid(row = 5, column = 2, padx = pad, pady = pad)

	ubicar(n)

	Button(frameStats, text = "Borrar Highscores", cursor = "hand2", width = 15, bg = bg_root, fg = "white", font = ("Comic Sans MS", 12), command = lambda: borrarHighscore(n)).pack(padx = pad / 2, pady = pad / 2)
	Button(frameStats, text = "Volver a jugar", cursor = "hand2", width = 15, bg = bg_root, fg = "white", font = ("Comic Sans MS", 12), command = inicio).pack(padx = pad / 2, pady = pad / 2)



miConexion.commit()

root.mainloop()