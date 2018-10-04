
class Afd:
	def __init__(self, delta, alfabeto, estadosFinales):
		self.delta = delta
		self.inicio = 0
		self.estadosFinales = estadosFinales

	def aceptarCadena(self, cadena):
		estadoActual = self.inicio

		for char in cadena:
			if char in self.delta[estadoActual]:
				estadoActual = self.delta[estadoActual][char]

		return estadoActual in self.estadosFinales