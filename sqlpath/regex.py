import re
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("regex")
q = '@test==1'
#print(re.compile(r'[==|!=|>|<|>=|<=]').split(q))


class Control(object):

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



operations = re.compile(r'[@\w\'\d]+[(==)(!=)(>)(<)(<=)(>=)]+[@\w\'\d]+')

logical = re.compile(r'[or|and]+')

function = re.compile(r'fn\:[\w]+\([\w@]+\)')

operator = re.compile(r'[(==)(!=)(>)(<)(<=)(>=)]+')

operando = re.compile(r'[@\w\'\d]+')

op_sppliter = re.compile(r'[==|!=|>|<|>=|<=]')

#primer paso es hacer el corte por espacios
#noramlizar
"""

"""
def seekParentesisGroup(text,exp):

	def findParentesisPairs(text,exp,idx=0):

		logger.debug('call')
		op = False
		lst =[]
		a  = 0
		inner = None
		while idx < len(text):

			if text[idx] == '(' and idx not in exp:
				if op:
					logger.debug('Inside: ' + str(idx))
					idx, l = findParentesisPairs(text,exp,idx)
					lst += l
					logger.debug('Return: ' + str(idx))
				else:
					logger.debug('Open: ' + str(idx))
					a = idx
					op = True
					idx += 1
				continue

			if text[idx] ==')' and idx not in exp and op:
				logger.debug('Close: ' + str(idx))
				op = False
				lst.append((a,idx))
				idx +=1
				break
			else:
				idx += 1
		return idx, lst
	#Recorre la cadena completa
	idx = 0 
	result =[]
	while idx < len(text):
		idx, r = findParentesisPairs(text,exp,idx)
		logger.debug(r)
		result+= r

	return result

def identifyFuncParentesis(text):
	def seekBracketsPair(text,idx):
		logger.debug('call:')

		op = cl = fx = False
		exp = []
		while idx < len(text):
			if text[idx:idx+3] == 'fn:':
				logger.info('fn:')
				if fx:  #si es open, busca nuevamente
					idx, l = seekBracketsPair(text,idx)
					exp += l
				else:
					op = fx = True

			if text[idx] == '(' and op:
				op = False
				cl = True
				exp.append(idx)
				logger.debug('open:' + str(idx))

			if text[idx] == ')' and cl:
				logger.debug('close: ' + str(idx))
				exp.append(idx)
	 
				cl = False
				return idx + 1, exp
			idx += 1
		return idx, exp

	idx = 0
	result =[]
	while idx < len(text):
		idx , res = seekBracketsPair(text,idx)
		logger.debug(idx)
		result += res
	return result



class ProcessQuery(object):


	def __init__(self):
		pass


	def parseQuery(self,query):
		logger.info(query)
		query = query.replace('and','|and|').replace('or','|or|')
		#query = "".join(query.split())
		phase0 = self.__processPhase0(query)
		#lista en grupos
		logger.info(phase0)
		quit()
		phase1 = self.__processPhase1(phase0)
		phase2 = self.__processPhase2(phase1)
		phase3 = self.__processPhase3(phase2)
		return phase3

	def __processPhase0(self,query):

		#Esto paerentecis no se proceosan
		exp = seekFunctions(query)
		logger.info(exp)
		lista=[]
		re = parseParen(query,lista,exp)
		re.reverse()
		logger.info(re)
		quit()
		return re
		#normalizar la precedencia

	def __expandOperation(self,item):
		
		retval = []
		operations = list(filter(lambda x : x if len(x) > 0 else x, \
		 re.compile(r'[==|!=|>|<|>=|<=]').split(item['value'])))

		retval.append({'type': 'operando ', 'value' : operations[0] })
		r1 = item['value'].replace(operations[0],'')
		op = r1.replace(operations[1],'')
		retval.append({'type' : 'operator' , 'value' : op })
		retval.append({'type': 'operando ', 'value' : operations[1] })
		return retval

	#ahora la organizacion es operaciones & logical

	def __processPhase1(self,query):
		phase1 = []
		selectors = re.compile(r'\|').split(query)
		for item in selectors:

			if function.match(item):
				phase1.append({'type' : 'function', 'value': item})
				continue

			if logical.match(item):
				phase1.append({'type' : 'logical', 'value': item})
			else:
				phase1.append({'type' : 'operation' , 'value' : item })
		return phase1


	#normalizar otdas las operaciones
	#Ok

	def __processPhase2(self,phase1):
		phase2 = []
		for item in phase1:
			if item['type'] is 'operation':
				result = self.__expandOperation(item)
				list(map(lambda x : phase2.append(x), result))
			else:
				phase2.append(item)
		return phase2


	def __processPhase3(self,phase2):
		#for idx in range(0,len(fase2)-1,4):
		fase3 = []
		idx = 0
		while idx < len(phase2):
			if phase2[idx]['type'] is 'function':
				fase3.append(
					{
					"function" : phase2[idx]['value'],
					"logical"  : phase2[idx+1]['value'] if (idx + 1) < len(phase2) else None
					}

					)
				idx += 2 
				continue
			fase3.append({
			 	"operando1": phase2[idx]['value'],
			 	"operacion": phase2[idx+1]['value'],
			 	"operando2": phase2[idx+2]['value'],
			 	"logical": phase2[idx+3]['value'] if (idx + 3) < len(phase2) else None,
			 	})
			idx += 4
		return fase3


def indetifyFunctionsParentesis(text,idx):
	logger.info('identifyParantesis')
	logger.info('id: ' + str(idx))
	i = idx
	_close = False
	_open = False
	pos = []
	while i < len(text):

		if text[i:i+3] == 'fn:':
			logger.info('fn:' + str( i))
			i, l = indetifyFunctionsParentesis(text,i+1)
			pos += l
			continue
			
		if text[i] == '(' and _open: 
			logger.info('open: ' + str(i))
			_open = False
			_close = True 
			pos.append(i)

		if text[i] == ')' and _close: 
			logger.info('close: ' + str(i))
			logger.debug(pos)
			logger.debug('-------------------')
			_close = False
			pos.append(i)
			
			return i + 1, pos 
		i += 1
	return i, pos

#print(indetifyFunctionsParentesis(test,0))

# print(seekFunctions(text))


# print(seekFunctions('xxxxxx'))

# print(seekFunctions('fn:test(fn:test(a))'))  #7,15,17,18
					#0123456789012345678

test1 = "(@field = x and fn:exist(@field2)) or (@campo == 'algop' and fn:count(@test)== 1)"
#        012345678901234567890123456789012345678901234567890123456789012345678901234567890
#                 10        20        30        40        50        60        70 
test = "(fn:exist(fn:counr(@test)) and fn:count(x))" # and @campo == 'algop') and fn:count(@test)== 1"
#       0123456789012345678901234567890123456789012345678901234567890123456789012
#                 10        20        30        40        50        60        70 

query = "fn:exist(@test) and @campo == 'algop' and fn:count(@test)== 1" #or @algo in data and @test!=2 or 2>@valor"


test2 = "( a = 2 and ( a or b) ) or ( fn:exist(a) )"
#        0123456789012345678901234567890123456789012345678901234567890123456789012
#                 10        20        30        40        50        60        70 
test3 = "( @f == '5' and ( @b == 1 or @b ==2) )"


 
def phase0(text):

	ex = identifyFuncParentesis(text)
	logger.info(ex)
	groups = seekParentesisGroup(text,ex) #0-8 , 6-7, 9-10

	#clasificar los grupos, revisar los iner barcked

	groups.sort(key = lambda x : x[0])
	logger.info(groups)

	#CRear estrucutra
	#                     01234567890123456789012345
	i = 1
	cursor = 0
	lista = []
	for group in groups:
		print(group)
		start,end = group
	
		conj = text[cursor:start]
		if conj != '':
			lista.append(conj)
		print('group' +str(i) +':' + text[start+1:end])
		lista.append(text[start+1:end])
		cursor = end + 1
		i+= 1
	return lista


l =  [ (0,10), (5,7) , (11,15) ]

while len(l) > 0:
	logger.info(l)
	l.pop()


x = "(op and ( op2 or op3 )) and ( op3 or op4 )"  # -->  grupo1 [ [ op , and , [ op2, or, op3 ] , and , [ op3 , or , op4] ]  


def 


#logger.info(phase0(test3))
