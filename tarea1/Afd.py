import pdb

class Afd:
	def __init__(self, delta, alfabeto, estadosFinales):
		self.delta = delta
		self.alfabeto = alfabeto
		self.inicio = 0
		self.estadosFinales = estadosFinales


	# aceptarCadena: self string -> boolean
	# retorna True si la cadena es aceptada por el automata.
	# Reutiliza la funcion buscarPatrones
	def aceptarCadena(self, cadena):
		terminos = self.buscarPatrones(cadena)

		return len(terminos) > 0 and (terminos.pop() + 1) == len(cadena)


	# buscarPatrones: self string Afd boolean -> list
	# retorna una lista con todas las posiciones en donde el afd detecto
	# una cadena aceptada. Si el parametro afdInvertido existe, entonces recursivamente
	# se busca una coincidencia en reversa a partir de un final encontrado. Si soloUnTermino
	# es True, la funcion retorna la primera coincidencia encontrada.
	def buscarPatrones(self, cadena, afdInvertido=None, soloUnTermino=False):
		estadoActual = self.inicio
		terminos = []
		cadenaActual = ''
		simbolosExternos = set()

		for idx, char in enumerate(cadena):
			cadenaActual += char
			if char not in self.alfabeto:
				simbolosExternos.update([char])

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

		if len(simbolosExternos) > 0:
		    print("Warning: El texto contiene simbolos no encontrado en el alfabeto: " + str(simbolosExternos) + "\n\n")

		if soloUnTermino:
			return None

		return terminos