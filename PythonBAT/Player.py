import random
import pygame
class Player:
	def __init__(self):
		self.PosX=random.randint(95,480)
		self.PosY=460
		self.cont=0
		self.nombre=random.choice(["FemBAT","SeguridadBAT","NinjaBAT"])
		self.imagen="ImagenesBAT/"+self.nombre+str(self.cont)+".png"

	def set_PosX(self,PosX):
		self.PosX = PosX
	def get_PosX(self):
		return self.PosX
	
	def set_PosY(self,PosY):
		self.PosY = PosY
	def get_PosY(self):
		return self.PosY
	
	def set_imagen(self,imagen):
		self.imagen = imagen
	def get_imagen(self):
		return self.imagen

	def set_Cont(self,cont):
		self.cont =	cont
	def get_Cont(self):
		return self.cont

	def set_Nombre(self,nombre):
		self.nombre =	nombre
	def get_Nombre(self):
		return self.nombre	
	
	def mostrar(self):
		print("Coordenada x: "+ str(self.PosX))
		print("Coordenada y: "+ str(self.PosY))
		print("Imagen: "+ str(self.imagen))
		
	def MoverDerecha(self):
		#Bronze_PassedTime = pygame.time.get_ticks()
		if self.cont>-1:
			self.PosX+=25
			if self.cont<2:
				self.cont+=1
			else:
				self.cont=0	
		else:
			self.cont=0		
		print(self.cont)
		print(self.PosX)
	
	def MoverIzquierda(self):
		if self.cont<0:	
			self.PosX-=25
			if self.cont>-3:
				self.cont-=1
			else:
				self.cont=-1
		else:
			self.cont=-1			
		print(self.cont)
		print(self.PosX)
	
	def Atacar(self):
		if self.cont>=0:
			self.cont=3
		else:
			self.cont=-4
		print(self.cont)
		print(self.PosX)		

	def Saltar(self):
		self.PosY-=75
		if self.cont>=0:
			self.cont=0
			self.PosX+=15
		else:
			self.cont=-1
			self.PosX-=15 
	def ActualizarSprite(self):
		self.imagen="ImagenesBAT/"+self.nombre+str(self.cont)+".png"

"""Player1=Player()
Player1.MoverDerecha()
Player1.MoverDerecha()
Player1.MoverIzquierda()
Player1.ActualizarSprite()
print(Player1.get_imagen())"""