class Nodo:
	def __init__(self, val, izq=None, der=None):
		self.izq = izq
		self.der = der
		self.val = val