from Lista import Lista

class Pila:
	def __init__(self):
		self.lista = Lista(None)
		self.size = 0

	def apilar(self, elem):
		self.lista = Lista(elem, self.lista)
		self.size += 1

	def desapilar(self):
		top = None

		if self.size > 0:
			top = self.lista.head
			self.lista = self.lista.cola
			self.size -= 1

		return top

	def estaVacia(self):
		return self.size == 0