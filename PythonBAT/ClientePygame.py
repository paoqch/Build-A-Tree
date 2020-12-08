### LIBRARIES ###------------------------------------------------------------------------------------------------------
import pygame  # Load all Pygame functionalities
import sys     # Increase the capacity of recursion
import random  # To use of random options
import time    # To control execution times and waiting periods
import threading # For the implementation and control of the animation threads
sys.setrecursionlimit(10**9) # Increased recursion limit
from Player import Player
from Power import Power
from Token import Token
import socket
import threading

### MAIN FUNCTION OF THE GAME (GAMEPLAY) ###
pygame.init()

def main():
	global data1
	data1="1"
	global OrdenChallenges
	global Primero
	global Segundo
	global Ultimo 
	global ChallengeActual

	def Conexion1(msg):
		HOST = "localhost"
		PORT = 5555
		msg2 = msg
		global s
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		    s.connect((HOST,PORT))
		    s.sendall((msg2.encode()))	
		    data1 = s.recv(1024)
		OrdenChallenges=str(data1).split("|")[1]
		global Primero
		Primero = OrdenChallenges.split(",")[0]
		global Segundo
		Segundo = OrdenChallenges.split(",")[1]
		global Ultimo
		Ultimo = OrdenChallenges.split(",")[2].split("'")[0]
		print ("Recibido ",repr(data1))
		print("Primero: "+Primero+" Segundo: "+Segundo+" Ultimo: "+Ultimo)
		#print(str(data1.split(",")[0]))
		
	

	def Conexion(msg):
		HOST = "localhost"
		PORT = 5555
		msg2 = msg
		global s
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		    s.connect((HOST,PORT))
		    s.sendall((msg2.encode()))
		    data = s.recv(1024)
		#print ("Recibido ",repr(data))	

	VentanaJuego =  pygame.display.set_mode([600,630])
	Mapa_Image = pygame.image.load("ImagenesBat/MapaBAT.png").convert()
	ShieldIm = pygame.image.load("ImagenesBat/ShieldBAT.png")
	P1Win_Image = pygame.image.load("ImagenesBAT/P1WinBAT.jpg") 
	P2Win_Image = pygame.image.load("ImagenesBAT/P2WinBAT.jpg") 
	TokenObtenido = pygame.mixer.Sound("SonidosBAT/PrincesaBATSoundAt.wav")
	TokenIncorrecto = pygame.mixer.Sound("SonidosBAT/PrincesaBATSoundAt.wav")
	Soundtrack1 = pygame.mixer.Sound("SonidosBAT/PrincesaBATSoundAt.wav")
	Soundtrack2 = pygame.mixer.Sound("SonidosBAT/PrincesaBATSoundAt.wav")
	Soundtrack3 = pygame.mixer.Sound("SonidosBAT/PrincesaBATSoundAt.wav")
	font1 = pygame.font.SysFont("Britannic" , 30)
	TextColor = (74,48,111)
	# JUGADOR 1 # ==========================================================================================================
	Player1 = Player()
	Conexion1("inicio")
	Player_Image = pygame.image.load(Player1.get_imagen())
	P = pygame.image.load("ImagenesBAT/EstrellaBAT.png")
	Player1.mostrar()
	Player1At = pygame.mixer.Sound(Player1.get_SonidoAtaque())
	global IndicadorPoder
	IndicadorPoder = [False]
	global ContadorPoder
	ContadorPoder = 0


	# JUGADOR 2 # ==========================================================================================================
	Player2 = Player()
	Conexion("H3")
	Conexion("H3")
	Player2_Image = pygame.image.load(Player2.get_imagen())
	PP = pygame.image.load("ImagenesBAT/EstrellaBAT.png")
	Player2.mostrar()
	Player2At = pygame.mixer.Sound(Player2.get_SonidoAtaque())
	global IndicadorPoder2
	IndicadorPoder2 = [False]
	global ContadorPoder2
	ContadorPoder2 = 0

	# ======================================================================================================================

	ChallengeActual = Primero
	PoderObtenido = pygame.mixer.Sound("SonidosBAT/EstrellaSoundBAT.mp3")

	global Animation_Estrella
	Animation_Estrella = [True]
	global Animation_Tokens
	Animation_Tokens = [True]
	global Challenge_Image

	global FinChallenge
	FinChallenge = [False]
	global FinJuego
	FinJuego = [False]
	global InicioOst
	InicioOst = [False]
	global SiguienteOst
	SiguienteOst = [False]
	global UltimoOst
	UltimoOst = [False]
	global contChallenge
	contChallenge = 0
	global contChallenge2
	contChallenge2 = 0
	global contChallenge3
	contChallenge3 = 0

	global contSoundtrack
	contSoundtrack = 0
	global contSoundtrack2
	contSoundtrack2 = 0
	global contSoundtrack3
	contSoundtrack3 = 0

	#pygame.key.set_repeat(1, 1000)
	while True:
		Challenge_Image = pygame.image.load("ImagenesBAT/"+ChallengeActual+"BAT.png")
		global PoderSaltoUsado
		PoderSaltoUsado = [True]

		global PoderSaltoUsado2
		PoderSaltoUsado2 = [True]

		def Retroceder(P1,P2):
			Player_Image2 = pygame.image.load(Player2.get_imagen())
			cont = 0
			if Player1.get_PosX()<Player2.get_PosX():
				Player2.RecibirAtaqueD()
				Player2.ActualizarSprite()
				Player_Image2 = pygame.image.load(Player2.get_imagen())
				while cont<81:
					P1+=10
					cont+=10
					VentanaJuego.blit(Player_Image2,(P1,P2))		
					pygame.time.wait(20)
			if Player1.get_PosX()>Player2.get_PosX():
				Player2.RecibirAtaqueI()
				Player2.ActualizarSprite()
				Player_Image2 = pygame.image.load(Player2.get_imagen())
				while cont<81:
					P1-=10
					cont+=10
					VentanaJuego.blit(Player_Image2,(P1,P2))		
					pygame.time.wait(20)
			if Player2.get_PosX()>515:
				P1=515
				P2=Player2.get_PosY()
				Player2.set_PosY(531)
				Player2.set_PosX(-101)
				P3 = Player2.get_PosX()
				TCaida2 = threading.Thread(target = Caida2,args=(P1,P2,P3))
				TCaida2.start()
			if Player2.get_PosX()<25:
				P1=25
				P2=Player2.get_PosY()
				Player2.set_PosY(530)
				Player2.set_PosX(-100)
				P3 = Player2.get_PosX()
				TCaida2 = threading.Thread(target = Caida2,args=(P1,P2,P3))
				TCaida2.start()					

		def Retroceder2(P1,P2):
			Player_Image2 = pygame.image.load(Player1.get_imagen())
			cont = 0
			if Player2.get_PosX()<Player1.get_PosX():
				Player1.RecibirAtaqueD()
				Player1.ActualizarSprite()
				Player_Image2 = pygame.image.load(Player1.get_imagen())
				while cont<81:
					P1+=10
					cont+=10
					VentanaJuego.blit(Player_Image2,(P1,P2))		
					pygame.time.wait(20)
			if Player2.get_PosX()>Player1.get_PosX():
				Player1.RecibirAtaqueI()
				Player1.ActualizarSprite()
				Player_Image2 = pygame.image.load(Player1.get_imagen())
				while cont<81:
					P1-=10
					cont+=10
					VentanaJuego.blit(Player_Image2,(P1,P2))		
					pygame.time.wait(20)
			if Player1.get_PosX()>515:
				P1=515
				P2=Player1.get_PosY()
				Player1.set_PosY(531)
				Player1.set_PosX(-101)
				P3 = Player1.get_PosX()
				TCaida = threading.Thread(target = Caida,args=(P1,P2,P3))
				TCaida.start()
			if Player1.get_PosX()<25:
				P1=25
				P2=Player1.get_PosY()
				Player1.set_PosY(530)
				Player1.set_PosX(-100)
				P3 = Player1.get_PosX()
				TCaida = threading.Thread(target = Caidaa,args=(P1,P2,P3))
				TCaida.start()				

		def Subida(P1,P2):
			Player_Image2 = pygame.image.load(Player1.get_imagen())
			cont = P2
			while cont>129:
				P2-=10
				cont-=10
				VentanaJuego.blit(Player_Image2,(P1,P2))		
				pygame.time.wait(20)		
			if P1 == 25: 	
				Player1.set_PosY(129)
				Player1.set_PosX(35)
			else:
				Player1.set_PosY(129)
				Player1.set_PosX(505)

		def Subida2(P1,P2):
			Player2_Image2 = pygame.image.load(Player2.get_imagen())
			cont = P2
			while cont>129:
				P2-=10
				cont-=10
				VentanaJuego.blit(Player2_Image2,(P1,P2))		
				pygame.time.wait(20)		
			if P1 == 25: 	
				Player2.set_PosY(129)
				Player2.set_PosX(35)
			else:
				Player2.set_PosY(129)
				Player2.set_PosX(505)			
		
		def Caida(P1,P2,P3):
			Player_Image2 = pygame.image.load(Player1.get_imagen())
			cont = P2
			while cont<630:
				P2+=10
				cont+=10
				VentanaJuego.blit(Player_Image2,(P1,P2))		
				pygame.time.wait(20)
				if PoderSaltoUsado[0]==False:
					cont=630
			PoderSaltoUsado[0]=True				
				
			Player1.set_PosY(630)
			if P3 == 25:
				Player1.set_PosX(25)
			else:
				Player1.set_PosX(515)

		def Caida2(P1,P2,P3):
			Player2_Image2 = pygame.image.load(Player2.get_imagen())
			cont = P2
			while cont<630:
				P2+=10
				cont+=10
				VentanaJuego.blit(Player2_Image2,(P1,P2))		
				pygame.time.wait(20)
				if PoderSaltoUsado2[0]==False:
					cont=630
			PoderSaltoUsado2[0]=True				
				
			Player2.set_PosY(630)
			if P3 == 25:
				Player2.set_PosX(25)
			else:
				Player2.set_PosX(515)			
		
		Tiempo = pygame.time.get_ticks()
		#print(Tiempo//1000)
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				pygame.quit()
			if event.type == pygame.KEYDOWN:
				#===========================================IZQUIERDA==================================================	
				if event.key == pygame.K_LEFT:
					Player1.MoverIzquierda()
					Player1.ActualizarSprite()
					print(Player1.get_PosY())
					Player_Image = pygame.image.load(Player1.get_imagen())
					if Player1.get_PosY()==460 and Player1.get_PosX()<25:
						P1=25
						P2=Player1.get_PosY()
						Player1.set_PosY(530)
						Player1.set_PosX(-100)
						P3 = Player1.get_PosX()

						TCaida = threading.Thread(target = Caida,args=(P1,P2,P3))
						TCaida.start()


					if Player1.get_PosY()==352 and Player1.get_PosX()<190:
						Player1.set_PosY(460)
					
					if Player1.get_PosY()==283 and Player1.get_PosX()<25:
						P1=25
						P2=Player1.get_PosY()
						Player1.set_PosY(530)
						Player1.set_PosX(-100)
						P3 = Player1.get_PosX()

						TCaida = threading.Thread(target = Caida,args=(P1,P2,P3))
						TCaida.start()

					if Player1.get_PosY()==213 and Player1.get_PosX()<195:
						Player1.set_PosY(283)
					
					if Player1.get_PosY()==129 and Player1.get_PosX()<25:
						P1=25
						P2=Player1.get_PosY()
						Player1.set_PosY(530)
						Player1.set_PosX(-100)
						P3 = Player1.get_PosX()

						TCaida = threading.Thread(target = Caida,args=(P1,P2,P3))
						TCaida.start()
					
					if Player1.get_PosY()==43 and Player1.get_PosX()<130:
						Player1.set_PosY(129)



				if event.key == pygame.K_a:
					Player2.MoverIzquierda()
					Player2.ActualizarSprite()
					print(Player2.get_PosY())
					Player2_Image = pygame.image.load(Player2.get_imagen())
					if Player2.get_PosY()==460 and Player2.get_PosX()<25:
						P1=25
						P2=Player2.get_PosY()
						Player2.set_PosY(530)
						Player2.set_PosX(-100)
						P3 = Player2.get_PosX()

						TCaida2 = threading.Thread(target = Caida2,args=(P1,P2,P3))
						TCaida2.start()


					if Player2.get_PosY()==352 and Player2.get_PosX()<190:
						Player2.set_PosY(460)
					
					if Player2.get_PosY()==283 and Player2.get_PosX()<25:
						P1=25
						P2=Player2.get_PosY()
						Player2.set_PosY(530)
						Player2.set_PosX(-100)
						P3 = Player2.get_PosX()

						TCaida2 = threading.Thread(target = Caida2,args=(P1,P2,P3))
						TCaida2.start()

					if Player2.get_PosY()==213 and Player2.get_PosX()<195:
						Player2.set_PosY(283)
					
					if Player2.get_PosY()==129 and Player2.get_PosX()<25:
						P1=25
						P2=Player2.get_PosY()
						Player2.set_PosY(530)
						Player2.set_PosX(-100)
						P3 = Player2.get_PosX()

						TCaida2 = threading.Thread(target = Caida2,args=(P1,P2,P3))
						TCaida2.start()
					
					if Player2.get_PosY()==43 and Player2.get_PosX()<130:
						Player2.set_PosY(129)										
                #================================================DERECHA================================================				
				if event.key == pygame.K_RIGHT:
					ActualX = Player1.get_PosX()					
					Player1.MoverDerecha()
					Player1.ActualizarSprite()
					Player_Image = pygame.image.load(Player1.get_imagen())
					if Player1.get_PosY()==460 and Player1.get_PosX()>515:
						P1=515
						P2=Player1.get_PosY()
						Player1.set_PosY(531)
						Player1.set_PosX(-101)
						P3 = Player1.get_PosX()

						TCaida = threading.Thread(target = Caida,args=(P1,P2,P3))
						TCaida.start()
					
					if Player1.get_PosY()==352 and Player1.get_PosX()>515:
						P1=515
						P2=Player1.get_PosY()
						Player1.set_PosY(531)
						Player1.set_PosX(-101)
						P3 = Player1.get_PosX()

						TCaida = threading.Thread(target = Caida,args=(P1,P2,P3))
						TCaida.start()

					if Player1.get_PosY()==283 and Player1.get_PosX()>210:
						Player1.set_PosY(352)
					if Player1.get_PosY()==213 and Player1.get_PosX()>430:
						Player1.set_PosY(352)
					
					if Player1.get_PosY()==129 and Player1.get_PosX()>515:
						P1=515
						P2=Player1.get_PosY()
						Player1.set_PosY(531)
						Player1.set_PosX(-101)
						P3 = Player1.get_PosX()

						TCaida = threading.Thread(target = Caida,args=(P1,P2,P3))
						TCaida.start()

					if Player1.get_PosY()==43 and Player1.get_PosX()>417:
						Player1.set_PosY(129)		
					if Player1.get_PosY()==530:
						Player1.set_PosX(ActualX)



				if event.key == pygame.K_d:
					ActualX = Player2.get_PosX()					
					Player2.MoverDerecha()
					Player2.ActualizarSprite()
					Player2_Image = pygame.image.load(Player2.get_imagen())
					if Player2.get_PosY()==460 and Player2.get_PosX()>515:
						P1=515
						P2=Player2.get_PosY()
						Player2.set_PosY(531)
						Player2.set_PosX(-101)
						P3 = Player2.get_PosX()

						TCaida2 = threading.Thread(target = Caida2,args=(P1,P2,P3))
						TCaida2.start()
					
					if Player2.get_PosY()==352 and Player2.get_PosX()>515:
						P1=515
						P2=Player2.get_PosY()
						Player2.set_PosY(531)
						Player2.set_PosX(-101)
						P3 = Player2.get_PosX()

						TCaida2 = threading.Thread(target = Caida2,args=(P1,P2,P3))
						TCaida2.start()

					if Player2.get_PosY()==283 and Player2.get_PosX()>210:
						Player2.set_PosY(352)
					if Player2.get_PosY()==213 and Player2.get_PosX()>430:
						Player2.set_PosY(352)
					
					if Player2.get_PosY()==129 and Player2.get_PosX()>515:
						P1=515
						P2=Player2.get_PosY()
						Player2.set_PosY(531)
						Player2.set_PosX(-101)
						P3 = Player2.get_PosX()

						TCaida2 = threading.Thread(target = Caida2,args=(P1,P2,P3))
						TCaida2.start()

					if Player2.get_PosY()==43 and Player2.get_PosX()>417:
						Player2.set_PosY(129)		
					if Player2.get_PosY()==530:
						Player2.set_PosX(ActualX)
						
				#==============================================ATAQUE===================================================	
				if event.key == pygame.K_RSHIFT:
					if ContadorPoder == 2:
						Player1.Atacar()
						Player1.ActualizarSprite()
						Player_Image = pygame.image.load(Player1.get_imagen())
						ContadorPoder = 0
						Player1At.play()
						if Player1.get_Cont()>=0:
							if Player2.get_Cont()>=0:
								if Player1.get_PosY()==Player2.get_PosY() and Player1.get_PosX()<Player2.get_PosX()+45 and Player1.get_PosX()>Player2.get_PosX()-85: 
									if ContadorPoder2==3:
										ContadorPoder2=0
									else:	
										P1=Player2.get_PosX()
										P2=Player2.get_PosY()
										Thread_Retro = threading.Thread(target = Retroceder, args = (P1,P2))
										Thread_Retro.start()
							if Player2.get_Cont()<=-1:
								if Player1.get_PosY()==Player2.get_PosY() and Player1.get_PosX()<Player2.get_PosX()+45 and Player1.get_PosX()>Player2.get_PosX()-85: 
									if ContadorPoder2==3:
										ContadorPoder2=0
									else:	
										P1=Player1.get_PosX()
										P2=Player1.get_PosY()
										Thread_Retro2 = threading.Thread(target = Retroceder, args = (P1,P2))
										Thread_Retro2.start()		
						if Player1.get_Cont()<=-1:
							if Player2.get_Cont()<=-1:
								if Player1.get_PosY()==Player2.get_PosY() and Player1.get_PosX()>Player2.get_PosX()-45 and Player1.get_PosX()<Player2.get_PosX()+85: 
									if ContadorPoder2==3:
										ContadorPoder2=0
									else:	
										P1=Player2.get_PosX()
										P2=Player2.get_PosY()
										Thread_Retro = threading.Thread(target = Retroceder, args = (P1,P2))
										Thread_Retro.start()
							if Player2.get_Cont()>=0:
								if Player1.get_PosY()==Player2.get_PosY() and Player1.get_PosX()>Player2.get_PosX()-85 and Player1.get_PosX()>Player2.get_PosX()+45:
									if ContadorPoder2==3:
										ContadorPoder2=0
									else:
										P1=Player2.get_PosX()
										P2=Player2.get_PosY()
										Thread_Retro2 = threading.Thread(target = Retroceder, args = (P1,P2))
										Thread_Retro2.start()#if Player1.get_PosY()==Player2.get_PosY() and Player1.get_PosX()<
				
				if event.key == pygame.K_f:
					if ContadorPoder2 == 2:
						Player2.Atacar()
						Player2.ActualizarSprite()
						Player2_Image = pygame.image.load(Player2.get_imagen())
						ContadorPoder2 = 0
						Player2At.play()
						if Player2.get_Cont()>=0:
							if Player1.get_Cont()>=0:
								if Player2.get_PosY()==Player1.get_PosY() and Player2.get_PosX()<Player1.get_PosX()+45 and Player2.get_PosX()>Player1.get_PosX()-85: 
									if ContadorPoder==3:
										ContadorPoder=0
									else:	
										P1=Player1.get_PosX()
										P2=Player1.get_PosY()
										Thread_Retro3 = threading.Thread(target = Retroceder2, args = (P1,P2))
										Thread_Retro3.start()
							if Player1.get_Cont()<=-1:
								if Player2.get_PosY()==Player1.get_PosY() and Player2.get_PosX()<Player1.get_PosX()+45 and Player2.get_PosX()>Player1.get_PosX()-85: 
									if ContadorPoder==3:
										ContadorPoder=0
									else:	
										P1=Player1.get_PosX()
										P2=Player1.get_PosY()
										Thread_Retro4 = threading.Thread(target = Retroceder2, args = (P1,P2))
										Thread_Retro4.start()		
						if Player2.get_Cont()<=-1:
							if Player1.get_Cont()<=-1:
								if Player2.get_PosY()==Player1.get_PosY() and Player2.get_PosX()>Player1.get_PosX()-45 and Player2.get_PosX()<Player1.get_PosX()+85: 
									if ContadorPoder==3:
										ContadorPoder=0
									else:	
										P1=Player1.get_PosX()
										P2=Player1.get_PosY()
										Thread_Retro3 = threading.Thread(target = Retroceder2, args = (P1,P2))
										Thread_Retro3.start()
							if Player1.get_Cont()>=0:
								if Player2.get_PosY()==Player1.get_PosY() and Player2.get_PosX()>Player1.get_PosX()-85 and Player2.get_PosX()>Player1.get_PosX()+45:
									if ContadorPoder==3:
										ContadorPoder=0
									else:
										P1=Player1.get_PosX()
										P2=Player1.get_PosY()
										Thread_Retro4 = threading.Thread(target = Retroceder2, args = (P1,P2))
										Thread_Retro4.start()#if Player1.get_PosY()==Player2.get_PosY() and Player1.get_PosX()<

            	#==============================================ARRIBA===================================================	
				if event.key == pygame.K_UP:
					ActualX = Player1.get_PosX()
					ActualY = Player1.get_PosY()
					print(ActualY)
					Player1.Saltar()
					Player1.ActualizarSprite()
					Player_Image = pygame.image.load(Player1.get_imagen())
					if Player1.get_PosY()>340 and Player1.get_PosY()<400 and Player1.get_PosX()>180 and Player1.get_PosX()<470:
						Player1.set_PosY(352)
						print(Player1.get_PosY())
					elif Player1.get_PosY()>264 and Player1.get_PosY()<299 and Player1.get_PosX()>56 and Player1.get_PosX()<210:
						Player1.set_PosY(283)
						print(Player1.get_PosY())
					elif Player1.get_PosY()>194 and Player1.get_PosY()<230 and Player1.get_PosX()>185 and Player1.get_PosX()<430:
						Player1.set_PosY(213)
						print(Player1.get_PosY())
					elif Player1.get_PosY()>110 and Player1.get_PosY()<145 and Player1.get_PosX()>190 and Player1.get_PosX()<500:
						Player1.set_PosY(129)
						print(Player1.get_PosY())
					elif Player1.get_PosY()>25 and Player1.get_PosY()<60 and Player1.get_PosX()>140 and Player1.get_PosX()<460:
						Player1.set_PosY(43)
						print(Player1.get_PosY())
					elif ActualX ==-100 and ContadorPoder==1:
						P1=25
						P2=Player1.get_PosY()
						Player1.set_Cont(4)
						Player1.ActualizarSprite()
						PoderSaltoUsado[0] = False
						Player_Image = pygame.image.load(Player1.get_imagen())
						Ts = threading.Thread(target = Subida,args=(P1,P2))
						Ts.start()
						ContadorPoder=0
					elif ActualX ==-101 and ContadorPoder==1:
						P1=515
						P2=Player1.get_PosY()
						Player1.set_Cont(-5)
						Player1.ActualizarSprite()
						PoderSaltoUsado[0] = False
						Player_Image = pygame.image.load(Player1.get_imagen())
						Ts = threading.Thread(target = Subida,args=(P1,P2))
						Ts.start()
						ContadorPoder=0
					else:
						Player1.set_PosY(ActualY)
						Player1.set_PosX(ActualX)



				if event.key == pygame.K_w:
					ActualX = Player2.get_PosX()
					ActualY = Player2.get_PosY()
					print(ActualY)
					Player2.Saltar()
					Player2.ActualizarSprite()
					Player2_Image = pygame.image.load(Player2.get_imagen())
					if Player2.get_PosY()>340 and Player2.get_PosY()<400 and Player2.get_PosX()>180 and Player2.get_PosX()<470:
						Player2.set_PosY(352)
						print(Player2.get_PosY())
					elif Player2.get_PosY()>264 and Player2.get_PosY()<299 and Player2.get_PosX()>56 and Player2.get_PosX()<210:
						Player2.set_PosY(283)
						print(Player2.get_PosY())
					elif Player2.get_PosY()>194 and Player2.get_PosY()<230 and Player2.get_PosX()>185 and Player2.get_PosX()<430:
						Player2.set_PosY(213)
						print(Player2.get_PosY())
					elif Player2.get_PosY()>110 and Player2.get_PosY()<145 and Player2.get_PosX()>190 and Player2.get_PosX()<500:
						Player2.set_PosY(129)
						print(Player2.get_PosY())
					elif Player2.get_PosY()>25 and Player2.get_PosY()<60 and Player2.get_PosX()>140 and Player2.get_PosX()<460:
						Player2.set_PosY(43)
						print(Player2.get_PosY())
					elif ActualX ==-100 and ContadorPoder2==1:
						P1=25
						P2=Player2.get_PosY()
						Player2.set_Cont(4)
						Player2.ActualizarSprite()
						PoderSaltoUsado2[0] = False
						Player2_Image = pygame.image.load(Player2.get_imagen())
						Ts2 = threading.Thread(target = Subida2,args=(P1,P2))
						Ts2.start()
						ContadorPoder2=0
					elif ActualX ==-101 and ContadorPoder2==1:
						P1=515
						P2=Player2.get_PosY()
						Player2.set_Cont(-5)
						Player2.ActualizarSprite()
						PoderSaltoUsado2[0] = False
						Player2_Image = pygame.image.load(Player2.get_imagen())
						Ts2 = threading.Thread(target = Subida2,args=(P1,P2))
						Ts2.start()
						ContadorPoder2=0
					else:
						Player2.set_PosY(ActualY)
						Player2.set_PosX(ActualX)				
				
				#===================================================ABAJO==============================================	
				if event.key == pygame.K_DOWN:
					if Player1.get_Cont()>=0:
						Player1.set_Cont(0)
					else:
						Player1.set_Cont(-1)
					Player1.ActualizarSprite()
					Player_Image = pygame.image.load(Player1.get_imagen())
					if Player1.get_PosY()==352:
						Player1.set_PosY(460)
					if Player1.get_PosY()==129:
						if Player1.get_PosX()>49 and Player1.get_PosX()<200: 
							Player1.set_PosY(Player1.get_PosY())
						else:
							Player1.set_PosY(213)	
					if Player1.get_PosY()==43:
						Player1.set_PosY(129)

				

				if event.key == pygame.K_s:
					if Player2.get_Cont()>=0:
						Player2.set_Cont(0)
					else:
						Player2.set_Cont(-1)
					Player2.ActualizarSprite()
					Player2_Image = pygame.image.load(Player2.get_imagen())
					if Player2.get_PosY()==352:
						Player2.set_PosY(460)
					if Player2.get_PosY()==129:
						if Player2.get_PosX()>49 and Player2.get_PosX()<200: 
							Player2.set_PosY(Player2.get_PosY())
						else:
							Player2.set_PosY(213)	
					if Player2.get_PosY()==43:
						Player2.set_PosY(129)				

			# =============================================================================================================================
		def Estrella():
			Estrella_x=random.randint(35,505)
			Estrella_y=-100
			Estrella_PassedTime=pygame.time.get_ticks()
			Estrella_ActualTime=0
			while True:
				Estrella_y+=6
				pygame.time.wait(20)
				Estrella_ActualTime = pygame.time.get_ticks()
				if (Estrella_ActualTime - Estrella_PassedTime)//1000>=6:
					Estrella_PassedTime = pygame.time.get_ticks()
					Animation_Estrella[0] = True
					break
				if Estrella_y>Player1.get_PosY() and Estrella_y < Player1.get_PosY() + 90 and Estrella_x > Player1.get_PosX() and Estrella_x < Player1.get_PosX()+55:	
					PoderObtenido.play()
					Estrella_x=-111
					IndicadorPoder[0]=True
				if Estrella_y>Player1.get_PosY() and Estrella_y < Player1.get_PosY() + 90 and Estrella_x < Player1.get_PosX() and Estrella_x > Player1.get_PosX()-55:	
					PoderObtenido.play()
					Estrella_x=-111
					IndicadorPoder[0]=True
				if Estrella_y>Player2.get_PosY() and Estrella_y < Player2.get_PosY() + 95 and Estrella_x > Player2.get_PosX() and Estrella_x < Player2.get_PosX()+55:	
					PoderObtenido.play()
					Estrella_x=-111
					IndicadorPoder2[0]=True
				if Estrella_y>Player2.get_PosY() and Estrella_y < Player2.get_PosY() + 95 and Estrella_x < Player2.get_PosX() and Estrella_x > Player2.get_PosX()-55:	
					PoderObtenido.play()
					Estrella_x=-111
					IndicadorPoder2[0]=True		

				Star = pygame.image.load("ImagenesBAT/EstrellaBAT.png")
				VentanaJuego.blit(Star,(Estrella_x,Estrella_y))

		def Tokens():
			Token_x=random.randint(35,505)
			Token_y=-100
			Token_PassedTime=pygame.time.get_ticks()
			Token_ActualTime=0
			Token0 = Token()
			while True:
				Token_y+=6
				pygame.time.wait(20)
				Token_ActualTime = pygame.time.get_ticks()
				if (Token_ActualTime - Token_PassedTime)//1000>=4:
					Token_PassedTime = pygame.time.get_ticks()
					Animation_Tokens[0] = True
					break
				if Token_y>Player1.get_PosY() and Token_y < Player1.get_PosY() + 90 and Token_x > Player1.get_PosX() and Token_x < Player1.get_PosX()+55:	
					Token_x=-111
					print(Token0.get_Figura()+" "+str(Token0.get_Valor()))
					if Token0.get_Arbol()==ChallengeActual:
						TokenObtenido.play()
						Player1.AumentoPuntos()
						Conexion(Token0.get_Arbol()+"/1/"+str(Token0.get_Valor()))
					else:
						TokenIncorrecto.play()
						Player1.ReinicioPuntos()
						Conexion(Token0.get_Arbol()+"/1/0")
					Token_PassedTime = pygame.time.get_ticks()

				elif Token_y>Player1.get_PosY() and Token_y < Player1.get_PosY() + 90 and Token_x < Player1.get_PosX() and Token_x > Player1.get_PosX()-55:	
					Token_x=-111
					print(Token0.get_Figura()+" "+str(Token0.get_Valor()))
					if Token0.get_Arbol()==ChallengeActual:
						TokenObtenido.play()
						Player1.AumentoPuntos()
						Conexion(Token0.get_Arbol()+"/1/"+str(Token0.get_Valor()))
					else:
						TokenIncorrecto.play()
						Player1.ReinicioPuntos()
						Conexion(Token0.get_Arbol()+"/1/0")
					Token_PassedTime = pygame.time.get_ticks()

				elif Token_y>Player2.get_PosY() and Token_y < Player2.get_PosY() + 95 and Token_x > Player2.get_PosX() and Token_x < Player2.get_PosX()+55:	
					Token_x=-111
					print(Token0.get_Figura()+" "+str(Token0.get_Valor()))
					if Token0.get_Arbol()==ChallengeActual:
						TokenObtenido.play()
						Player2.AumentoPuntos()
						Conexion(Token0.get_Arbol()+"/2/"+str(Token0.get_Valor()))
					else:
						TokenIncorrecto.play()
						Player2.ReinicioPuntos()
						Conexion(Token0.get_Arbol()+"/2/0")
					Token_PassedTime = pygame.time.get_ticks()

				elif Token_y>Player2.get_PosY() and Token_y < Player2.get_PosY() + 95 and Token_x < Player2.get_PosX() and Token_x > Player2.get_PosX()-55:	
					Token_x=-111
					print(Token0.get_Figura()+" "+str(Token0.get_Valor()))
					if Token0.get_Arbol()==ChallengeActual:
						TokenObtenido.play()
						Player2.AumentoPuntos()
						Conexion(Token0.get_Arbol()+"/2/"+str(Token0.get_Valor()))
					else:
						TokenIncorrecto.play()
						Player2.ReinicioPuntos()
						Conexion(Token0.get_Arbol()+"/2/0")
					Token_PassedTime = pygame.time.get_ticks()
				
				Token_Image = pygame.image.load(Token0.get_imagen())
				Token_Image = pygame.transform.scale(Token_Image, (40, 40))
				VentanaJuego.blit(Token_Image,(Token_x,Token_y))		
		
		if ContadorPoder==0:
			P = pygame.image.load("ImagenesBAT/EmptyBAT.png")
		if IndicadorPoder[0]:
			PoderActual = Power()
			P = pygame.image.load(PoderActual.get_imagen())
			if PoderActual.get_Nombre()=="AirJump":
				ContadorPoder = 1
			elif PoderActual.get_Nombre()=="ForcePush":
				ContadorPoder = 2
			else:
				ContadorPoder = 3	
			IndicadorPoder[0]=False
		
		if ContadorPoder2==0:
			PP = pygame.image.load("ImagenesBAT/EmptyBAT.png")
		if IndicadorPoder2[0]:
			PoderActual2 = Power()
			PP = pygame.image.load(PoderActual2.get_imagen())
			if PoderActual2.get_Nombre()=="AirJump":
				ContadorPoder2 = 1
			elif PoderActual2.get_Nombre()=="ForcePush":
				ContadorPoder2 = 2
			else:
				ContadorPoder2 = 3	
			IndicadorPoder2[0]=False
		
		"""if Tiempo>0:
			contSoundtrack+=1
			if contSoundtrack==1:
				InicioOst[0]=True
		if Tiempo>56000:
			contSoundtrack2+=1
			if contSoundtrack2==1:
				SiguienteOst[0]=True
		if Tiempo>160000:
			contSoundtrack3+=1
			if contSoundtrack3==1:
				UltimoOst[0]=True"""			

		if Tiempo>80000:
			contChallenge+=1
			ChallengeActual=Segundo
			if contChallenge==1:
				FinChallenge[0]=True

		if Tiempo>160000:
			contChallenge2+=1
			ChallengeActual=Ultimo
			if contChallenge2==1:
				FinChallenge[0]=True

		if Tiempo>240000:
			contChallenge3+=1
			if contChallenge3==1:
				FinJuego[0]=True		

		if FinChallenge[0]:
			Player1.AumentoaTotal(Player1.get_PuntuacionP())
			Player1.ReinicioPuntos()
			Player2.AumentoaTotal(Player2.get_PuntuacionP())
			Player2.ReinicioPuntos()
			print("Parcial: "+str(Player1.get_PuntuacionP())+" Total: "+str(Player1.get_PuntuacionT()))
			print("Parcial: "+str(Player2.get_PuntuacionP())+" Total: "+str(Player2.get_PuntuacionT()))
			FinChallenge[0]=False

		if InicioOst[0]:
			Soundtrack1.play()
		if SiguienteOst[0]:
			Soundtrack2.play()
		if UltimoOst[0]:
			Soundtrack3.play()		

					
		if Animation_Estrella[0]:
			Thread_Estrella = threading.Thread(target = Estrella, args = ())
			Thread_Estrella.start()
			Animation_Estrella[0]=False

		if Animation_Tokens[0]:
			Thread_Token = threading.Thread(target = Tokens, args = ())
			Thread_Token.start()
			Animation_Tokens[0]=False

		if Player1.get_PosY()>=630:
			Player1.set_PosY(43)
			Player1.set_Cont(0)
			Player1.ActualizarSprite()
			Player1.set_PosX(random.randint(160,440))
			pygame.time.delay(1000)

		if Player2.get_PosY()>=630:
			Player2.set_PosY(43)
			Player2.set_Cont(0)
			Player2.ActualizarSprite()
			Player2.set_PosX(random.randint(160,440))
			pygame.time.delay(1000)	


		VentanaJuego.blit(Mapa_Image,(0,0))
		VentanaJuego.blit(Player_Image,(Player1.get_PosX(),Player1.get_PosY()))

		VentanaJuego.blit(Player2_Image,(Player2.get_PosX(),Player2.get_PosY()))
		
		if ContadorPoder == 3:
			Escudo = pygame.image.load("ImagenesBAT/Shield0BAT.png")
			VentanaJuego.blit(Escudo,(Player1.get_PosX()-15,Player1.get_PosY()))

		if ContadorPoder2 == 3:
			Escudo2 = pygame.image.load("ImagenesBAT/Shield0BAT.png")
			VentanaJuego.blit(Escudo2,(Player2.get_PosX()-15,Player2.get_PosY()))	
		VentanaJuego.blit(Challenge_Image,(470,0))
		VentanaJuego.blit(P,(60,2))
		VentanaJuego.blit(PP,(200,2))

		P1PuntosP_Label = font1.render(str(Player1.get_PuntuacionP()), True, TextColor)
		P1Total_Label = font1.render(str(Player1.get_PuntuacionT()), True, TextColor)
		P1_Label = font1.render("P1", True, TextColor)
		VentanaJuego.blit(P1_Label,(7,10))
		VentanaJuego.blit(P1PuntosP_Label,(7,50))
		VentanaJuego.blit(P1Total_Label,(67,50))

		P2PuntosP_Label = font1.render(str(Player2.get_PuntuacionP()), True, TextColor)
		P2Total_Label = font1.render(str(Player2.get_PuntuacionT()), True, TextColor)
		P2_Label = font1.render("P2", True, TextColor)
		VentanaJuego.blit(P2_Label,(147,10))
		VentanaJuego.blit(P2PuntosP_Label,(147,50))
		VentanaJuego.blit(P2Total_Label,(207,50))


		if FinJuego[0]:
			if Player1.get_PuntuacionT()>Player2.get_PuntuacionT():
				VentanaJuego.blit(P1Win_Image,(100,115))
				Player_ImageWin=Player_Image
				Player_ImageWin = pygame.transform.scale(Player_ImageWin, (100, 150))
				VentanaJuego.blit(Player_ImageWin,(225,300))

			if Player2.get_PuntuacionT()>Player1.get_PuntuacionT():
				VentanaJuego.blit(P2Win_Image,(100,115))
				Player2_ImageWin=Player2_Image
				Player2_ImageWin = pygame.transform.scale(Player2_ImageWin, (100, 150))
				VentanaJuego.blit(Player2_ImageWin,(225,300))	
		

	
		pygame.time.wait(50)
		pygame.display.update()



def menu():
    Menu = pygame.display.set_mode([500,530]) # Play window with its dimensions     

    MainMenu_Image = pygame.image.load("ImagenesBat/MenupBAT.jpg").convert()
    
    while True:
    	
    	for event in pygame.event.get(): # It prevents the program from collapsing        
            if event.type == pygame.QUIT: # By pressing the "x" in the upper right corner
                pygame.quit() # Close the program
            if event.type == pygame.MOUSEBUTTONDOWN and event.button==1:
            	PositionMenu = pygame.mouse.get_pos()
            	if PositionMenu[0]>160 and PositionMenu[0]<332 and PositionMenu[1]>204 and PositionMenu[1]<274:
            		return main()
	        
                            
    	Menu.blit(MainMenu_Image,(0,0))
    	pygame.time.wait(50) # Waiting time in milliseconds for correct operation
    	pygame.display.update() # Constant updating of the screen        
menu()

"""if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
	        	if PositionMenu[0] > 160 and PositionMenu[0] < 332 and PositionMenu[1] > 204 and PositionMenu[1] < 274: # Over "New Game"
	                print ("ddd")"""