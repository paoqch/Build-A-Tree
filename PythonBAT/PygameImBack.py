### LIBRARIES ###------------------------------------------------------------------------------------------------------
import pygame  # Load all Pygame functionalities
import sys     # Increase the capacity of recursion
import random  # To use of random options
import time    # To control execution times and waiting periods
import threading # For the implementation and control of the animation threads
sys.setrecursionlimit(10**9) # Increased recursion limit
from Player import Player

### MAIN FUNCTION OF THE GAME (GAMEPLAY) ###
pygame.init()

def main():
	VentanaJuego =  pygame.display.set_mode([600,630])
	Mapa_Image = pygame.image.load("ImagenesBat/MapaBAT.png").convert()
	FemSound = pygame.mixer.Sound("SonidosBAT/FemAtSoundBAT.wav")
	Player1 = Player()
	Player2 = Player()
	Player_Image = pygame.image.load(Player1.get_imagen())
	Player1.mostrar()	
	#pygame.key.set_repeat(1, 1000)
	while True:
		
		
		Tiempo = pygame.time.get_ticks()
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				pygame.quit()
			if event.type == pygame.KEYDOWN:
				
				if event.key == pygame.K_LEFT:
					Player1.MoverIzquierda()
					Player1.ActualizarSprite()
					print(Player1.get_PosY())
					Player_Image = pygame.image.load(Player1.get_imagen())
					if Player1.get_PosY()==352 and Player1.get_PosX()<190:
						Player1.set_PosY(460)
					#if Player1.get_PosY()==352 and Player1.get_PosX()<190:
						#Player1.set_PosY(460)
					if Player1.get_PosY()==213 and Player1.get_PosX()<195:
						Player1.set_PosY(283)
					#if Player1.get_PosY()==352 and Player1.get_PosX()<190:
						#Player1.set_PosY(460)
					if Player1.get_PosY()==43 and Player1.get_PosX()<130:
						Player1.set_PosY(129)								
				
				if event.key == pygame.K_RIGHT:					
					Player1.MoverDerecha()
					Player1.ActualizarSprite()
					Player_Image = pygame.image.load(Player1.get_imagen())
					#if Player1.get_PosY()==352 and Player1.get_PosX()>190:
						#Player1.set_PosY(460)
					if Player1.get_PosY()==283 and Player1.get_PosX()>210:
						Player1.set_PosY(352)
					if Player1.get_PosY()==213 and Player1.get_PosX()>430:
						Player1.set_PosY(352)
					#if Player1.get_PosY()==352 and Player1.get_PosX()<190:
						#Player1.set_PosY(460)
					if Player1.get_PosY()==43 and Player1.get_PosX()>417:
						Player1.set_PosY(129)		

				if event.key == pygame.K_x:
					Player1.Atacar()
					Player1.ActualizarSprite()
					Player_Image = pygame.image.load(Player1.get_imagen())
					FemSound.play()
					#Player_Sound = pygame.mixer.Sound("Sounds/StickSound.mp3") # Sound of the Cannibal's attack

				if event.key == pygame.K_UP:
					ActualY = Player1.get_PosY()
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
					else:
						Player1.set_PosY(ActualY)	

				if event.key == pygame.K_DOWN:
					if Player1.get_Cont()>=0:
						Player1.set_Cont(0)
					else:
						Player1.set_Cont(-1)
					Player1.ActualizarSprite()
					Player_Image = pygame.image.load(Player1.get_imagen())
					if Player1.get_PosY()==352:
						Player1.set_PosY(460)
					if Player1.get_PosY()==283:
						Player1.set_PosY(460)
					if Player1.get_PosY()==213:
						Player1.set_PosY(352)
					if Player1.get_PosY()==129:
						if Player1.get_PosX()>71 and Player1.get_PosX()<200: 
							Player1.set_PosY(283)
						else:
							Player1.set_PosY(213)	
					if Player1.get_PosY()==43:
						Player1.set_PosY(129)		


		#print(Player1.get_PosY())	
		VentanaJuego.blit(Mapa_Image,(0,0))
		VentanaJuego.blit(Player_Image,(Player1.get_PosX(),Player1.get_PosY()))

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