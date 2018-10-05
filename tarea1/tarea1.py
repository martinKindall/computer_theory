import sys
import pdb
from Afnd import Afnd
from PatternMatch import PatternMatch


# Afnd.tests()


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


def pruebas():
	regExp = "|a..bab"
	alfabeto = "ab"

	afnd1 = Afnd.fromRegExpToAfnd(regExp, alfabeto, [])
	afnd1Invertido = afnd1.invertir()
	afnd1.addLoopsTexto()

	afd1 = afnd1.convertToAfd()
	afd1Inv = afnd1Invertido.convertToAfd()

	principal(buscarMaches, afd1, afd1Inv)


def main():
	argumentos = sys.argv

	if len(argumentos) != 3:
		raise Exception("uso correcto: python3 tarea1.py archivo regEx")

	texto = argumentos[1]
	regEx = argumentos[2]

	file = open(texto + ".txt", "r").read()
	# pdb.set_trace()
	matches = PatternMatch.buscarYFormatear(regEx, file)

	for match in matches:
		print(match)


main()