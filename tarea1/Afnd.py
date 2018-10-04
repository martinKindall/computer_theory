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
		estadoFinal = estados.copy()
		for estado in estados:
			if '€' in delta[estado]:
				masEstados = delta[estado]['€']
				for estadoActual in masEstados:
					estadoFinal.update(Afnd._clausuraEpsilon(set([estadoActual]), delta))

		return estadoFinal


	@staticmethod
	def _createOrAddDict(diccionario, key1, key2, value):
		# pdb.set_trace()
		if key1 not in diccionario:
			diccionario[key1] = {key2: value}
		else:
			diccionario[key1][key2] = value


	def __init__(self, regExp, alfabeto="ab"):
		self.delta = []
		self.inicio = 0
		self.final = 1
		# self.alfabeto = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 \n"
		self.alfabeto = alfabeto
		self._erToAfnd(regExp)


	def convertToAfd(self):
		# clausura epsilon estado inicial
		estadoInicial = Afnd._clausuraEpsilon(set([self.inicio]), self.delta)
		estados = {0:estadoInicial.copy()}
		contadorEstados = 0
		estadosNoVistos = Pila()
		estadosNoVistos.apilar(contadorEstados)
		contadorEstados += 1
		deltaD = {}
		finalesD = []
		# pdb.set_trace()

		while not estadosNoVistos.estaVacia():
			indexEstado = estadosNoVistos.desapilar()
			estadosActual = estados[indexEstado]
			for char in self.alfabeto:
				# pdb.set_trace()
				estadosFinales = set()
				for current in estadosActual:
					if char in self.delta[current]:
						estadosFinales.update(Afnd._clausuraEpsilon(set(self.delta[current][char]), self.delta))

				newEstado = True
				for key, value in estados.items():
					if len(set(value)^estadosFinales) == 0:
						Afnd._createOrAddDict(deltaD, indexEstado, char, key)
						newEstado = False
						break

				# pdb.set_trace()
				if newEstado:
					Afnd._createOrAddDict(deltaD, indexEstado, char, contadorEstados)
					estadosNoVistos.apilar(contadorEstados)
					estados[contadorEstados] = estadosFinales
					contadorEstados += 1

		for key, value in estados.items():
			if self.final in value:
				finalesD.append(key)

		pdb.set_trace()
		return Afd(deltaD, self.alfabeto, finalesD)



	def addLoopsTexto(self):
		for char in self.alfabeto:
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
			# pdb.set_trace()
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
				print("La expresión contiene un caracter fuera del alfabeto")
				assert False

		arcos.desapilar()
		if not arcos.estaVacia():
			assert False