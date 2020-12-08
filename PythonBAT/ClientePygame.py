### Bibliotecas ###================================================================================================================
import pygame  
import sys    
import random  
import time    
import threading # hilos
sys.setrecursionlimit(10**9) # aumentar limite de recursividad
from Player import Player # Clase Player
from Power import Power # Clase Power
from Token import Token # Clase Token
import socket # conexion
import threading # hilos

pygame.init()
### Funcion Main (toda la jugabilidad) ###===========================================================================================
def main():
	# Variables globales para la asignacion del orden de los challenges, segun la informacion(data) recibida del Servidor
	global data1 
	data1="1"
	global OrdenChallenges 
	global Primero
	global Segundo
	global Ultimo 
	global ChallengeActual
	### Funion que realiza la primera conexion con el Servidor, esto para recibir y asignar el orden de los challenges ###============
	def Conexion1(msg): # msg: es el mensaje desde el Cliente
		HOST = "localhost"  
		PORT = 5555 # puerto
		msg2 = msg # el mensaje que se enviara al servidor
		global s
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		    s.connect((HOST,PORT)) # conexion del socket
		    s.sendall((msg2.encode()))	
		    data1 = s.recv(1024)
		# El mensaje recibido se separa entre la parte del indicador de bytes con la posicion en memoria, y el mensage que se necesita   
		OrdenChallenges=str(data1).split("|")[1]
		global Primero
		Primero = OrdenChallenges.split(",")[0] # Al dividir el mensaje(,), el primer desafio por jugar
		global Segundo
		Segundo = OrdenChallenges.split(",")[1] # Segundo desafio por jugar
		global Ultimo
		Ultimo = OrdenChallenges.split(",")[2].split("'")[0] # Ultimo desafio por jugar
		print ("Recibido ",repr(data1))
		print("Primero: "+Primero+" Segundo: "+Segundo+" Ultimo: "+Ultimo)
		#print(str(data1.split(",")[0]))
			
	### Funion utilizada constantemente para enviar mensajes al servidor (funciona muy similar a Conexion1()), msg: es el mensaje ###======
	def Conexion(msg): # String que se envia como mensaje
		HOST = "localhost"
		PORT = 5555
		msg2 = msg
		global s
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		    s.connect((HOST,PORT))
		    s.sendall((msg2.encode())) # Codificacion del mensaje
		    data = s.recv(1024) 
		#print ("Recibido ",repr(data))	
	#--Imagenes, sonidos y fuentes generales------------------------------------------------------------------------------------
	VentanaJuego =  pygame.display.set_mode([600,630])
	Mapa_Image = pygame.image.load("ImagenesBat/MapaBAT.png").convert()
	ShieldIm = pygame.image.load("ImagenesBat/ShieldBAT.png")
	P1Win_Image = pygame.image.load("ImagenesBAT/P1WinBAT.jpg") 
	P2Win_Image = pygame.image.load("ImagenesBAT/P2WinBAT.jpg") 
	TokenObtenido = pygame.mixer.Sound("SonidosBAT/TokensSoundBAT.mp3")
	TokenIncorrecto = pygame.mixer.Sound("SonidosBAT/FalloSoundBAT.mp3")
	Soundtrack1 = pygame.mixer.Sound("SonidosBAT/OST1SoundBAT.mp3")
	Soundtrack2 = pygame.mixer.Sound("SonidosBAT/OST2SoundBAT.mp3")
	Soundtrack3 = pygame.mixer.Sound("SonidosBAT/OST3SoundBAT.mp3")
	PoderObtenido = pygame.mixer.Sound("SonidosBAT/EstrellaSoundBAT.mp3")
	font1 = pygame.font.SysFont("Britannic" , 30)
	TextColor = (74,48,111)
	# JUGADOR 1 # -------------------------------------------------------------------------------------------------------------
	Player1 = Player() # Se crea la instancia
	Conexion1("AVL/1/0") # Primera conexion
	Player_Image = pygame.image.load(Player1.get_imagen()) # Imagen del jugador
	P = pygame.image.load("ImagenesBAT/EstrellaBAT.png") # Su indicado de poder
	Player1.mostrar()
	Player1At = pygame.mixer.Sound(Player1.get_SonidoAtaque()) # Su sonido de ataque
	global IndicadorPoder # Su indicador de poder (poder conocer el poder poseido)
	IndicadorPoder = [False] 
	global ContadorPoder # Contador que afecta al indicador de poder
	ContadorPoder = 0


	# JUGADOR 2 # -------------------------------------------------------------------------------------------------------------
	Player2 = Player()
	Player2_Image = pygame.image.load(Player2.get_imagen())
	PP = pygame.image.load("ImagenesBAT/EstrellaBAT.png")
	Player2.mostrar()
	Player2At = pygame.mixer.Sound(Player2.get_SonidoAtaque())
	global IndicadorPoder2
	IndicadorPoder2 = [False]
	global ContadorPoder2
	ContadorPoder2 = 0

	# ----Variables globales para control de hilos y eventos en el juego--------------------------------------------------------

	ChallengeActual = Primero # se inicia con el primer challenge

	global Animation_Estrella # manejo de la activacion del hilo de la estrella de poderes
	Animation_Estrella = [True]
	global Animation_Tokens # manejo de la activacion del hilo de los tokens
	Animation_Tokens = [True]
	global Challenge_Image # imagen del challenge actual

	global FinChallenge # manejo para la finalizacion de un challenge
	FinChallenge = [False]
	global FinJuego # manejo para la finalizacion de la partida
	FinJuego = [False]
	global InicioOst # encargada de la activacion del primer soundtrack de fondo
	InicioOst = [False]
	global SiguienteOst # encargada de la activacion del segundo soundtrack de fondo
	SiguienteOst = [False]
	global UltimoOst # encargada de la activacion del tercero soundtrack de fondo
	UltimoOst = [False]
	global contChallenge # variables encargadas de llevar el control del Challenge actual
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

	### BUCLE DE JUEGO ###======================================================================================================
	while True: 
		Challenge_Image = pygame.image.load("ImagenesBAT/"+ChallengeActual+"BAT.png") # indicador en pantalla del challenge actual
		global PoderSaltoUsado # variable global que detecta si el jugador 1 ha usado el poder AirJump  
		PoderSaltoUsado = [True]

		global PoderSaltoUsado2
		PoderSaltoUsado2 = [True] # variable global que detecta si el jugador 2 ha usado el poder AirJump
		### Hilo que cntrola la animacion cuando el jugador 2 es atacado (efecto de retroceder)
		def Retroceder(P1,P2):# recibe la pocision x y y del jugador
			Player_Image2 = pygame.image.load(Player2.get_imagen())
			cont = 0 # contador que funciona como condicion de parada del bucle del hilo
			if Player1.get_PosX()<Player2.get_PosX(): # si se recibe el ataque desde la derecha
				Player2.RecibirAtaqueD()
				Player2.ActualizarSprite()
				Player_Image2 = pygame.image.load(Player2.get_imagen()) # imagen secundaria (copia de la imagen del jugador 2)
				while cont<81: # condicion de parada
					P1+=10 
					cont+=10
					VentanaJuego.blit(Player_Image2,(P1,P2)) # la imagen secundaria simula el efecto		
					pygame.time.wait(20)
			if Player1.get_PosX()>Player2.get_PosX(): # si se recibe el ataque desde la izquierda
				Player2.RecibirAtaqueI()
				Player2.ActualizarSprite()
				Player_Image2 = pygame.image.load(Player2.get_imagen()) # imagen secundaria (copia de la imagen del jugador 2)
				while cont<81: # condicion de parada
					P1-=10
					cont+=10
					VentanaJuego.blit(Player_Image2,(P1,P2))# la imagen secundaria simula el efecto		
					pygame.time.wait(20)
			if Player2.get_PosX()>515: # Si la posicion del jugador sobrepasa el suelo
				P1=515 # Se asignan posiciones de caida
				P2=Player2.get_PosY()
				Player2.set_PosY(531)
				Player2.set_PosX(-101)
				P3 = Player2.get_PosX()
				TCaida2 = threading.Thread(target = Caida2,args=(P1,P2,P3)) # activacion del hilo que simula la animacion del jugador cayendo
				TCaida2.start()
			if Player2.get_PosX()<25:
				P1=25# Se asignan posiciones de caida
				P2=Player2.get_PosY()
				Player2.set_PosY(530)
				Player2.set_PosX(-100)
				P3 = Player2.get_PosX()
				TCaida2 = threading.Thread(target = Caida2,args=(P1,P2,P3))
				TCaida2.start()					
		### Animacion de recibir un ataque pero para el jugador 1 (Funciona de la misma forma)
		def Retroceder2(P1,P2):# recibe la pocision x y y del jugador
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
		### Hilo que simula la animacion de subir, al utilizar el poder "AirJump" para el jugador 1 ### ==================================================
		def Subida(P1,P2): # recibe la pocision x y y del jugador
			Player_Image2 = pygame.image.load(Player1.get_imagen()) # imagen secundaria
			cont = P2
			while cont>129: # condicion de parada, cuando se haya recorrido la distancia hacia arriba necesaria
				P2-=10
				cont-=10
				VentanaJuego.blit(Player_Image2,(P1,P2)) # la imagen secundaria simula la animacion		
				pygame.time.wait(20)		
			if P1 == 25: 	
				Player1.set_PosY(129) # posicion a la que se llega cuando se utiliza el Airjump (cuarta plataforma)
				Player1.set_PosX(35)
			else:
				Player1.set_PosY(129) # posicion a la que se llega cuando se utiliza el Airjump (cuarta plataforma)
				Player1.set_PosX(505)
		### Hilo que simula la animacion de subir, al utilizar el poder "AirJump" para el jugador 2 ### ==================================================
		def Subida2(P1,P2):# recibe la pocision x y y del jugador
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
		### Hilo que simula la animacion de caida por el precipicio para el jugador 1 ### ==================================================
		def Caida(P1,P2,P3):# recibe un valor de posicion para la iniciacion de la animacion, asi como la pocision y y x del jugador
			Player_Image2 = pygame.image.load(Player1.get_imagen()) # imagen secundaria/auxiliar
			cont = P2
			while cont<630: # mientras que el jugador no haya caido por completo
				P2+=10 # baje (aumentando posicion y de la imagen auxiliar)
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
		### Hilo que simula la animacion de caida por el precipicio para el jugador 1 ### ===============================================
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
		# Contador de tiempo
		Tiempo = pygame.time.get_ticks()
		### EVENTOS ### =================================================================================================================
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				pygame.quit() # cerrar el juego
			if event.type == pygame.KEYDOWN: # al pulsar una tecla
				#===========================================IZQUIERDA==================================================	
				if event.key == pygame.K_LEFT: # Flecha izquierda para el jugador 1
					Player1.MoverIzquierda() # Mover a la izquierda implica un cambio en la imagen y las coordenadas del jugador
					Player1.ActualizarSprite()
					print(Player1.get_PosY())
					Player_Image = pygame.image.load(Player1.get_imagen())
					if Player1.get_PosY()==460 and Player1.get_PosX()<25: # Si desde el suelo, caminando hacia la izquierda el jugador se sale del suelo
						P1=25
						P2=Player1.get_PosY()
						Player1.set_PosY(530)
						Player1.set_PosX(-100)
						P3 = Player1.get_PosX()
						# Se activa el hilo de la animacion de caida
						TCaida = threading.Thread(target = Caida,args=(P1,P2,P3)) # se envian una variable de posicion predeterminada y las posiciones de jugador
						TCaida.start()


					if Player1.get_PosY()==352 and Player1.get_PosX()<190: # Al pasarse de esta plataforma el jugador cae en la siguiente
						Player1.set_PosY(460)
					
					if Player1.get_PosY()==283 and Player1.get_PosX()<25: # Si el jugador se pasa de esta plataforma, se cae al precipicio (hilo)
						P1=25
						P2=Player1.get_PosY()
						Player1.set_PosY(530)
						Player1.set_PosX(-100)
						P3 = Player1.get_PosX()
						# Se activa el hilo de la animacion de caida
						TCaida = threading.Thread(target = Caida,args=(P1,P2,P3))
						TCaida.start()

					if Player1.get_PosY()==213 and Player1.get_PosX()<195: # Al pasarse de esta plataforma el jugador cae en la siguiente
						Player1.set_PosY(283)
					
					if Player1.get_PosY()==129 and Player1.get_PosX()<25: # Si el jugador se pasa de esta plataforma, se cae al precipicio (hilo)
						P1=25
						P2=Player1.get_PosY()
						Player1.set_PosY(530)
						Player1.set_PosX(-100)
						P3 = Player1.get_PosX()
						# Se activa el hilo de la animacion de caida
						TCaida = threading.Thread(target = Caida,args=(P1,P2,P3))
						TCaida.start()
					
					if Player1.get_PosY()==43 and Player1.get_PosX()<130: # Al pasarse de esta plataforma el jugador cae en la siguiente
						Player1.set_PosY(129)


				# Movimiento hacia la izquierda Jugador 2 ------------------------------------------------------------------------------
				if event.key == pygame.K_a: # Letra a para el jugador 2
					Player2.MoverIzquierda()
					Player2.ActualizarSprite()
					print(Player2.get_PosY())
					Player2_Image = pygame.image.load(Player2.get_imagen())
					if Player2.get_PosY()==460 and Player2.get_PosX()<25:# Si desde el suelo, caminando hacia la izquierda el jugador se sale del suelo
						P1=25
						P2=Player2.get_PosY()
						Player2.set_PosY(530)
						Player2.set_PosX(-100)
						P3 = Player2.get_PosX()
						# Se activa el hilo de la animacion de caida
						TCaida2 = threading.Thread(target = Caida2,args=(P1,P2,P3))# se envian una variable de posicion predeterminada y las posiciones de jugador
						TCaida2.start()


					if Player2.get_PosY()==352 and Player2.get_PosX()<190:# Al pasarse de esta plataforma el jugador cae en la siguiente
						Player2.set_PosY(460)
					
					if Player2.get_PosY()==283 and Player2.get_PosX()<25:
						P1=25
						P2=Player2.get_PosY()
						Player2.set_PosY(530)
						Player2.set_PosX(-100)
						P3 = Player2.get_PosX()
						# Se activa el hilo de la animacion de caida
						TCaida2 = threading.Thread(target = Caida2,args=(P1,P2,P3))
						TCaida2.start()

					if Player2.get_PosY()==213 and Player2.get_PosX()<195:# Al pasarse de esta plataforma el jugador cae en la siguiente
						Player2.set_PosY(283)
					
					if Player2.get_PosY()==129 and Player2.get_PosX()<25:
						P1=25
						P2=Player2.get_PosY()
						Player2.set_PosY(530)
						Player2.set_PosX(-100)
						P3 = Player2.get_PosX()
						# Se activa el hilo de la animacion de caida
						TCaida2 = threading.Thread(target = Caida2,args=(P1,P2,P3))
						TCaida2.start()
					
					if Player2.get_PosY()==43 and Player2.get_PosX()<130:# Al pasarse de esta plataforma el jugador cae en la siguiente
						Player2.set_PosY(129)										
                #================================================DERECHA================================================				
				if event.key == pygame.K_RIGHT: # Flecha derecha para el jugador 1
					ActualX = Player1.get_PosX() # Mover a la derecha implica un cambio en la imagen y las coordenadas del jugador					
					Player1.MoverDerecha()
					Player1.ActualizarSprite()
					Player_Image = pygame.image.load(Player1.get_imagen())
					if Player1.get_PosY()==460 and Player1.get_PosX()>515:# Si el jugador se pasa de esta plataforma, se cae al precipicio (hilo)
						P1=515
						P2=Player1.get_PosY()
						Player1.set_PosY(531)
						Player1.set_PosX(-101)
						P3 = Player1.get_PosX()
						# Se activa el hilo de la animacion de caida
						TCaida = threading.Thread(target = Caida,args=(P1,P2,P3))
						TCaida.start()
					
					if Player1.get_PosY()==352 and Player1.get_PosX()>515:# Si el jugador se pasa de esta plataforma, se cae al precipicio (hilo)
						P1=515
						P2=Player1.get_PosY()
						Player1.set_PosY(531)
						Player1.set_PosX(-101)
						P3 = Player1.get_PosX()
						# Se activa el hilo de la animacion de caida
						TCaida = threading.Thread(target = Caida,args=(P1,P2,P3))# Si el jugador se pasa de esta plataforma, se cae al precipicio (hilo)
						TCaida.start()

					if Player1.get_PosY()==283 and Player1.get_PosX()>210:# Al pasarse de esta plataforma el jugador cae en la siguiente
						Player1.set_PosY(352)
					if Player1.get_PosY()==213 and Player1.get_PosX()>430:# Al pasarse de esta plataforma el jugador cae en la siguiente
						Player1.set_PosY(352)
					
					if Player1.get_PosY()==129 and Player1.get_PosX()>515:# Si el jugador se pasa de esta plataforma, se cae al precipicio (hilo)
						P1=515
						P2=Player1.get_PosY()
						Player1.set_PosY(531)
						Player1.set_PosX(-101)
						P3 = Player1.get_PosX()
						# Se activa el hilo de la animacion de caida
						TCaida = threading.Thread(target = Caida,args=(P1,P2,P3))
						TCaida.start()

					if Player1.get_PosY()==43 and Player1.get_PosX()>417:# Al pasarse de esta plataforma el jugador cae en la siguiente
						Player1.set_PosY(129)		
					if Player1.get_PosY()==530:
						Player1.set_PosX(ActualX)



				if event.key == pygame.K_d: # Letra d para el jugador 2
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
						# Se activa el hilo de la animacion de caida
						TCaida2 = threading.Thread(target = Caida2,args=(P1,P2,P3))
						TCaida2.start()
					
					if Player2.get_PosY()==352 and Player2.get_PosX()>515:
						P1=515
						P2=Player2.get_PosY()
						Player2.set_PosY(531)
						Player2.set_PosX(-101)
						P3 = Player2.get_PosX()
						# Se activa el hilo de la animacion de caida
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
						# Se activa el hilo de la animacion de caida
						TCaida2 = threading.Thread(target = Caida2,args=(P1,P2,P3))
						TCaida2.start()

					if Player2.get_PosY()==43 and Player2.get_PosX()>417:
						Player2.set_PosY(129)		
					if Player2.get_PosY()==530:
						Player2.set_PosX(ActualX)
						
				#==============================================ATAQUE===================================================	
				if event.key == pygame.K_RSHIFT: # Tecla shift para el jugador 1
					if ContadorPoder == 2: # Si el contador de poder indica que el jugador tiene el poder ForcePush
						Player1.Atacar() # Se cambia a la imagen de ataque
						Player1.ActualizarSprite()
						Player_Image = pygame.image.load(Player1.get_imagen())
						ContadorPoder = 0
						Player1At.play()
						if Player1.get_Cont()>=0: #Se detecta la posicion del jugador con respecto al openente que recibe el ataque
							if Player2.get_Cont()>=0:
								if Player1.get_PosY()==Player2.get_PosY() and Player1.get_PosX()<Player2.get_PosX()+45 and Player1.get_PosX()>Player2.get_PosX()-85: 
									if ContadorPoder2==3:
										ContadorPoder2=0
									else:	
										P1=Player2.get_PosX() # Se envian las coordenadas del atacado al hilo de Retroceder
										P2=Player2.get_PosY()
										Thread_Retro = threading.Thread(target = Retroceder, args = (P1,P2)) # Se activa el hilo que comienza la animacion de recibir ataque
										Thread_Retro.start()
							if Player2.get_Cont()<=-1:
								if Player1.get_PosY()==Player2.get_PosY() and Player1.get_PosX()<Player2.get_PosX()+45 and Player1.get_PosX()>Player2.get_PosX()-85: 
									if ContadorPoder2==3:
										ContadorPoder2=0
									else:	
										P1=Player1.get_PosX()# Se envian las coordenadas del atacado al hilo de Retroceder
										P2=Player1.get_PosY()
										Thread_Retro2 = threading.Thread(target = Retroceder, args = (P1,P2))# Se activa el hilo que comienza la animacion de recibir ataque
										Thread_Retro2.start()		
						if Player1.get_Cont()<=-1:
							if Player2.get_Cont()<=-1:
								if Player1.get_PosY()==Player2.get_PosY() and Player1.get_PosX()>Player2.get_PosX()-45 and Player1.get_PosX()<Player2.get_PosX()+85: 
									if ContadorPoder2==3:
										ContadorPoder2=0
									else:	
										P1=Player2.get_PosX()# Se envian las coordenadas del atacado al hilo de Retroceder
										P2=Player2.get_PosY()
										Thread_Retro = threading.Thread(target = Retroceder, args = (P1,P2))# Se activa el hilo que comienza la animacion de recibir ataque
										Thread_Retro.start()
							if Player2.get_Cont()>=0:
								if Player1.get_PosY()==Player2.get_PosY() and Player1.get_PosX()>Player2.get_PosX()-85 and Player1.get_PosX()>Player2.get_PosX()+45:
									if ContadorPoder2==3:
										ContadorPoder2=0
									else:
										P1=Player2.get_PosX()# Se envian las coordenadas del atacado al hilo de Retroceder
										P2=Player2.get_PosY()
										Thread_Retro2 = threading.Thread(target = Retroceder, args = (P1,P2))# Se activa el hilo que comienza la animacion de recibir ataque
										Thread_Retro2.start()
				
				if event.key == pygame.K_f: # Tecla f para el jugador 2
					if ContadorPoder2 == 2: # Si el contador de poder indica que el jugador 2 tiene el poder ForcePush
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
										Thread_Retro3 = threading.Thread(target = Retroceder2, args = (P1,P2))# Se activa el hilo que comienza la animacion de recibir ataque
										Thread_Retro3.start()
							if Player1.get_Cont()<=-1:
								if Player2.get_PosY()==Player1.get_PosY() and Player2.get_PosX()<Player1.get_PosX()+45 and Player2.get_PosX()>Player1.get_PosX()-85: 
									if ContadorPoder==3:
										ContadorPoder=0
									else:	
										P1=Player1.get_PosX()
										P2=Player1.get_PosY()
										Thread_Retro4 = threading.Thread(target = Retroceder2, args = (P1,P2))# Se activa el hilo que comienza la animacion de recibir ataque
										Thread_Retro4.start()		
						if Player2.get_Cont()<=-1:
							if Player1.get_Cont()<=-1:
								if Player2.get_PosY()==Player1.get_PosY() and Player2.get_PosX()>Player1.get_PosX()-45 and Player2.get_PosX()<Player1.get_PosX()+85: 
									if ContadorPoder==3:
										ContadorPoder=0
									else:	
										P1=Player1.get_PosX()
										P2=Player1.get_PosY()
										Thread_Retro3 = threading.Thread(target = Retroceder2, args = (P1,P2))# Se activa el hilo que comienza la animacion de recibir ataque
										Thread_Retro3.start()
							if Player1.get_Cont()>=0:
								if Player2.get_PosY()==Player1.get_PosY() and Player2.get_PosX()>Player1.get_PosX()-85 and Player2.get_PosX()>Player1.get_PosX()+45:
									if ContadorPoder==3:
										ContadorPoder=0
									else:
										P1=Player1.get_PosX()
										P2=Player1.get_PosY()
										Thread_Retro4 = threading.Thread(target = Retroceder2, args = (P1,P2))# Se activa el hilo que comienza la animacion de recibir ataque
										Thread_Retro4.start()

            	#==============================================ARRIBA===================================================	
				if event.key == pygame.K_UP: # En el jugador 1, al pulsar la flecha de arriba
					ActualX = Player1.get_PosX() # Se crean dos variables que registran la posicion de salto del jugador
					ActualY = Player1.get_PosY()
					print(ActualY)
					Player1.Saltar() # Metodo que cambia la posicion del jugador, como si hubiese realizado un leve salto
					Player1.ActualizarSprite()
					Player_Image = pygame.image.load(Player1.get_imagen())
					if Player1.get_PosY()>340 and Player1.get_PosY()<400 and Player1.get_PosX()>180 and Player1.get_PosX()<470: # Si jugador salta dentro de el rango de la plataforma superior
						Player1.set_PosY(352) # El jugador sube de plataforma
						print(Player1.get_PosY())
					elif Player1.get_PosY()>264 and Player1.get_PosY()<299 and Player1.get_PosX()>56 and Player1.get_PosX()<210:# Si jugador salta dentro de el rango de la plataforma superior
						Player1.set_PosY(283) # El jugador sube de plataforma
						print(Player1.get_PosY())
					elif Player1.get_PosY()>194 and Player1.get_PosY()<230 and Player1.get_PosX()>185 and Player1.get_PosX()<430:# Si jugador salta dentro de el rango de la plataforma superior
						Player1.set_PosY(213) # El jugador sube de plataforma
						print(Player1.get_PosY())
					elif Player1.get_PosY()>110 and Player1.get_PosY()<145 and Player1.get_PosX()>190 and Player1.get_PosX()<500:# Si jugador salta dentro de el rango de la plataforma superior
						Player1.set_PosY(129) # El jugador sube de plataforma
						print(Player1.get_PosY())
					elif Player1.get_PosY()>25 and Player1.get_PosY()<60 and Player1.get_PosX()>140 and Player1.get_PosX()<460:# Si jugador salta dentro de el rango de la plataforma superior
						Player1.set_PosY(43) # El jugador sube de plataforma
						print(Player1.get_PosY())
					elif ActualX ==-100 and ContadorPoder==1: # Si el jugador se mueve hacia arriba mientras tiene el poder AirJump y si posicion registrada corresponde a la posicion de caida (se encuentra cayendo)
						P1=25
						P2=Player1.get_PosY()
						Player1.set_Cont(4)
						Player1.ActualizarSprite()
						PoderSaltoUsado[0] = False
						Player_Image = pygame.image.load(Player1.get_imagen())
						Ts = threading.Thread(target = Subida,args=(P1,P2)) # Se activa el poder, activando el hilo de subida, el cual recibe como parametros la posicion del jugador
						Ts.start()
						ContadorPoder=0
					elif ActualX ==-101 and ContadorPoder==1: # Si el jugador se mueve hacia arriba mientras tiene el poder AirJump y si posicion registrada corresponde a la posicion de caida (se encuentra cayendo)
						P1=515
						P2=Player1.get_PosY()
						Player1.set_Cont(-5)
						Player1.ActualizarSprite()
						PoderSaltoUsado[0] = False
						Player_Image = pygame.image.load(Player1.get_imagen())
						Ts = threading.Thread(target = Subida,args=(P1,P2)) #Se activa el poder, activando el hilo de subida, el cual recibe como parametros la posicion del jugador
						Ts.start()
						ContadorPoder=0
					else:
						Player1.set_PosY(ActualY) # El jugador no puede utilizar la tecla hacia arriba
						Player1.set_PosX(ActualX)



				if event.key == pygame.K_w:  # En el jugador 2, al pulsar la tecla w
					ActualX = Player2.get_PosX()
					ActualY = Player2.get_PosY()
					print(ActualY)
					Player2.Saltar()
					Player2.ActualizarSprite()
					Player2_Image = pygame.image.load(Player2.get_imagen())
					if Player2.get_PosY()>340 and Player2.get_PosY()<400 and Player2.get_PosX()>180 and Player2.get_PosX()<470: # Subida del jugador 2 a plataformas superiores
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
					elif ActualX ==-100 and ContadorPoder2==1:# Si el jugador 2 se mueve hacia arriba mientras tiene el poder AirJump y si posicion registrada corresponde a la posicion de caida (se encuentra cayendo)
						P1=25
						P2=Player2.get_PosY()
						Player2.set_Cont(4)
						Player2.ActualizarSprite()
						PoderSaltoUsado2[0] = False
						Player2_Image = pygame.image.load(Player2.get_imagen())
						Ts2 = threading.Thread(target = Subida2,args=(P1,P2))# Se activa el poder, activando el hilo de subida, el cual recibe como parametros la posicion del jugador 2
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
				
				#===================================================ABAJO=========================================================	
				if event.key == pygame.K_DOWN: # En el jugador 1, al pulsar la flecha de abajo
					if Player1.get_Cont()>=0:
						Player1.set_Cont(0)
					else:
						Player1.set_Cont(-1)
					Player1.ActualizarSprite()
					Player_Image = pygame.image.load(Player1.get_imagen())
					if Player1.get_PosY()==352: # Si el jugador tiene una plataforma directamente por debajo 
						Player1.set_PosY(460) # Su pocision cambia a la plataforma inferior
					if Player1.get_PosY()==129:
						if Player1.get_PosX()>49 and Player1.get_PosX()<200:# Si el jugador tiene una plataforma directamente por debajo  
							Player1.set_PosY(Player1.get_PosY())
						else:
							Player1.set_PosY(213)# Su pocision cambia a la plataforma inferior	
					if Player1.get_PosY()==43:
						Player1.set_PosY(129)# Su pocision cambia a la plataforma inferior

				

				if event.key == pygame.K_s: # En el jugador 2, al pulsar la tecla s
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

			# ===============ESTRELLA. Hilo que controla la animacion de las estrellas=====================================================================================================
		def Estrella(): 
			Estrella_x=random.randint(35,505)
			Estrella_y=-100
			Estrella_PassedTime=pygame.time.get_ticks() # Tiempo para el reinicio de la animacion
			Estrella_ActualTime=0
			while True:
				Estrella_y+=6 # La estrella cae
				pygame.time.wait(20)
				Estrella_ActualTime = pygame.time.get_ticks()
				if (Estrella_ActualTime - Estrella_PassedTime)//1000>=6: # Si la diferencia de tiempos es de 6 segundos
					Estrella_PassedTime = pygame.time.get_ticks() # Reinicia el tiempo y la animacion
					Animation_Estrella[0] = True
					break
				if Estrella_y>Player1.get_PosY() and Estrella_y < Player1.get_PosY() + 90 and Estrella_x > Player1.get_PosX() and Estrella_x < Player1.get_PosX()+55:	
					PoderObtenido.play() # Si el jugador 1 colisiona con la estrella
					Estrella_x=-111
					IndicadorPoder[0]=True # Obtiene un poder
				if Estrella_y>Player1.get_PosY() and Estrella_y < Player1.get_PosY() + 90 and Estrella_x < Player1.get_PosX() and Estrella_x > Player1.get_PosX()-55:	
					PoderObtenido.play() # Si el jugador 1 colisiona con la estrella
					Estrella_x=-111
					IndicadorPoder[0]=True # Obtiene un poder
				if Estrella_y>Player2.get_PosY() and Estrella_y < Player2.get_PosY() + 95 and Estrella_x > Player2.get_PosX() and Estrella_x < Player2.get_PosX()+55:	
					PoderObtenido.play() # Si el jugador 2 colisiona con la estrella
					Estrella_x=-111
					IndicadorPoder2[0]=True # Obtiene un poder
				if Estrella_y>Player2.get_PosY() and Estrella_y < Player2.get_PosY() + 95 and Estrella_x < Player2.get_PosX() and Estrella_x > Player2.get_PosX()-55:	
					PoderObtenido.play() # Si el jugador 2 colisiona con la estrella
					Estrella_x=-111
					IndicadorPoder2[0]=True	# Obtiene un poder	

				Star = pygame.image.load("ImagenesBAT/EstrellaBAT.png")
				VentanaJuego.blit(Star,(Estrella_x,Estrella_y))
		### TOKENS Hilo que controla la animacion de los tokens #==========================================================================================
		def Tokens():
			Token_x=random.randint(35,505) # Coordenadas X aleatorias de aparicion
			Token_y=-100 
			Token_PassedTime=pygame.time.get_ticks() # Tiempo para el reinicio de la animacion
			Token_ActualTime=0
			Token0 = Token() # Se crea una instancia Token 
			while True:
				Token_y+=6 # El Token cae
				pygame.time.wait(20)
				Token_ActualTime = pygame.time.get_ticks()
				if (Token_ActualTime - Token_PassedTime)//1000>=4: # Si la diferencia de tiempos es de 4 segundos
					Token_PassedTime = pygame.time.get_ticks() # Reinicia el tiempo y la animacion
					Animation_Tokens[0] = True
					break
				if Token_y>Player1.get_PosY() and Token_y < Player1.get_PosY() + 90 and Token_x > Player1.get_PosX() and Token_x < Player1.get_PosX()+55:	
					Token_x=-111 # Si el jugador 1 colisiona con la estrella
					print(Token0.get_Figura()+" "+str(Token0.get_Valor()))
					if Token0.get_Arbol()==ChallengeActual: # Si el token es el objetivo del challenge actual
						TokenObtenido.play()
						Player1.AumentoPuntos()
						Conexion(Token0.get_Arbol()+"/1/"+str(Token0.get_Valor())) # Envia el mensaje con el tipo de arbol, el numero del jugador y el valor del token tomado, respectivamente
					else:# Si el token es incorrecto
						TokenIncorrecto.play()
						Player1.ReinicioPuntos() # Se reinician sus puntos parciales, pierde su arbol
						Conexion(Token0.get_Arbol()+"/1/0") # Envia un mensaje indicando el reinicio del arbol
					Token_PassedTime = pygame.time.get_ticks()

				elif Token_y>Player1.get_PosY() and Token_y < Player1.get_PosY() + 90 and Token_x < Player1.get_PosX() and Token_x > Player1.get_PosX()-55:	
					Token_x=-111 # Si el jugador 1 colisiona con la estrella
					print(Token0.get_Figura()+" "+str(Token0.get_Valor()))
					if Token0.get_Arbol()==ChallengeActual: # Si el token es el objetivo del challenge actual
						TokenObtenido.play()
						Player1.AumentoPuntos() # Aumenta la puntuacion parcial
						Conexion(Token0.get_Arbol()+"/1/"+str(Token0.get_Valor()))# Envia el mensaje con el tipo de arbol, el numero del jugador y el valor del token tomado, respectivamente
					else:# Si el token es incorrecto
						TokenIncorrecto.play()
						Player1.ReinicioPuntos() # Se reinician sus puntos parciales, pierde su arbol
						Conexion(Token0.get_Arbol()+"/1/0") # Envia un mensaje indicando el reinicio del arbol
					Token_PassedTime = pygame.time.get_ticks()

				elif Token_y>Player2.get_PosY() and Token_y < Player2.get_PosY() + 95 and Token_x > Player2.get_PosX() and Token_x < Player2.get_PosX()+55:	
					Token_x=-111 # Si el jugador 2 colisiona con la estrella
					print(Token0.get_Figura()+" "+str(Token0.get_Valor()))
					if Token0.get_Arbol()==ChallengeActual: # Si el token es el objetivo del challenge actual
						TokenObtenido.play()
						Player2.AumentoPuntos() # Aumenta la puntuacion parcial
						Conexion(Token0.get_Arbol()+"/2/"+str(Token0.get_Valor()))# Envia el mensaje con el tipo de arbol, el numero del jugador y el valor del token tomado, respectivamente
					else:# Si el token es incorrecto
						TokenIncorrecto.play()
						Player2.ReinicioPuntos() # Se reinician sus puntos parciales, pierde su arbol
						Conexion(Token0.get_Arbol()+"/2/0") # Envia un mensaje indicando el reinicio del arbol
					Token_PassedTime = pygame.time.get_ticks()

				elif Token_y>Player2.get_PosY() and Token_y < Player2.get_PosY() + 95 and Token_x < Player2.get_PosX() and Token_x > Player2.get_PosX()-55:	
					Token_x=-111 # Si el jugador 2 colisiona con la estrella
					print(Token0.get_Figura()+" "+str(Token0.get_Valor()))
					if Token0.get_Arbol()==ChallengeActual: # Si el token es el objetivo del challenge actual
						TokenObtenido.play()
						Player2.AumentoPuntos() # Aumenta la puntuacion parcial
						Conexion(Token0.get_Arbol()+"/2/"+str(Token0.get_Valor()))# Envia el mensaje con el tipo de arbol, el numero del jugador y el valor del token tomado, respectivamente
					else: # Si el token es incorrecto
						TokenIncorrecto.play() # Se reinician sus puntos parciales, pierde su arbol
						Player2.ReinicioPuntos() # Aumenta la puntuacion parcial
						Conexion(Token0.get_Arbol()+"/2/0") # Envia un mensaje indicando el reinicio del arbol
					Token_PassedTime = pygame.time.get_ticks()
				
				Token_Image = pygame.image.load(Token0.get_imagen())
				Token_Image = pygame.transform.scale(Token_Image, (40, 40))
				VentanaJuego.blit(Token_Image,(Token_x,Token_y))		
		# Poder para el jugador 1 #-----------------------------------------------------------------------------------------------
		if ContadorPoder==0: 
			P = pygame.image.load("ImagenesBAT/EmptyBAT.png") # No hay un poder actual
		if IndicadorPoder[0]: # Al tomar un poder
			PoderActual = Power() # Se instancia un poder para el jugador 1
			P = pygame.image.load(PoderActual.get_imagen())
			if PoderActual.get_Nombre()=="AirJump":
				ContadorPoder = 1 # AirJump
			elif PoderActual.get_Nombre()=="ForcePush":
				ContadorPoder = 2 # ForcePush
			else:
				ContadorPoder = 3 # Shield
			IndicadorPoder[0]=False
		# Poder para el jugador 2 #-----------------------------------------------------------------------------------------------
		if ContadorPoder2==0: # No hay un poder actual
			PP = pygame.image.load("ImagenesBAT/EmptyBAT.png")
		if IndicadorPoder2[0]:
			PoderActual2 = Power() # Se instancia un poder para el jugador 2
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
		### CONTROL DE TIEMPOS, TRANSICIONES Y FIN DEL JUEGO ### ========================================================================
		if Tiempo>80000: # 80 s
			contChallenge+=1
			ChallengeActual=Segundo # Se pasa al siguiente challenge
			if contChallenge==1:
				FinChallenge[0]=True

		if Tiempo>160000: # 160 s
			contChallenge2+=1
			ChallengeActual=Ultimo # Se pasa al siguiente challenge
			if contChallenge2==1:
				FinChallenge[0]=True

		if Tiempo>240000: # 240 s
			contChallenge3+=1
			if contChallenge3==1:
				FinJuego[0]=True # Se Termina la partida		

		if FinChallenge[0]: # Al final de cada challenge
			Player1.AumentoaTotal(Player1.get_PuntuacionP()) # La puntuacion parcial del jugador 1 se suma a su total  
			Player1.ReinicioPuntos() # Se reinicia su puntuacion
			Player2.AumentoaTotal(Player2.get_PuntuacionP()) # La puntuacion parcial del jugador 2 se suma a su total 
			Player2.ReinicioPuntos() # Se reinicia su puntuacion
			print("Parcial: "+str(Player1.get_PuntuacionP())+" Total: "+str(Player1.get_PuntuacionT()))
			print("Parcial: "+str(Player2.get_PuntuacionP())+" Total: "+str(Player2.get_PuntuacionT()))
			FinChallenge[0]=False

		if InicioOst[0]: #Activa primer sonido de fondo
			Soundtrack1.play() 
		if SiguienteOst[0]:#Activa Segundo sonido de fondo
			Soundtrack2.play()
		if UltimoOst[0]:#Activa tercer sonido de fondo
			Soundtrack3.play()		

					
		if Animation_Estrella[0]: # Activa el hilo de la estrella
			Thread_Estrella = threading.Thread(target = Estrella, args = ())
			Thread_Estrella.start()
			Animation_Estrella[0]=False

		if Animation_Tokens[0]: # Activa el hilo de los tokens
			Thread_Token = threading.Thread(target = Tokens, args = ())
			Thread_Token.start()
			Animation_Tokens[0]=False

		if Player1.get_PosY()>=630: # Si el jugador 1 cae completamente al precipicio
			Player1.set_PosY(43) # Reaparece
			Player1.set_Cont(0)
			Conexion(ChallengeActual+"/1/0")
			Player1.ActualizarSprite()
			Player1.set_PosX(random.randint(160,440))
			pygame.time.delay(1000)

		if Player2.get_PosY()>=630: # Si el jugador 2 cae completamente al precipicio
			Player2.set_PosY(43) # Reaparece
			Player2.set_Cont(0)
			Conexion(ChallengeActual+"/2/0")
			Player2.ActualizarSprite()
			Player2.set_PosX(random.randint(160,440))
			pygame.time.delay(1000)	


		VentanaJuego.blit(Mapa_Image,(0,0)) # imagen fondo
		VentanaJuego.blit(Player_Image,(Player1.get_PosX(),Player1.get_PosY())) # imagen jugador 1

		VentanaJuego.blit(Player2_Image,(Player2.get_PosX(),Player2.get_PosY())) # imagen jugador 2
		
		if ContadorPoder == 3: # Si se obtiene el poder Shield
			Escudo = pygame.image.load("ImagenesBAT/Shield0BAT.png") # La imagen de un escudo se mostrara alrededor del jugador 1
			VentanaJuego.blit(Escudo,(Player1.get_PosX()-15,Player1.get_PosY()))

		if ContadorPoder2 == 3: # Si se obtiene el poder Shield
			Escudo2 = pygame.image.load("ImagenesBAT/Shield0BAT.png") # La imagen de un escudo se mostrara alrededor del jugador 2
			VentanaJuego.blit(Escudo2,(Player2.get_PosX()-15,Player2.get_PosY()))	
		VentanaJuego.blit(Challenge_Image,(470,0))
		VentanaJuego.blit(P,(60,2)) # Icono del poder actual del jugador 1
		VentanaJuego.blit(PP,(200,2)) # Icono del poder actual del jugador 2
		### LABELS Y TEXTO EN PANTALLA###==========================================================================================
		P1PuntosP_Label = font1.render(str(Player1.get_PuntuacionP()), True, TextColor) # Puntos parciales del jugador 1
		P1Total_Label = font1.render(str(Player1.get_PuntuacionT()), True, TextColor) # Puntuacion Total del jugador 1
		P1_Label = font1.render("P1", True, TextColor)
		VentanaJuego.blit(P1_Label,(7,10))
		VentanaJuego.blit(P1PuntosP_Label,(7,50))
		VentanaJuego.blit(P1Total_Label,(67,50))

		P2PuntosP_Label = font1.render(str(Player2.get_PuntuacionP()), True, TextColor) # Puntos parciales del jugador 2
		P2Total_Label = font1.render(str(Player2.get_PuntuacionT()), True, TextColor) # Puntuacion Total del jugador 2
		P2_Label = font1.render("P2", True, TextColor)
		VentanaJuego.blit(P2_Label,(147,10))
		VentanaJuego.blit(P2PuntosP_Label,(147,50))
		VentanaJuego.blit(P2Total_Label,(207,50))

		### GAME OVER ### =========================================================================================================
		if FinJuego[0]: # Si el ultimo challenge ya se ha jugado
			if Player1.get_PuntuacionT()>Player2.get_PuntuacionT(): # Si el jugador 1 tiene una mayor puntuacion Total
				VentanaJuego.blit(P1Win_Image,(100,115))
				Player_ImageWin=Player_Image
				Player_ImageWin = pygame.transform.scale(Player_ImageWin, (100, 150)) #Se muestra como ganador
				VentanaJuego.blit(Player_ImageWin,(225,300))

			if Player2.get_PuntuacionT()>Player1.get_PuntuacionT(): # Si el jugador 2 tiene una mayor puntuacion Total
				VentanaJuego.blit(P2Win_Image,(100,115))
				Player2_ImageWin=Player2_Image
				Player2_ImageWin = pygame.transform.scale(Player2_ImageWin, (100, 150)) #Se muestra como ganador
				VentanaJuego.blit(Player2_ImageWin,(225,300))	
		

	
		pygame.time.wait(50)
		pygame.display.update()


### MENU ### ===================================================================================================================
def menu():
    Menu = pygame.display.set_mode([500,530]) # Play window with its dimensions     

    MainMenu_Image = pygame.image.load("ImagenesBat/MenupBAT.jpg").convert()
    
    while True:
    	
    	for event in pygame.event.get():         
            if event.type == pygame.QUIT: 
                pygame.quit() # Cerrar
            if event.type == pygame.MOUSEBUTTONDOWN and event.button==1:
            	PositionMenu = pygame.mouse.get_pos()
            	if PositionMenu[0]>160 and PositionMenu[0]<332 and PositionMenu[1]>204 and PositionMenu[1]<274: # Si se pulsa el boton Play
            		return main()
	        
                            
    	Menu.blit(MainMenu_Image,(0,0))
    	pygame.time.wait(50) # Tiempo en milisegundos para una mejor funcionalidad
    	pygame.display.update() # Actualizar constantemente la pantalla        
menu()

"""if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
	        	if PositionMenu[0] > 160 and PositionMenu[0] < 332 and PositionMenu[1] > 204 and PositionMenu[1] < 274: # Over "New Game"
	                print ("ddd")"""