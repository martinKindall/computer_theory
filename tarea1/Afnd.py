from Pila import Pila
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
	def _clausuraEpsilon(estado, delta):
		estadoFinal = [estado]
		if '€' in delta[estado]:
			masEstados = delta[estado]['€']
			for estadoActual in masEstados:
				estadoFinal += Afnd._clausuraEpsilon(estadoActual, delta)

		return estadoFinal


	def __init__(self, regExp):
		self.delta = []
		self.inicio = 0
		self.final = 1
		self.alfabeto = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 \n"
		self._erToAfnd(regExp)



	def convertToAfd(self):
		# clausura epsilon estado inicial
		estadoInicial = Afnd._clausuraEpsilon(self.inicio, self.delta)

		pdb.set_trace();True


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
				arco21, arco22 = arcos.desapilar()
				arco11, arco12 = arcos.desapilar()
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