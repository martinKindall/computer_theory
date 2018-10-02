class Afnd:
	def __init__(self, regExp):
		self.estados = []
		self.delta = []

		self.convertir(regExp)

	def convertir(self, regExp):
		

		
		self.estados.append(regExp)