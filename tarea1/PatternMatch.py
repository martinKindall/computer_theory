from Afnd import Afnd


class PatternMatch():
	
	@staticmethod
	def buscar(regEx, texto):
		alfabeto = "ab\n"

		afnd1 = Afnd.fromRegExpToAfnd(regEx, alfabeto, [])
		afnd1Invertido = afnd1.invertir()
		afnd1.addLoopsTexto()

		afd1 = afnd1.convertToAfd()
		afd1Inv = afnd1Invertido.convertToAfd()

		matches = afd1.buscarPatrones(texto, afd1Inv)
		substrs = []

		for match in matches:
			substrs.append(texto[match[0]:(match[1] + 1)])

		return (matches, substrs)


	def formatear(listaResultados):
		busquedas = []
		matches = listaResultados[0]
		substrs = listaResultados[1]

		for idx, _ in enumerate(matches):
			busquedas.append("["+str(matches[idx][0])+","+str(matches[idx][1])+"]: " + str(substrs[idx]))

		return busquedas


	def buscarYFormatear(regEx, texto):
		listaResultados = PatternMatch.buscar(regEx, texto)

		return PatternMatch.formatear(listaResultados)