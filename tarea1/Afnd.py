from Pila import Pila
from Afd import Afd
import pdb


class Afnd:

	@staticmethod
	def _actualizarContador(indice):
		indice += 1
		id1 = indice
		indice += 1
		id2 = indice

		return (indice, id1, id2)


	@staticmethod
	def _clausuraEpsilon(estados, delta):
		estadoFinal = set(estados)
		for estado in estados:
			if '€' in delta[estado]:
				masEstados = delta[estado]['€']
				for estadoActual in masEstados:
					estadoFinal.update(Afnd._clausuraEpsilon([estadoActual], delta))

		return estadoFinal


	@staticmethod
	def _createOrAddDict(diccionario, key1, key2, value):
		if key1 not in diccionario:
			diccionario[key1] = {key2: value}
		else:
			diccionario[key1][key2] = value


	@staticmethod
	def fromRegExpToAfnd(regExp, alfabeto, delta):
		automata = Afnd(alfabeto, delta)
		automata._erToAfnd(regExp)

		return automata


	def __init__(self, alfabeto, delta, inicio=0, final=1):
		self.alfabeto = alfabeto
		self.delta = delta
		self.inicio = inicio
		self.final = final


	def convertToAfd(self):
		# clausura epsilon estado inicial
		estadoInicial = Afnd._clausuraEpsilon([self.inicio], self.delta)

		estados = {0:estadoInicial.copy()}
		contadorEstados = 0
		estadosNoVistos = Pila()
		estadosNoVistos.apilar(contadorEstados)
		contadorEstados += 1
		deltaD = {}
		finalesD = []


		while not estadosNoVistos.estaVacia():
			indexEstado = estadosNoVistos.desapilar()
			estadosActual = estados[indexEstado]
			for char in self.alfabeto:
				
				estadosFinales = set()
				for current in estadosActual:
					if char in self.delta[current]:
						estadosFinales.update(Afnd._clausuraEpsilon(self.delta[current][char], self.delta))

				newEstado = True
				for key, value in estados.items():
					if len(set(value)^estadosFinales) == 0:
						Afnd._createOrAddDict(deltaD, indexEstado, char, key)
						newEstado = False
						break
				
				if newEstado:
					Afnd._createOrAddDict(deltaD, indexEstado, char, contadorEstados)
					estadosNoVistos.apilar(contadorEstados)
					estados[contadorEstados] = estadosFinales
					contadorEstados += 1

		for key, value in estados.items():
			if self.final in value:
				finalesD.append(key)

		

		return Afd(deltaD, self.alfabeto, finalesD)


	def addLoopsTexto(self):
		for char in self.alfabeto:
			if char not in self.delta[self.inicio]:
				self.delta[self.inicio][char] = (self.inicio,)


	# _erToAfnd: string -> None
	# convierte una expresion regular a un automata
	# no deterministico usando Thompson!
	# efecto: modifica el afnd		
	def _erToAfnd(self, regExp):

		indice = -1
		id1 = 0
		id2 = 0
		arcos = Pila()

		for char in regExp[::-1]:
			
			if char in self.alfabeto:
				indice, id1, id2 = self._actualizarContador(indice)

				afnd1 = {}
				afnd2 = {}
				afnd1[char] = (id2,)
				self.delta.append(afnd1)
				self.delta.append(afnd2)

				arcos.apilar([id1, id2])

			elif char == '.':
				arco11, arco12 = arcos.desapilar()
				arco21, arco22 = arcos.desapilar()
				arcos.apilar([arco11, arco22])
				
				self.delta[arco12]['€'] = (arco21,)

				if self.inicio == arco21:
					self.inicio = arco11
				if self.final == arco12:
					self.final = arco22

			elif char == '|':
				indice, id1, id2 = self._actualizarContador(indice)
				arco21, arco22 = arcos.desapilar()
				arco11, arco12 = arcos.desapilar()
				arcos.apilar([id1, id2])

				self.delta.append({})
				self.delta.append({})
				self.delta[id1]['€'] = (arco11, arco21)
				self.delta[arco12]['€'] = (id2,)
				self.delta[arco22]['€'] = (id2,)

				if self.inicio == arco21 or self.inicio == arco11:
					self.inicio = id1
				if self.final == arco22 or self.final == arco12:
					self.final = id2

			elif char == '*':
				indice, id1, id2 = self._actualizarContador(indice)
				arco1, arco2 = arcos.desapilar()
				arcos.apilar([id1, id2])

				self.delta.append({})
				self.delta.append({})
				self.delta[id1]['€'] = (arco1, id2)
				self.delta[arco2]['€'] = (arco1, id2)

				if self.inicio == arco1:
					self.inicio = id1
				if self.final == arco2:
					self.final = id2
			
			else:
				raise Exception("La expresión contiene un caracter fuera del alfabeto: a, ..., z, A, ..., Z, 0, ..., 9, ,\\n")

		arcos.desapilar()
		if not arcos.estaVacia():
			raise Exception("Expresion regular debe estar en notación prefijo y ser correcta. Ej: |a..bab")


	def invertir(self):
		newDelta = [{} for _ in range(len(self.delta))]

		for idx, mDelta in enumerate(self.delta):
			for char in self.alfabeto + '€':
				if char in mDelta:
					for initEstado in mDelta[char]:
						if char not in newDelta[initEstado]:
							newDelta[initEstado][char] = (idx,)
						else:
							newDelta[initEstado][char] += (idx,)


		return Afnd(self.alfabeto, newDelta, self.final, self.inicio)


	@staticmethod
	def tests():
		regExp = "*|.ab..aba"
		alfabeto = "ab"
		afnd1 = Afnd.fromRegExpToAfnd(regExp, alfabeto, [])
		afd1 = afnd1.convertToAfd()

		assert afd1.aceptarCadena("ab")
		assert afd1.aceptarCadena("aba")
		assert afd1.aceptarCadena("abaab")
		assert afd1.aceptarCadena("ababababababaab")
		assert afd1.aceptarCadena("abababbabababaab") == False
		assert afd1.aceptarCadena("aab") == False
		assert afd1.aceptarCadena("bab") == False
		assert afd1.aceptarCadena("baba") == False
		assert afd1.aceptarCadena("bb") == False
		assert afd1.aceptarCadena("abaaab") == False
		assert afd1.aceptarCadena("b") == False
		assert afd1.aceptarCadena("a") == False

		regExp2 = "|ab"
		afnd2 = Afnd.fromRegExpToAfnd(regExp2, alfabeto, [])
		afd2 = afnd2.convertToAfd()

		assert afd2.aceptarCadena("a")
		assert afd2.aceptarCadena("b")
		assert afd2.aceptarCadena("aa") == False
		assert afd2.aceptarCadena("bb") == False

		regExp3 = "|a..bab"
		afnd3 = Afnd.fromRegExpToAfnd(regExp3, alfabeto, [])
		afd3 = afnd3.convertToAfd()

		assert afd3.aceptarCadena("a")
		assert afd3.aceptarCadena("bab")
		assert afd3.aceptarCadena("aa") == False
		assert afd3.aceptarCadena("bb") == False
		assert afd3.aceptarCadena("aba") == False
		assert afd3.aceptarCadena("babb") == False

		regExp4 = "..*|ab.ba*|ab"
		afnd4 = Afnd.fromRegExpToAfnd(regExp4, alfabeto, [])
		afd4 = afnd4.convertToAfd()

		assert afd4.aceptarCadena("aba")
		assert afd4.aceptarCadena("bab")
		assert afd4.aceptarCadena("babb") 
		assert afd4.aceptarCadena("aaaaaaaaaaaababbbbbbbbbbbbbbbbbbbb") 
		assert afd4.aceptarCadena("bbbbbbbbbbbbbbbbbbbbbabbbbbbbbbbbbbbbbbbbb") 
		assert afd4.aceptarCadena("aa") == False
		assert afd4.aceptarCadena("bb") == False

		regExp5 = "..bab"
		afnd5 = Afnd.fromRegExpToAfnd(regExp5, alfabeto, [])
		afd5 = afnd5.convertToAfd()

		assert afd5.aceptarCadena("bab")
		assert afd5.aceptarCadena("baba") == False
		assert afd5.aceptarCadena("aa") == False
		assert afd5.aceptarCadena("bb") == False
		assert afd5.aceptarCadena("aba") == False
		assert afd5.aceptarCadena("babb") == False

		regExp6 = "*a"
		afnd6 = Afnd.fromRegExpToAfnd(regExp6, alfabeto, [])
		afd6 = afnd6.convertToAfd()

		assert afd6.aceptarCadena("a") 
		assert afd6.aceptarCadena("aa") 
		assert afd6.aceptarCadena("aaaaaaaaa") 
		assert afd6.aceptarCadena("bab") == False
		assert afd6.aceptarCadena("bb") == False
		assert afd6.aceptarCadena("aba") == False
		assert afd6.aceptarCadena("babb") == False