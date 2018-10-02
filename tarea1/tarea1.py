from Nodo import Nodo
from Pila import Pila
from Lista import Lista
from Afnd import Afnd

import pdb

def fromRegToNodo(regExp):
	pila = Pila()
	memoria = 0

	for char in regExp[::-1]:
		if char not in "*.|":
			pila.apilar(char)
		else:
			izq = pila.desapilar()
			der = pila.desapilar()
			pila.apilar(Nodo(char, izq, der))

	return pila.desapilar()


regExp = "|a..bab"

alfabeto = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 \n"

arbolReg = fromRegToNodo(regExp)

pdb.set_trace();True