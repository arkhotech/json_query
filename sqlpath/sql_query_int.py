import re

sql = r'SELECT\s+[(\*)|(\w)+(\s+,\w+)*]+\s+FROM\s+[/\w]+[/\w]*\s+WHERE\s+'

def parseSQL(text):
	parts = re.split('FROM',text,flags=re.IGNORECASE)
	select = parts[0].replace('SELECT','')
	print(parts[1])
	where = re.split('WHERE',parts[1],flags=re.IGNORECASE)
	print(select)
	_from = where[0]
	print(where[1])
	print(_from)
	


parseSQL('SELECT a,b,c FROM /a/b/c WHERE item==5')