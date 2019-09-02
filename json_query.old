import json
import re
from itertools import cycle
import sys
import logging

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger("engine") #.addHandler(handler)


base_regex = re.compile(r'^[*{0,1}]*[/\w+]+[\[\d+:*\d*\]]*[\[\w+\W+\]]*')

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
	op = re.compile(r'[==|!=|>=|<=|in|notin]{1}')
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

def intersection(lst1, lst2): 
    lst3 = [value for value in lst1 if value in lst2] 
    return lst3

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


def  CleanTokensPath(lista):
	logger.debug(lista)
	for item in  lista:
		if item == '' or item is None:
			continue
		yield item


class JsonQuery(object):

	def __init__(self, query, dataset ):
		self.query = query
		self.dataset = dataset

	"""
	================================================
	"""



	def __parseQuery(self,query):

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
				raise Exception('Sintaxis invalida: token ' + part + ' No se esperaba aca')
		return operations


	def __indexOrQuery(self,chunk):
		logger.debug('indexOrQuery')
		logger.debug(chunk)

		index_pattern = re.compile(r'\d+:*\d*')
		retval = {}
		if index_pattern.match(chunk):
			return {
				"type" : "index",
				"value" : chunk
			}	
		else:
			return {
				"type" : "query",
				"value" : chunk
			} 


	def __getIndexAndQuery(self,token):
		query = index = data1 = data2 = None
		selectors = []
		retval = {}
		logger.info('getIndexAndQuery')
		pt = re.compile(r'\w+\[+')
		index_pattern = re.compile(r'\d+:*\d*')
		#check si es que contien un indice
		if pt.match(token):
			tokens = token.split('[')
			selectors.append({'type' : 'path',"value" :  tokens[0]})
			selectors.append( self.__indexOrQuery(tokens[1][0:tokens[1].find(']')]) )
			if len(tokens) == 3:
				selectors.append( self.__indexOrQuery( tokens[2][0:tokens[2].find(']')] ) )

		else:
			logger.debug('path')
			selectors.append({'type' : 'path',"value" : token})

		#logger.debug(selectors)
		for item in selectors:
			retval.update({item['type'] : item['value']})
		
		return retval

	def __createProgram(self,tokens):

		program = []
		_path = re.compile(r'\w+')
		_path_idx = re.compile(r'\w+\[[\W\w=<>\'\w]+\]')
		_idx = re.compile(r'\d+')

		#GEt index

		for item in tokens:
			#es parh o query
			
			program_part = self.__getIndexAndQuery(item)
			program.append({
				"path" : program_part['path'],
				"index" : program_part['index'] if 'index' in program_part else None,
				"query" : self.__parseQuery(program_part['query']) if 'query' in program_part else None,
				"select" : "*"
				})

		return program


	def __programOperations(self,program):
		p1 = re.compile(r'^@')
		#logger.debug(program)
		retval = []
		
		for idx in range(0,len(program)-1,4):
			#logger.info('*********************************************************')
			logical = None
			field =  program[idx]['value'] if p1.match(program[idx]['value']) else program[idx+2]['value']
			operator = program[idx + 1]['value']
			value = program[idx]['value'] if not p1.match(program[idx]['value']) else program[idx+2]['value']
			if idx +3 < len(program):
				logical = program[idx+3]['value']
			retval.append( {
				"field" : field,
				"operation" : operator,
				"value" : value,
				"logical" : logical
			})

		return retval


	def __executeSelectors(self,program,dataset):
		logger.info('Ejecutando Plan')
		p1 = re.compile(r'^@')
		isarr = re.compile(r'[\w]+\?')

		def mergeResult(resultset):
			if len (resultset) > 1:
				lst1,lst2 = resultset[0]['data'],resultset[1]['data']
				# lst3 = [value for value in lst1 if value in lst2] 
				# logger.debug('----------------')
				# logger.debug(lst3)
				return lst1 + lst2
			return resultset

		def select(field,operador,value,dataset):

			result = []
			for item in dataset:
				#check field
				f = field.replace('@','')
				# logger.debug(f)
				#check si hay que buscar dentro de un array

				field_value = "'" +item[f]+ "'"  if isinstance(item[f],str) else item[f]
				# logger.debug(operador+".")
				oper = 'not in' if operador == 'notin' else operador

				operation =  str(value) + ' ' + oper + ' ' + str(field_value) if isinstance(field_value,list) \
							    else str(field_value) + ' ' + oper + ' ' + str(value)
				#logger.debug(operation)
				if eval(operation):
					result.append(item)
			return result


		idx = 0
		result = dataset[:]
		#Aca se procesa todos los selectores que están dentro de [  instrucciones  ]. El dataset origen 
		print(len(program))
		resultset = []

		#deterinar cuantas operaciones se van a realizar acá.
		numoper = len(program) // 3 
		logger.debug('Numero de datasets necesarios: ' + str(numoper))
		
		#las intersecciones o uniones se necesitan con al menos 2 operaciones
		#La operación y se hace cone el resultado de la anterior.
		
		operationProgram = self.__programOperations(program)
		logical_operation = None
		logger.debug('***************************')
		for oprs in operationProgram:
			if logical_operation is None or logical_operation == 'and':
				result = select(oprs['field'],oprs['operation'],oprs['value'],result)
			if logical_operation == 'or':
				rv = select(oprs['field'],oprs['operation'],oprs['value'],dataset)
				result = result + rv

			logical_operation = oprs['logical']
		logger.debug('***************************')
		logger.debug(result)

		return result



	def __executeProgram(self, program, isRoot = True):

		dataset = self.dataset
		result = None

		for sentence in program:
			
			""" 
	        En este punto se debe aplicar la funcion al nodo correspondiente
			"""
			#Primero se debe obtener todos los items con el nombre de nodo seleccionado
			node_name = sentence['path']
			query = sentence['query']
			index = sentence['index']

			try:
				dataset = dataset[node_name] #if node_name in dataset else None  
				
			except Exception as e:
				print(result)
				print(program)
				raise e

			if dataset is None:
				raise Exception('No existe el nodo: ' + node_name)

			#Que tipo de operacion se hará con el nodo:  un item?, una consulta ?

			if index is not None:  # obtener el item especifico
				dataset = dataset[int(index)]

			if query is not None:   # realizar una query sobre el resultado anterior
				dataset = self.__executeSelectors(sentence['query'],dataset)
		
				
		
		return dataset

	def __processPath(self,path,data):

		root = True
		path_tokens = []

		isRoot = re.compile(r'^\/{1}')
		#Primer check de estructura
		
		if not base_regex.match(path):
			raise Exception('La query no corresponde con la sintaxis: ' + path)

		root = True if isRoot.match(path) else False
		#Parse
		logger.info('#####    fase 1:  parse path   ###########')
		tokens_path = []
		for item in CleanTokensPath(path.split('/')):
			tokens_path.append(item)
		#normalizar
		logger.debug(tokens_path)

		if not root:
			del tokens_path[0]
		logger.info('#####    fase 2:  program plan  ###########')
		program = self.__createProgram(tokens_path)
		
		logger.info('#####    fase 3:  Ejecutar Programa  ###########')
		result = self.__executeProgram(program,root)
		
		return result

	def execute(self):
		return self.__processPath(self.query, self.dataset)

# def main():
# 	#path = "*/kkjk/asdf[@name='marcelo']"
# 	#path = "/a/b/c"
# 	print()
# 	path = sys.argv[1] # "/a/b[1][@valor == 1000]"  #[@valor == 1000 or @valor == 2000 ]->select('name')"
# 	data = {}
# 	with open(sys.argv[2],'r') as json_file:
# 		data = json.load(json_file)

# 	jsonquery = JsonQuery(path,data)
# 	retval = jsonquery.execute()	

# 	# retval = processPath(path,data)
# 	logger.info(retval)
# 	return retval




# if __name__ == "__main__":
# 	main()
