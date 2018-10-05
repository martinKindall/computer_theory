
class Afd:
	def __init__(self, delta, alfabeto, estadosFinales):
		self.delta = delta
		self.inicio = 0
		self.estadosFinales = estadosFinales


	def aceptarCadena(self, cadena):
		terminos = self.buscarPatrones(cadena)

		return len(terminos) > 0 and (terminos.pop() + 1) == len(cadena)


	def buscarPatrones(self, cadena):
		estadoActual = self.inicio
		terminos = []

		for idx, char in enumerate(cadena):
			if char in self.delta[estadoActual]:
				estadoActual = self.delta[estadoActual][char]

				if estadoActual in self.estadosFinales:
					terminos.append(idx)

		return terminos