import pdb

class Afd:
	def __init__(self, delta, alfabeto, estadosFinales):
		self.delta = delta
		self.alfabeto = alfabeto
		self.inicio = 0
		self.estadosFinales = estadosFinales


	def aceptarCadena(self, cadena):
		terminos = self.buscarPatrones(cadena)

		return len(terminos) > 0 and (terminos.pop() + 1) == len(cadena)


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
				# if len(cadenaActual) >= 47:
					# pdb.set_trace()
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
		    print("El texto contiene simbolos no encontrado en el alfabeto: " + str(simbolosExternos))

		if soloUnTermino:
			return None

		return terminos