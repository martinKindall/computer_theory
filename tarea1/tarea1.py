import sys
import pdb
from Afnd import Afnd
from PatternMatch import PatternMatch


Afnd.tests()
PatternMatch.tests()


def main():
	argumentos = sys.argv

	if len(argumentos) != 3:
		raise Exception("uso correcto: python3 tarea1.py archivo regEx")

	texto = argumentos[1]
	regEx = argumentos[2]

	file = open(texto + ".txt", "r").read()
	matches = PatternMatch.buscarYFormatear(regEx, file)

	for match in matches:
		print(match)


main()