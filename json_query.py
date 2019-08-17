import json
import re
from itertools import cycle

base_regex = re.compile(r'^[*{0,1}]*[/\w+]+[\[\w+\W+\]]*')

_input = { "a" : { "b" : { "c" : 1000 } } }

_input2 = { "a" : { "b" : [ { "name" : "a", "valor" : 1000 },{"name" : "b","valor" :2000},{"name" : "c","valor": 3000}]}}

def operando(valor):
	#print('Operando')
	p1 = re.compile(r'^@')
	p2 = re.compile(r'[\'\w+\'|\d+]+')

	if p1.match(valor) or p2.match(valor):
		return {
			"type": "operando",
			"value": valor 
		}
	return None

def operador(valor):
	#print('Operador')
	op = re.compile(r'[==|!=|>=|<=]{1}')
	if op.match(valor):
		return {
			"type": "operacion",
			"value": valor
		}
	return None

def logical(valor):
	#print('Logical: .' + valor +'.')
	log = re.compile(r'[and|or]{1}')
	if log.match(valor):
		return {
			"type": "logico",
			"value": valor
		}
	return None


query_struct ={
	'operando1': operando,
	'operador' : operador,
	'operando2': operando ,
	'logical'  : logical,
}

clist =[ 'operando1', 'operador','operando2' ,'logical' ]

secuence = cycle(clist)

class CircularList(object):

	def __init__(self,lista):
		self._index = 0
		self._list = lista

	def __iter__(self):
		return self

	def __next__(self):
		current = self._list[self._index]
		self._index += 1
		if self._index>= len(self._list):
			self._index = 0
		return current


def parseQuery(query):

	tokens = query.split(' ')
	secuencia = CircularList(clist)
	operations = []
	for part in tokens:
		if part == '':
			continue
		op = query_struct[next(secuencia)](part)
		if op is not None:
			operations.append(op)
		else:
			raise Exception('Sintaxis invalida: token ' + part + ' No se esperaba acá')
	return operations


def createProgram(tokens):

	program = []
	_path = re.compile(r'\w+')
	_path_idx = re.compile(r'\w+\[[\W\w=<>\'\w]+\]')
	_idx = re.compile(r'\d+')

	for item in tokens:
		#es parh o query
	
		if _path_idx.match(item):
			s = item.index('[') + 1 
			f = item.index(']')
			#obtener el select
			query = item[s:f]
			if _idx.match(query):
				program.append({ 'path' : item[0:s-1] , 'index' : query , 'query' : None , 'select' : '*' })
			else:
				program.append({ 'path' : item[0:s-1] , 'index' : None , 'query' : parseQuery(query) , 'select': '*' })
			continue
		if _path.match(item):   #es un indice
			program.append({ 'path' : item , 'index' : None , 'query' : None })
			continue
	return program


def processPath(path):

	root = True
	path_tokens = []

	isRoot = re.compile(r'^\/{1}')
	#Primer check de estructura
	
	if not base_regex.match(path):
		raise Exception('La query no corresponde con la sintaxis: ' + path)

	root = True if isRoot.match(path) else False
	#Parse
	tokens_path = path.split('/')

	if not root:
		del tokens_path[0]

	program = createProgram(tokens_path)
	
	result = execute(program,_input2,root)
	print(result)
	return result


def executeQuery(program,data):
	p1 = re.compile(r'^@')

	def select(field,operador,value,dataset):
		print('Select')
		result = []
		for item in dataset:
			print(item)
			#check field
			f = field.replace('@','')
			
			field_value = "'" +item[f]+ "'"  if isinstance(item[f],str) else item[f]
			 
			operation = str(field_value) + operador + str(value)
			print(operation)
			if eval(operation):
				result.append(item)
		return result



	idx = 0
	result = data
	#print(program)
	print(len(program))
	logic_operator = 'and'
	for idx in range(0,len(program)-1,4):
		print('loop')
		field =  program[idx]['value'] if p1.match(program[idx]['value']) else program[idx+2]['value']
		operator = program[idx + 1]['value']
		value = program[idx]['value'] if not p1.match(program[idx]['value']) else program[idx+2]['value']
		if (idx + 3) < len(program):
			logic_operator = program[idx+3]['value']

		if logic_operator == 'and':
			result = select(field,operator,value,result)
		else:
			result = select(field,operator,value,data)

	return result



"""
================================================
"""
def execute(program,json = None, isRoot = True):

	dataset = json
	result = None
	print(program)
	for sentence in program:
		
		""" 
        En este punto se debe aplicar la funcion al nodo correspondiente
		"""
		#Primero se debe obtener todos los items con el nombre de nodo seleccionado
		node_name = sentence['path']
		query = sentence['query']
		index = sentence['index']
		print('loop ---------------- : ' + node_name)
		print(dataset)
		print('----------------------')
		try:
			dataset = dataset[node_name] #if node_name in dataset else None  
			
		except e as Exception:
			print(result)
			raise e

		if dataset is None:
			print(dataset)
			raise Exception('No existe el nodo: ' + node_name)

		#Que tipo de operacion se hará con el nodo:  un item?, una consulta ?

		if index is not None:  # obtener el item especifico
			print('indice:' )
			result = dataset[int(index)]

		if query is not None:   # realizar una query sobre el resultado anterior
			dataset = executeQuery(sentence['query'],dataset)
			continue
			
	
	return dataset

def getQuery(query):
	pass


_input = { "a" : { "b" : { "c" : 1000 } } }


def main():
	#path = "*/kkjk/asdf[@name='marcelo']"
	#path = "/a/b/c"
	path = "/a/b[1][@valor == 1000]"  #[@valor == 1000 or @valor == 2000 ]->select('name')"
	processPath(path)
	return

	pattern = re.compile(r'[*]{0,1}[/\\w-]+')
	if pattern.match(path):
		print('Corresponde')
	else:
		print('No corresponde')

	return

	tokens = path.split("/")
	data = _input
	if tokens[0] == '':  #Root
		for i in range(1,len(tokens)):
			if tokens[i] in data: 
				data = data[tokens[i]]
			else:
				raise Execption('Key ' + tokens[i] + ' does not exits')
		print(data)



if __name__ == "__main__":
	main()
