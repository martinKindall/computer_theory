import pdb

class Afd:
	def __init__(self, delta, alfabeto, estadosFinales):
		self.delta = delta
		self.inicio = 0
		self.estadosFinales = estadosFinales


	def aceptarCadena(self, cadena):
		terminos = self.buscarPatrones(cadena)

		return len(terminos) > 0 and (terminos.pop() + 1) == len(cadena)


	def buscarPatrones(self, cadena, afdInvertido=None, soloUnTermino=False):
		estadoActual = self.inicio
		terminos = []
		cadenaActual = ''

		for idx, char in enumerate(cadena):
			cadenaActual += char
			if char in self.delta[estadoActual]:
				estadoActual = self.delta[estadoActual][char]

				if estadoActual in self.estadosFinales:
					terminos.append(idx)
					if soloUnTermino:
						return idx

					if not (afdInvertido is None):
						end = terminos.pop()
						start = afdInvertido.buscarPatrones(cadenaActual[::-1], soloUnTermino=True)

						if start is not None:
							terminos.append((idx-start, end))

		if soloUnTermino:
			return None

		return terminos