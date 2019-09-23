<img src="https://arkho.tech/wp-content/uploads/2019/08/logo.png" width="400px"/>

# JSON Query

## State: PROTOTYPE
#### AUTHOR: Marcelo Silva
#### Language:  Python


### Setup

Install application from GitHub using git client:

```bash
git clone https://gitlab.com/arkhotech/json_query.git
```

Once the repository is cloned we can use the library adding the following import:

```python
from jsonquery import JsonQuery
```
The library have two ways to use it, one way is usgin the class **JsonQuery. This class takes 2 parameters: the query and the json data on 'dict' object type. Ej.

```python
query = JsonQuery(query,data)
```

* **query**: Query applied over the data (see syntax).
* **data**:  'dict' object that contains the json data.

Example:

```python
from json_query import JsonQuery

import json
data = None
with open('test.json','r') as input:
   data = json.load(input)

jsonquery = JsonQuery("/a",data)
retval = jsonquery.execute()

print(retval)
```

The second way to use it is like a function. The module have got a function called jsonquery and you must declare the correct import. Ex.

```python

from jsonquery import jsonquery

jsonquery('archivo.json','/item[0]/items[@id=='1001']
```


## Syntax

The sytanx used for the query have got 3 parts:

* path
* select
* query

### PATH

The path represents every level on the Json in a single line separated trough the slash ('/') symbol. Ex:

```json
{
	"nivel1": {
		"nivel2": {
			"nivel3": "hola"
		}
	}
}
```

One query like this over the json example above:  **/nivel1/nivel2/nivel3**, must return the following  **"hola"**.

## Arrays

If the json contains some array dadta inside, you can specify the index of the item that you want, using a index number between bracket ( **[  ]** ).

> **NOTA:** The array have got 0 base index.
> 
> **NOTA2:** The query execution returns a list with result if the query return mora that one item or if the result is a json array otherwise return a json value.

Using the following JSON:

```json
{
   "lista":
        { "items": [
        	{ "item": 1},
        	{ "item": 3},
        	{ "item": 4},
        	.....
        	{ "item": N},
        ]
}
```

| query | descrición | resultado |
|-------|------------|-----------|
| /items/items[15] | Recover the item on 16th position | **[{ "item": 16}]** |
| /items/items[0]/item | Return the item value: 1 |  **1** |
| /items/items[n+1] | throws a error index out of range |**Error**|

### Root Node

On a query, the root node is representated with the slash symbol on the begining. If you don't especified the slash on the begin of the path query, the seek could select any node on the three wich match with the node name specified in the path query.  

Using the json above if we execute just the following query:  

'item'

We will get the following result:

```json
[
	{ "item": 1},
	{ "item": 3},
	....
	{ "item": N}
]
```

## select

You can use field selector if you don't want only especific fields from the requested json file. By use selector you must add a list of fields between curly bracket ( **{  }** ) separated with comes: 

```
  { 'FIELD-1', 'FIELD-2', ... 'FIELD-N' }
```

The field names must be inside "" or ''.

Example, if we execte the following query: Si ejecutamos:  **/items[0]{ 'id','name'}**

Over the following json:

```json
{ 
"items":{
	[   
		{
			"id": "7002",
			"name": "Custard",
			"addcost": 0
		},
		{
			"id": "7003",
			"name": "Whipped Cream",
			"addcost": 0
		},
		{
			"id": "7004",
			"name": "Strawberry Jelly",
			"addcost": 0
		},
		{
			"id": "7005",
			"name": "Rasberry Jelly",
			"addcost": 0
		}
	]}
}
```

The returned of the query will be:

```python
>>> from jsonquery import *
>>> jsonquery('archivo.json','items[0]{ 'id','name'}')

{
	"id": "7003",
	"name": "Whipped Cream"
}
```

### Query Filter

The must important part of the jsonquery sentence is the selector or filters.  We can filter what items will be selected according the criteria applied over the node. 
The selector are between square bracket ( **[  ]** ) and it must put over the end of the node name. Ex:

```
/nodename[ query ]
``` 

the query filter must be applied over the node child. You can mix the query filter with item index if the child of the current node where the query will be applied. Ex:

```
/nodename[15][ query ]
```

On the example above the query fileter must be applied over the item number 16 (remember that the first item index is 0).  

You could apply new query path over the result in the same query path. Ex.

```
/nodename[15][ query]/another-item
```
On the example above the query will be applied over the item 16  of the nodename and over the result, will be requested the node "another-item" and so on.

> **NOTE**: You must consider if the requested json node is an array or not for make a path quert over the result. You cannot get an unique particular node name over an array. The array return a list.


### Query filter Syntax


**[** *OPERATION* *[LOGIC_OPERATOR OPERATION]*+ **]**

Where:

* ***OPERATION***:  2 operands plus a mathematical comparator.
* ***LOGIC_OPERADOR***: Logic operation. You could use: **and, or**


Example:

```python
>>> from jsonquery import *
>>> path = '/item/items[@valor >= 1000 and @valor <= 10000]'
>>> 
>>> jsonquery('archivo.json',path)

```

#### Operands

The operands are values that you can use for filter values that accomplish with the condition. The operands must be a *field* and some value for perform the comparation. An field represents some name inside of the json file and you can map with a '**@**' before the name.

An operation must take an field, an comparator and a value. The value must be a string, integer, float or boolean. Ex:

```
@id == 1000
```

The field must be in the first place or to the left of the operation.

#### Field

representa el nombre de un campo dentro de un Json. El nombre debe comenzar con un simbolo '@'. Por ejemplo:  

```
# @id
# Este valor hace referencia al campo id del siguiente JSON:

{
	"id": 1000,
	"comantario": "Test"
}

```

#### Comparators

The permited comparators over an operation are:


| Comparator| Description|
|-----------|------------|
| == | Equals to. If you comparate agains an array value, equlas act as a 'IN' operation.|
| != | Not equal. Over an array acts as a 'NOT IN'|
| > , <, <= , >= | 
inequality . Only applied over integer and float values.|

#### Compare against array

When the value it's comparated against and array the simbols '==' and '!=' acts a IN and NOT IN operation respectively. Ex:

By the following JSON:

```json
{
	"valor" : [2,3,4,5,6],
	"valor" : [5,6,7]
}
```

And the following operation:

```python
>>> from jsonquery import *
>>> 
>>> jsonquery('archivo.json','/[@valor==5]')
>>> 
{ "valor": [2,3,4,5,6] }

```

On the example above it has slected the first array because it array comtains the number five. 
The opossite case, we can change the equal for not equal:

```python 
>>> from jsonquery import *
>>> 
>>> jsonquery('archivo.json','/[@valor!=5]')
>>> 
{ }

```

On the example above the returned value is a empty json because on both cases exists the number five in the array's

### Operations AND & OR

The operations **AND** performs a union of dataset with that accomplish with the conditions.

The **OR** logic conditions, performs a union of datasets that accomplish with our respective conditions. Both resulting dataset will be merged.

### Excution order

All of the operations are executed from left to rigth. Consider the following example:

```
[ @id=='1001' and @type=='té' or @type=='cafe']
```

* First will be executed the operation: ***(@id=='1001' and @type=='té' )*** 
* The previus result will be all values that have id equals to '1001' and type equals to 'te. The operation will be a intersection of both results.
* Then, will be executed the operation: **@type=='cafe'**
* The result of the previus operation will be merged with the first operation

## Syntax




---

|expresion|    |
|---------|----|
| ***QUERY_PATH*** | **[/*NODE_NAME*]+** |
| **NODE_NAME** | *NAME* **[** *INDEX* **]**\* **[** *QUERY* **]**\* |
| **NAME** | Sequence "a-z A-Z_0-9" |
| **INDEX** | *DIGIT*+:*DIGIT*\* |
| **DIGIT** | [0-9]+ |
| **QUERY** | *OPERATION* [*LOGIC_OPERATOR* *OPERATION*]\*  ( **the spaces are required ** ) |
| **OPERATION** | *OPERAND* *COMPARATOR* *OPERAND* |
| **OPERANDO** | *FIELD* | *VALUE* |
| **FIELD** | @*NAME* (**el @ es literal**) |
| **VALUE** | 'STRING' | INTEGER |
| **COMPARADOR** | ==, !=, >, <, <=, >= |
| **OPERACION** |  and \| or |

----

## Examples:

With the following Json

```json
{
   "a" : {
      "b" : {
	"valor" : 1000	
      }		

   }

}

```
You can execute the following querys:


```
Query:   /a/b

Return:     [{ "valor": 1000 }]

Query:   /a  

Return:    [{ "b": { "valor": 1000 }}]

Query:  /a/b/valor

Return:    1000

```

Select directly an item inside an array:

```json

{ "a" : 
   { "b" : [ 
       { "name" : "a", "valor" : 1000 },
       {"name" : "b","valor" :2000},
       {"name" : "c","valor": 3000}
       ]
   }
}
```

Querys over json:

```
Query:  /a/b[0]

Return:    [{ "name" : "a", "valor" : 1000 }]

Query: /a/b[2]

Return:   [{"name" : "c","valor": 3000}]

```
