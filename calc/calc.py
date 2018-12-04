import ply.lex as lex
import ply.yacc as yacc
import sys


tokens = [
	'INT',
	'FLOAT',
	'NAME',
	'PLUS',
	'MINUS',
	'DIVIDE',
	'MULTIPLY',
	'EQUALS'
]

t_PLUS = r'\+'
t_MINUS = r'\-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'\/'
t_EQUALS = r'\='

t_ignore = r' '


def t_FLOAT(t):
	r'\d+\.\d+'
	t.value = float(t.value)
	return t


def t_INT(t):
	r'\d+'
	t.value = int(t.value)
	return t


def t_NAME(t):
	r'[a-zA-Z_][a-zA-Z_0-9]*'
	t.type = 'NAME'
	return t


def t_error(t):
	print("Illegal characters!")
	t.lexer.skip(1)


lexer = lex.lex()  

lexer.input("abc = 123.456")

while True:
	tok = lexer.token()

	if not tok:
		break
	print(tok)




