import re
import logging
import pprint

logging.basicConfig(level=logging.INFO)

"""

Operando ->  operacion | funcion 


"""
field = re.compile(r'[@\w!=<>\'"]')

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



test = "(@field!='algo' and @field2<>7) or (@field3<>5 and ( @field4!=10 or @field5 != 0  or ( a==b and c==d )))"#    ) and (fn:count(test)"
#       01234567890123456789012345678
test2 = "@field!='algo'"

grps = groups(test)

print(grps)

logger = logging.getLogger("test")

group_plan = {}

newplan = []


pp = pprint.PrettyPrinter(depth=6)

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
		# for i in range(0,int(level)):
		# 	logger.info('------------')
		# 	pp.pprint(group)
		# 	if 'suboperacion' in  group:
		# 		logger.info('get')
		# 		group = group['suboperacion']
		# 	else:
		# 		logger.info('put')
		# 		group.append({ 'suboperacion' : plan} )
		
		logger.info('level: ' + str(level))
		group.append({ 'suboperacion' : plan} )
	else:
		group_plan.update ({ groupname : plan })


pp.pprint(group_plan)





