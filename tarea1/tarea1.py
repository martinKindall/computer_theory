from Afnd import Afnd

import pdb


# regExp = "|..baba"
regExp = "*|.ab..aba"
# regExp = "|ab"

afnd1 = Afnd(regExp)
# afnd1.addLoopsTexto()
afd1 = afnd1.convertToAfd()

continuar = "s"

while continuar == "s":
	cadena = input("Ingrese cadena: ")
	respuesta = "El automata acepto la cadena" if afd1.aceptarCadena(cadena) else "Cadena no reconocida"
	print(respuesta)
	continuar = input("Desea continuar? (s/n): ")

# pdb.set_trace();True