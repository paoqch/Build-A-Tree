import random

class Token:
	def __init__(self):
		self.figura = random.choice(["circulo","rombo","cuadrado","triangulo"])
		if self.figura == "circulo":
			self.valor = random.choice([17,23,36,44,58,65,70,81,92])
			self.arbol = "AVL"
		elif self.figura == "rombo":
			self.valor = random.choice([5,12,28,30,45,51,63,74,86,97])
			self.arbol = "BST"
		elif self.figura == "cuadrado":
			self.valor = random.choice([7,10,25,34,42,56,61,77,83,99])
			self.arbol = "B"
		elif self.figura == "triangulo":
			self.valor = random.choice([3,18,20,39,41,54,67,72,85,96])
			self.arbol = "Splay"			
		self.imagen = "ImagenesBAT/Tokens/"+str(self.valor)+".png"

	def set_Figura(self,figura):
		self.figura = figura
	def get_Figura(self):
		return self.figura
		
	def set_Valor(self,valor):
		self.valor = valor
	def get_Valor(self):
		return self.valor	

	def set_imagen(self,imagen):
		self.imagen = imagen
	def get_imagen(self):
		return self.imagen

	def set_Arbol(self,arbol):
		self.arbol = arbol
	def get_Arbol(self):
		return self.arbol	


	