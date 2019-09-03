import re
import logging
import pprint
import json
import os
import sys

logging.basicConfig(level=logging.DEBUG)
pp = pprint.PrettyPrinter(depth=6)
"""

Operando ->  operacion | funcion 


"""
field = re.compile(r'[@\w!=<>\':\*"]')

_log = re.compile(r'^(and)|^(or)')

comp = re.compile(r'[!=<>]')

class States(object):

	def __init__(self, states):
		self._logger = logging.getLogger("States")
		self._states = states
		self._index = 0

	def __iter__(self):
		return self

	def __next__(self):

		current = self._states[self._index]
		self._logger.debug('indice: ' + str(self._index))
		self._logger.debug('retornando: ' + current)
		self._index += 1
		if self._index >= len(self._states):
			self._index = 0

		return current


def ffspace(text,idx):

	while idx < len(text):
		if text[idx] != ' ':
			return idx
		idx += 1
	return idx


def check(text):
	logger = logging.getLogger("check")
	text = text.lstrip().rstrip()
	operaciones = []
	operacion = {}
	operando = ''
	#-------------------
	idx = 0
	logger.info('.' + text + '.')
	state1 = States(['operando','comparador','operando','logical','close'])
	state = next(state1)
	logger.info(state)
	idopracion = 1
	while True:
		
		if state == 'close' or len(text) == idx:
			logger.info('close')
			operacion.update({ 'operando2': operando })
			operaciones.append(  operacion.copy())
			operacion.clear()
			operando =''
			state = next(state1)
			idx = ffspace(text,idx)
			if idx >= len(text):
				break
			continue

		if text[idx] == ' ':
			logger.debug('Space ' + str(idx))
			if state == 'operando' or state == 'logical':
				state = next(state1)
			idx += 1
			continue

		# and  /  or
		if state == 'logical':
			logger.info(text[idx:idx+3])
			if _log.match(text[idx:idx+3]):
				operacion.update({ 'logical' : text[idx:idx+3]})				
				idx += 3
				state = next(state1)
				continue
			else:
				raise Exception('Se esperaba un operador logic and / or en: ' + str(idx))

		if text[idx] in ['!','>','<','='] and state == 'operando':
			state = next(state1)
			logger.debug(state)

		if state == 'comparador':
			logger.debug('comparador')
			logger.debug(text[idx:idx+2])
			operacion.update({ 'operando1': operando })
			operando = ''
			#validar el operador
			operacion.update({ 'operador' : text[idx:idx+2]})
			#logger.debug('old:' + str(idx))
			idx = ffspace(text,idx + 2)
			#logger.debug('new:' + str(idx))
			logger.info(text[idx])
			state = next(state1)
			
		
		if state == 'operando' and field.match(text[idx]):
			#logger.debug('---> ' + str(text[idx]))
			operando += text[idx]
		# else:
		# 	raise Exception('Se esperaba un comparador: ' + text[idx])

		idx += 1
		if idx > len(text):
			break

	return operaciones


def groups(text):
	logger = logging.getLogger("groups")
	idGroup = 0
	idx = 0
	groupname = 'group' + str(idGroup) +'-0'
	groups = { groupname: []}
	temp = ''
	level = 0
	function = False
	function_level = 0
	while idx < len(text):

		if text[idx:idx+3] == 'fn:':
			logger.debug('function')
			logger.debug('Level ' +str(function_level))
			function_level += 1
			function = True

		if text[idx] == '(' and not function:  #open group
			logger.debug('open group ' + groupname)
			groups[groupname].append(temp)
			temp = ''

			idGroup += 1 if idx > 0 and not _open else 0

			groupname = 'group' + str(idGroup) + '-' + str(level)

			groups.update({groupname : [] })  #init
			level += 1
			idx += 1
			_open = True
			continue


		if  text[idx] == ')' and function:
			logger.debug('Close function Level: ' +str(function_level))
			function_level -= 1
			
			function = False if function_level == 0 else True
			temp+=text[idx] 
			idx+= 1
			continue

		if text[idx] == ')':
			#cierra grupoe
			logger.debug('close group')
			_open = False
			groups[groupname].append(temp)
			temp = ''
			level -= 1
			groupname = 'group' + str(idGroup) + '-' + str(level)
			idx += 1
			continue

		temp += text[idx] #if text[idx] != ' ' else ''

		idx += 1

	#logger.info(len(groups['group0-0']))
	if len(groups) == 1 and len(groups['group0-0']) == 0: # En caso que no hay parentesis
		groups['group0-0'] = temp

	return groups

def createProgram(query):
	grps = groups(query)
	logger = logging.getLogger("test")
	group_plan = {}
	newplan = []
	

	for key,value in grps.items():

		key = key.replace('group','')
		idgrp = key.split('-')[0]
		level = key.split('-')[1]
		groupname = 'group' + str(idgrp)
		print(key)
		print(idgrp)
		
		plan = check(''.join(value))

		if groupname in group_plan:
			logger.info(level)
			group = group_plan[groupname]
			logger.info('level: ' + str(level))
			group.append({ 'suboperacion' : plan} )
		else:
			group_plan.update ({ groupname : plan })

	return group_plan


def nodeParse(text):

	logger = logging.getLogger("nodeParse")
	logger.info(text)
	nname = re.compile(r'\w')
	nidx = re.compile(r'\d')
	states = States(['name','query1','query2'])
	state = next(states)
	idx = 0

	select = None
	if text.find('{') >= 0:
		select = text[text.find('{')+1:text.find('}')]		
		select = select.replace('\'','').replace('"','')
		select = select.split(',')
		text = text[:text.find('{')+1]

	node = { 'path' : text , 'idx' : None, 'query': '' , 'select': select }
	path = query1 = query2 = ''
	while idx < len(text):

		if nname.match(text[idx]) and state == 'name':	
			path = path + text[idx]
			idx+=1
			continue

		elif text[idx] == '[' and state == 'name': # es un array (excepcion)
			state = next(states)
			idx += 1

		if text[idx] == ']':
			idx+=1
			continue
		#cierre	
		if state == 'name':
			state = next(states)

		if state == 'query1':
			query1 += text[idx]
			idx+=1
			continue

		if state == 'query2':
			query2 += text[idx]
			idx+=1
			continue

		idx+=1
	node['path'] = path
	logger.info('query')
	logger.info(query1)
	if query1 != '' and nidx.match(query1): #podría ser indice o query
		node['idx'] = int(query1)
	else:
		if query1 != '':
			node['query'] = query1

	if query2 != '':
		node['query'] = query2

	return node


def executeQuery(query,dataset,select):
	logger = logging.getLogger("executeQuery")
	logger.info('ejecutando query')
	logger.debug(select)
	
	def fileterField(dataset,select):
		if select is None or select == '' or select == '*' :
			return dataset
		res = {}
		[ res.update({ k : v }) for k,v in dataset.items() if k in select]
		return res


	def execOperaciones(oprs,data):

		result = []  
		op_log = None
		subset = data.copy()
		for oper in oprs:  # cada operacion es un conjunto de dataset
			logger.debug('Operacion: ' + str(oper))

			if op_log == 'and':
				logger.debug('AND')
				logger.debug(len(result))
				subset = result.copy() #if len(result)>0 else subset
				result = []
			elif op_log == 'or':
				logger.debug('OR')
				subset = data.copy()

			op1 = oper['operando1']
			op2 = oper['operando2']
			comp = oper['operador']
			op_log = oper['logical'] if 'logical' in oper else None
			
			#select
			for dataitem in subset:  
				logger.debug('loop') 
				fieldname = op1[1:] if op1[0] == '@' else op2[1:]
				fieldvalue = dataitem[fieldname]
				logger.debug(fieldvalue)
				
				if isinstance(fieldvalue,list):
					logger.debug('--------->>>>>')
					value = op2.replace('"','').replace('\'','')
					logger.debug(value)
					logger.debug(value in fieldvalue)
					logger.debug(comp)
					if comp == '==' and value in fieldvalue:
						logger.debug('IN')
						result.append(fileterField(dataitem,select))
					elif comp == '!=' and value not in fieldvalue:
						logger.debug('NOT IN')
						result.append(fileterField(dataitem,select))
				elif isinstance(fieldvalue,str):
					value = op2
					o = 'fieldvalue' + comp + value
					logger.debug(o)
					if eval(o,{'fieldvalue' : fieldvalue}):
						logger.debug('True')
						result.append(fileterField(dataitem,select))
			
		return result

		

	#Por cada grupo
	for label , item in query.items():
		logger.info(label)
		logger.info(item)
		logger.debug('---------------')
		r = execOperaciones(item,dataset)
		return r
		# pp.pprint(r)
		# quit()


	



def seekPath(text,query):

	logger = logging.getLogger("seekPath")
	logger.info('Procesando query')
	if len(text) == 0:
		return None

	root = True if query[0] == '/' else False

	#cortar
	nodes = query.split('/')
	if not root:
		logger.debug('no es root')
		result = findnode(text,nodes[0])
	else:
		result = text.copy()


	logger.debug(result)
	quit()


	node = []
	for selectNode in filter(None ,nodes): #text
		logger.debug('Nodo seleccionado: ' + selectNode)
		nodeQuery = nodeParse(selectNode) #parsea la query
		#----------- 
		logger.debug(nodeQuery)
		logger.debug('----->')

		if nodeQuery['idx'] is not None \
		   and  nodeQuery['query']=='' \
		   and nodeQuery['path'] == '' \
		   and isinstance(result,list):  #TRaeer el nodo
			result = result[nodeQuery['idx']]
			continue
		# si el path es una lista y no tiene query, entonces error
		if isinstance(result,list) and \
		    nodeQuery['query'] == '' and \
		    nodeQuery['idx'] is None:

			logger.error('Es un lista')
			logger.error(nodeQuery)
			logger.error(result)
			raise Exception('El nodo ' + selectNode + ' es una lista')
		
		#Excepciones
		if nodeQuery['path'] not in result:
			return {}
		node = result[nodeQuery['path']]   #se trae el nodo
		logger.debug(type(node))
		
		if nodeQuery['query'] !='':
			logger.debug('Query')
			select = nodeQuery['select']
			r = createProgram(nodeQuery['query'])
			logger.info(r)
			node = executeQuery(r,node, select )

		if nodeQuery['idx'] is not None:  #TRaeer el nodo
			node = node[nodeQuery['idx']]
		result = node

		
	return result


def jsonquery(filename, path, _print = True):
	data = ''
	with open(filename,'r') as f:
		data = json.load(f)
	res = seekPath(data,path)
	if _print:
		pp.pprint(res)



test = "(@field!='algo' and @field2<>7) or (@field3<>5 and ( @field4!=10 or @field5 != 0  or ( a==b and c==d )))"#    ) and (fn:count(test)"
#       01234567890123456789012345678
test2 = "@field!='algo'"

#path = "/Statement[@Effect=='Allow' or @Action=='iam:passRole' or @Action=='s3:*']{'Action'}"  #{'Effect','Resource'}

#path2 = '/items'

file = sys.argv[1]
path = sys.argv[2] 

jsonquery(file,path)



