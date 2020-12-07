import random
import pygame
class Player:
	def __init__(self):
		self.PosX=random.randint(95,480)
		self.PosY=460
		self.cont=0
		self.nombre=random.choice(["FemBAT","SeguridadBAT","NinjaBAT","PrincesaBAT"])
		self.imagen="ImagenesBAT/"+self.nombre+str(self.cont)+".png"
		self.sonidoAtaque="SonidosBAT/"+self.nombre+"SoundAt.wav"
		self.puntuacionP=0
		self.puntuacionT=0

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

	def set_SonidoAtaque(self,sonido):
		self.sonidoAtaque = sonido
	def get_SonidoAtaque(self):
		return self.sonidoAtaque

	def set_PuntuacionP(self,puntuacionP):
		self.puntuacionP = puntuacionP
	def get_PuntuacionP(self):
		return self.puntuacionP

	def set_PuntuacionT(self,puntuacionT):
		self.puntuacionT = puntuacionT
	def get_PuntuacionT(self):
		return self.puntuacionT		

	
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

	def RecibirAtaqueI(self):
		self.cont = 0 
		self.PosX -= 87

	def RecibirAtaqueD(self):
		self.cont = -1
		self.PosX += 87

	def AumentoPuntos(self):
		self.puntuacionP+=100

	def ReinicioPuntos(self):
		self.puntuacionP=0

	def AumentoaTotal(self,aumento):
		self.puntuacionT+=aumento				

Player1=Player()
Player1.AumentoPuntos()
Player1.AumentoPuntos()
#Player1.ReinicioPuntos()
print(Player1.get_PuntuacionP())