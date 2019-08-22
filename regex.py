import re

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


query = "fn:exist(@test) and @campo == 'algop' and fn:count(@test)== 1" #or @algo in data and @test!=2 or 2>@valor"

operations = re.compile(r'[@\w\'\d]+[(==)(!=)(>)(<)(<=)(>=)]+[@\w\'\d]+')

logical = re.compile(r'[or|and]+')

function = re.compile(r'fn\:[\w]+\([\w@]+\)')

operator = re.compile(r'[(==)(!=)(>)(<)(<=)(>=)]+')

operando = re.compile(r'[@\w\'\d]+')

op_sppliter = re.compile(r'[==|!=|>|<|>=|<=]')

#primer paso es hacer el corte por espacios
#noramlizar
query = query.replace('and','|and|').replace('or','|or|')
query = "".join(query.split())


class ProcessQuery(object):


	def __init__(self):
		pass


	def parseQuery(self,query):
		phase1 = self.__processPhase1(query)
		phase2 = self.__processPhase2(phase1)
		phase3 = self.__processPhase3(phase2)
		return phase3

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
				fase1.append({'type' : 'operation' , 'value' : item })
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
		fase3 = [],	idx = 0
		while idx < len(fase2):
			if fase2[idx]['type'] is 'function':
				fase3.append(
					{
					"function" : fase2[idx]['value'],
					"logical"  : fase2[idx+1]['value'] if (idx + 1) < len(fase2) else None
					}

					)
				idx += 2 
				continue
			fase3.append({
			 	"operando1": fase2[idx]['value'],
			 	"operacion": fase2[idx+1]['value'],
			 	"operando2": fase2[idx+2]['value'],
			 	"logical": fase2[idx+3]['value'] if (idx + 3) < len(fase2) else None,
			 	})
			idx += 4
		return fase3


query = ProcessQuery()

print(query.parseQuery(query))
