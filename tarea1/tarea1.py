from Afnd import Afnd

import pdb

Afnd.tests()


def principal(accion, automata):
	continuar = "s"
	while continuar == "s":
		cadena = input("Ingrese cadena: ")
		mensaje = accion(cadena, automata)
		print(mensaje)
		continuar = input("Desea continuar? (s/n): ")


def buscarMaches(cadena, automata):
		return automata.buscarPatrones(cadena)

def buscarCadenas(cadena, automata):
		return automata.aceptarCadena(cadena)

# regExp = "|..baba"
regExp = "|a..bab"
# regExp = "|ab"

# alfabeto = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 \n"
alfabeto = "ab"
afnd1 = Afnd.fromRegExpToAfnd(regExp, alfabeto, [])
afnd1Invertido = afnd1.invertir()
afnd1.addLoopsTexto()
afd1 = afnd1.convertToAfd()

principal(buscarMaches, afd1)



# pdb.set_trace();True