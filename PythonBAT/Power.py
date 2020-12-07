import random

class Power:
	def __init__(self):
		self.nombre=random.choice(["ForcePush","ForcePush","ForcePush"])
		self.imagen="ImagenesBAT/"+self.nombre+"BAT.png"

	def set_Nombre(self,nombre):
		self.nombre =	nombre
	def get_Nombre(self):
		return self.nombre

	def set_imagen(self,imagen):
		self.imagen = imagen
	def get_imagen(self):
		return self.imagen
