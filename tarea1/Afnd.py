from Pila import Pila
import pdb


class Afnd:
	def __init__(self, regExp):
		self.arcos = Pila()
		self.deltas = []
		self.inicio = 0
		self.final = 0
		self.alfabeto = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 \n"
		self._erToAfnd(regExp)


	@staticmethod
	def _actualizarContador(indice):
		indice += 1
		id1 = indice
		indice += 1
		id2 = indice

		return (indice, id1, id2)


	# _erToAfnd: string -> None
	# convierte una expresion regular a un automata
	# no deterministico usando Thompson!
	# efecto: modifica el afnd		
	def _erToAfnd(self, regExp):

		indice = -1
		id1 = 0
		id2 = 0

		for char in regExp[::-1]:
			if char in self.alfabeto:
				indice, id1, id2 = self._actualizarContador(indice)

				afnd1 = {}
				afnd2 = {}
				afnd1[char] = id2
				self.deltas.append(afnd1)
				self.deltas.append(afnd2)

				self.arcos.apilar([id1, id2])

			elif char == '.':
				arco21, arco22 = self.arcos.desapilar()
				arco11, arco12 = self.arcos.desapilar()
				self.arcos.apilar([arco11, arco22])
				
				self.deltas[arco12]['€'] = arco21

				if self.inicio == arco21:
					self.inicio = arco11
				if self.final == arco12:
					self.final = arco22

			elif char == '|':
				indice, id1, id2 = self._actualizarContador(indice)
				arco21, arco22 = self.arcos.desapilar()
				arco11, arco12 = self.arcos.desapilar()
				self.arcos.apilar([id1, id2])

				self.deltas.append({})
				self.deltas.append({})
				self.deltas[id1]['€'] = (arco11, arco21)
				self.deltas[arco12]['€'] = id2
				self.deltas[arco22]['€'] = id2

				if self.inicio == arco21 or self.inicio == arco11:
					self.inicio = id1
				if self.final == arco22 or self.final == arco12:
					self.final = id2

			elif char == '*':
				indice, id1, id2 = self._actualizarContador(indice)
				arco1, arco2 = self.arcos.desapilar()
				self.arcos.apilar([id1, id2])

				self.deltas.append({})
				self.deltas.append({})
				self.deltas[id1]['€'] = (arco1, id2)
				self.deltas[arco2]['€'] = (arco1, id2)

				if self.inicio == arco1:
					self.inicio = id1
				if self.final == arco2:
					self.final = id2
			
			else:
				print("La expresión contiene un caracter fuera del alfabeto")
				assert False
			