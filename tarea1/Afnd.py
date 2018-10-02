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
	def _actualizarContador(cont):
		cont += 1
		c1 = cont
		cont += 1
		c2 = cont

		return (cont, c1, c2)


	def _erToAfnd(self, regExp):

		indice = -1
		c1 = 0
		c2 = 0

		for char in regExp[::-1]:
			if char in self.alfabeto:
				indice, c1, c2 = self._actualizarContador(indice)

				afnd1 = {}
				afnd2 = {}
				afnd1[char] = c2
				self.deltas.append(afnd1)
				self.deltas.append(afnd2)

				self.arcos.apilar([c1, c2])

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
				indice, c1, c2 = self._actualizarContador(indice)
				arco21, arco22 = self.arcos.desapilar()
				arco11, arco12 = self.arcos.desapilar()
				self.arcos.apilar([c1, c2])

				self.deltas.append({})
				self.deltas.append({})
				self.deltas[c1]['€'] = (arco11, arco21)
				self.deltas[arco12]['€'] = c2
				self.deltas[arco22]['€'] = c2

				if self.inicio == arco21 or self.inicio == arco11:
					self.inicio = c1
				if self.final == arco22 or self.final == arco12:
					self.final = c2

			elif char == '*':
				indice, c1, c2 = self._actualizarContador(indice)
				arco1, arco2 = self.arcos.desapilar()
				self.arcos.apilar([c1, c2])

				self.deltas.append({})
				self.deltas.append({})
				self.deltas[c1]['€'] = (arco1, c2)
				self.deltas[arco2]['€'] = (arco1, c2)

				if self.inicio == arco1:
					self.inicio = c1
				if self.final == arco2:
					self.final = c2
			
			else:
				print("La expresión contiene un caracter fuera del alfabeto")
				assert False
			