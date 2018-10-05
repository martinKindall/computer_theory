from Afnd import Afnd

import pdb

Afnd.tests()


def principal(accion, automata, afd1Inv):
	continuar = "s"
	while continuar == "s":
		cadena = input("Ingrese cadena: ")
		mensaje = accion(cadena, automata, afd1Inv)
		print(mensaje)
		continuar = input("Desea continuar? (s/n): ")


def buscarMaches(cadena, automata, afd1Inv):
		return automata.buscarPatrones(cadena, afd1Inv)

def buscarCadenas(cadena, automata, afd1Inv):
		return automata.aceptarCadena(cadena)

# regExp = "|..baba"
regExp = "|a..bab"
# regExp = "|ab"

# alfabeto = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 \n"
alfabeto = "ab"
afnd1 = Afnd.fromRegExpToAfnd(regExp, alfabeto, [])
afnd1Invertido = afnd1.invertir()
# afnd1.addLoopsTexto()
pdb.set_trace()
afd1Inv = afnd1Invertido.convertToAfd()
afd1 = afnd1.convertToAfd()

# principal(buscarMaches, afd1, afd1Inv)



# pdb.set_trace();True