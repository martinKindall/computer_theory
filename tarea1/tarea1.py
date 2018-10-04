from Afnd import Afnd

import pdb


Afnd.tests()

# regExp = "|..baba"
regExp = "*|.ab..aba"
# regExp = "|ab"

# alfabeto = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 \n"
alfabeto = "ab"
afnd1 = Afnd.fromRegExpToAfnd(regExp, alfabeto)
# afnd1.addLoopsTexto()
afd1 = afnd1.convertToAfd()

continuar = "s"

while continuar == "s":
	cadena = input("Ingrese cadena: ")
	respuesta = "El automata acepto la cadena" if afd1.aceptarCadena(cadena) else "Cadena no reconocida"
	print(respuesta)
	continuar = input("Desea continuar? (s/n): ")

# pdb.set_trace();True