import random

class Token:
	def __init__(self,figura):
		self.figura = figura
		if self.figura == "circulo":
			self.valor = random.choice([1,2,3,4,5])
		elif self.figura == "rombo":
			self.valor = random.choice([6,7,8,9,0])	
		self.imagen = figura+str(self.valor)

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

Token0 = Token("circulo")
print(Token1.get_Figura())
print(Token1.get_Valor()) 	
print(Token1.get_imagen())	

	