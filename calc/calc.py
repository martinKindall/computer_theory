
import pdb

import ply.lex as lex
import ply.yacc as yacc
import sys


tokens = [
	'FLOAT',
	'INT',
	'NAME',
	'PLUS',
	'MINUS',
	'DIVIDE',
	'MULTIPLY',
	'EQUALS',
	'LEFT_PAR',
	'RIGHT_PAR',
	'LESSTHAN',
	'LESSTHANEQ',
	'GREATTHAN',
	'GREATTHANEQ',
	'NOTEQUAL',
	'ISEQUAL',
	'INPUT',
	'PRINT',
	'IF',
	'THEN',
	'ELSE',
	'WHILE',
	'DO',
	'TERM',
	'RIGHT_KEY',
	'LEFT_KEY'
]

t_PLUS = r'\+'
t_MINUS = r'\-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'\/'
t_EQUALS = r'\='
t_LESSTHAN = r'\>'
t_LESSTHANEQ = r'\>='
t_GREATTHAN = r'\<'
t_GREATTHANEQ = r'\<='
t_NOTEQUAL = r'\!\='
t_ISEQUAL = r'\=\='

t_ignore = r' '


def t_FLOAT(t):
	r'\d+\.\d+'
	t.value = float(t.value)
	return t


def t_INT(t):
	r'\d+'
	t.value = int(t.value)
	return t


def t_IF(t):
	r'if'
	t.type = 'IF'
	return t


def t_THEN(t):
	r'then'
	t.type = 'THEN'
	return t


def t_ELSE(t):
	r'else'
	t.type = 'ELSE'
	return t


def t_WHILE(t):
	r'while'
	t.type = 'WHILE'
	return t


def t_do(t):
	r'do'
	t.type = 'DO'
	return t


def t_TERM(t):
	r'\;'
	t.type = 'TERM'
	return t


def t_LEFT_KEY(t):
	r'\{'
	t.type = 'LEFT_KEY'
	return t


def t_RIGHT_KEY(t):
	r'\}'
	t.type = 'RIGHT_KEY'
	return t


def t_LEFT_PAR(t):
	r'\('
	t.type = 'LEFT_PAR'
	return t


def t_RIGHT_PAR(t):
	r'\)'
	t.type = 'RIGHT_PAR'
	return t


def t_INPUT(t):
	r'read\(\)'
	t.type = 'INPUT'
	return t


def t_PRINT(t):
	r'print'
	t.type = 'PRINT'
	return t


def t_NAME(t):
	r'[a-z0-9]+'
	t.type = 'NAME'
	return t


def t_error(t):
	print("Illegal characters!")
	t.lexer.skip(1)


lexer = lex.lex()  


precedence = (
	('nonassoc', 'LESSTHANEQ', 'GREATTHANEQ'),
	('nonassoc', 'LESSTHAN', 'GREATTHAN'),
	('left', 'PLUS', 'MINUS'),
	('left', 'MULTIPLY', 'DIVIDE'),
	('left', 'IF'),
	('left', 'ELSE')
)


def p_calc(p):
	'''
	calc : if_else 
		 | if 
		 | while_do 
		 | read TERM
		 | print TERM
		 | var_assign TERM
		 | expression
	     | empty
	'''
	print(run(p[1]))


def p_if_else(p):
	'''
	if_else : IF LEFT_PAR expression RIGHT_PAR then_statement else_statement
	'''
	p[0] = ('if_else', p[3], p[5], p[6])


def p_if(p):
	'''
	if : IF LEFT_PAR expression RIGHT_PAR then_statement
	'''
	p[0] = ('if', p[3], p[5])


def p_then_statement(p):
	'''
	then_statement : THEN calc_2 
	'''
	p[0] = p[2]


def p_else_statement(p):
	'''
	else_statement : ELSE calc_2
	'''
	p[0] = p[2]


def p_while_do(p):
	'''
	while_do : WHILE LEFT_PAR expression RIGHT_PAR do_statement
	'''
	p[0] = ('while', p[3], p[5])


def p_do_statement(p):
	'''
	do_statement : DO calc_2
	'''
	p[0] = p[2]


def p_calc_2(p):
	'''
	calc_2 : if_else 
		 | if 
		 | while_do 
		 | read TERM
		 | print TERM
		 | var_assign TERM
		 | expression
	'''
	p[0] = p[1]


def p_calc_2_keys(p):
	'''
	calc_2 : LEFT_KEY calc_2 RIGHT_KEY 
	'''
	p[0] = p[2]


def p_calc_2_subtasks(p):
	'''
	calc_2 : calc_2 calc_2
	'''
	p[0] = ('subtasks', p[1], p[2])


def p_var_assign(p):
	'''
	var_assign : NAME EQUALS expression
	'''
	p[0] = ('=', p[1], p[3])


def p_read(p):
	'''
	read : NAME EQUALS INPUT
	'''
	p[0] = ('=', p[1], int(input()))


def p_print(p):
	'''
	print : PRINT LEFT_PAR expression RIGHT_PAR
	'''
	p[0] = ('print', p[3])


def p_expression(p):
	'''
	expression : expression MULTIPLY expression
			   | expression DIVIDE expression
			   | expression PLUS expression
			   | expression MINUS expression
			   | expression LESSTHAN expression
			   | expression LESSTHANEQ expression
			   | expression GREATTHAN expression
			   | expression GREATTHANEQ expression
			   | expression NOTEQUAL expression
			   | expression ISEQUAL expression
	'''
	p[0] = (p[2], p[1], p[3])


def p_expression_left_right_par(p):
	'''
	expression : LEFT_PAR expression RIGHT_PAR
	'''
	p[0] = p[2]


def p_expression_minus(p):
	'''
	expression : MINUS expression
	'''
	p[0] = ('-', 0, p[2])


def p_expression_int_float(p):
	'''
	expression : INT
			   | FLOAT
	'''
	p[0] = p[1]


def p_expression_var(p):
	'''
	expression : NAME
	'''
	p[0] = ('var', p[1])


# def p_error(p):
	# print("Syntax error found!")


def p_empty(p):
	'''
	empty :
	'''
	p[0] = None


parser = yacc.yacc()

env = {}

def run(p):
	global env
	if type(p) == tuple:
		if p[0] == '+':
			return run(p[1]) + run(p[2])
		elif p[0] == '-':
			return run(p[1]) - run(p[2])
		elif p[0] == '*':
			return run(p[1]) * run(p[2])
		elif p[0] == '/':
			return run(p[1]) / run(p[2])
		elif p[0] == '=':
			env[p[1]] = run(p[2])
		elif p[0] == '==':
			return run(p[1]) == run(p[2])
		elif p[0] == '!=':
			return run(p[1]) != run(p[2])
		elif p[0] == '<':
			return run(p[1]) < run(p[2])
		elif p[0] == '>':
			return run(p[1]) > run(p[2])
		elif p[0] == '<=':
			return run(p[1]) <= run(p[2])
		elif p[0] == '>=':
			return run(p[1]) >= run(p[2])
		elif p[0] == 'print':
			print(run(p[1]))
		elif p[0] == 'if':
			if run(p[1]):
				run(p[2])
		elif p[0] == 'if_else':
			if run(p[1]):
				run(p[2])
			else:
				run(p[3])
		elif p[0] == 'while':
			while run(p[1]):
				run(p[2])
				
		elif p[0] == 'subtasks':
			run(p[1])
			run(p[2])

		elif p[0] == 'var':
			if p[1] not in env:
				raise ValueError('Undeclared variable found!')
			else:
				return env[p[1]]
	else:
		return p
	

while True:
	try:
		s = input('>> ')
	except EOFError:
		break

	try:
		parser.parse(s)
	except ValueError as e:
		print(e)