from tkinter import *

class Casillero:
	def __init__(self, root, tab, fila, columna, bg, command):
		self.col = columna
		self.row = fila
		self.root = root
		self.but = Button(root, textvariable = tab[self.row][self.col], fg = "white", cursor = "hand2", font = ("Comic Sans MS", 12), command = lambda: command(self.row, self.col), width = 2, height = 1, bg = bg)
		self.but.grid(row = fila, column = columna, padx = 2, pady = 2)

class BotonNivel:
	def __init__(self, root, texto, my_command, bg):
		self.boton = Button(root, width = 8, text = texto, fg = "#FFFFFF", command = my_command, cursor = "hand2", bg = bg, font = ("Comic Sans MS", 14), relief = "groove")
	
	def grid(self, row, column, pad):
		self.boton.grid(row = row, column = column, padx = pad, pady = pad)