<img src="https://www.arkho.tech/wp-content/uploads/2019/06/Logo_Cloudready.jpg" width="400px"/>

# JSON Query

## Estado: PROTOTIPO
#### AUTHOR: Marcelo Silva
#### Lenguaje:  Python


### Instalación

Con el cliente GIT clonar el repositorio desde:
```bash
git clone https://gitlab.com/arkhotech/json_query.git
```

Una vez clonado el repositorio, para poder utilizar la librería solo se debe agregar el siguiente import:

```python
from jsonquery import JsonQuery
```

Esta librería posee solo una Clase llamada **JsonQuery** que es la que hace el trabajo de generar las consultas dentro de un archivo JSON.
La clase necesita 2 parametros:

```python
query = JsonQuery(query,data)
```

* **query**: Consulta json (ver sintaxis)
* **data**:  json o un objeto de tipo 'dict'

Ejemplo completo:

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

Como función:

```python

from jsonquery import jsonquery

jsonquery('archivo.json','/item[0]/items[@id=='1001']
```


## Sitaxis

La sintaxis de las consultas se dividen en 3 partes:

* path
* select
* query

####PATH

El path repsenta los niveles en forma dentro de un archivo Json . Cada nivel es separado por un '/'. Ej:

```json
{
	"nivel1": {
		"nivel2": {
			"nivel3": "hola"
		}
	}
}
```
Una consulta como:  /nivel1/nivel2/nivel3, debería retornar "hola".

## Arrays

Si el archivo JSON contiene un array, el path puede especificar un indice de item dentro del JSON, ej:

> **NOTA:** Lo números para indice tienen base "0".
> 
> **NOTA2:** La ejecución de la consulta, retorna una lista con resultados, si el resultado es un valor de un item en JSON. Si es una array o el resultado retorna mas de un valor, se retornará un List. 


Tomando como ejemplo el siguiente JSON:

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
| /items/items[15] | Este recupera el item número 16 | **[{ "item": 16}]** |
| /items/items[0]/item | Recupera el valor del item 1 |  **1** |
| /items/items[n+1] | Arroja un error de indice fuera de rango |**Error**|

#### Nodo Raíz

Para especificar el nodeo raíz en una consulta, se debe especificar el '/' al principio. Si no va un '/' al principio, se busca todas las concidencias en cualquier parte del JSON. Ej.

Para el mismo ejemplo anterior, una consulta del tipo:  'item':

```json
[
	{ "item": 1},
	{ "item": 3},
	....
	{ "item": N}
]
```

## select

Se puede seleccionar (por ahora) los campos de un item JSON que se quieren retonar, agreando lo nombres de los campos que se requieren entre corchetes:  **{ 'FIELD-1', 'FIELD-2', ... 'FIELD-N' }**

Ej: Para el siguiente JSON:

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

Si ejecutamos:  **/items[0]{ 'id','name'}**
El resultado sería:

```python
>>> from jsonquery import *
>>> jsonquery('archivo.json','items[0]{ 'id','name'}')

{
	"id": "7003",
	"name": "Whipped Cream"
}
```

### Query

Uno de los selectores mas importantes es la Query. Esta actúa como un filtro sobre un item dentro de un dataset (json).  Donde se aplica el filtro, solo se seleccionan los subnodos que cumplna con la condición:

### Sintaxis

```python
[ OPERACION { OPERADOR OPERACION } { OPERADOR OPERACION } ]

operación:  field comparador valor
```
Donde:
* **OPERCION**:  Es una operacion bunaria con 2 operandos mas un comparador.
* **OPERADOR**: es una operación lógica que puede ser "and" u "or".

Ejemplo

```python
>>> from jsonquery import *
>>> path = '/item/items[@valor >= 1000 and @valor <= 10000]'
>>> 
>>> jsonquery('archivo.json',path)

```

#### Operandos

Los operandos son valores que se pueden comparar y sirven de filtro para la consulta. Los operandos pueden ser valores interos, float, string o de tipo "Field". Ej de operandos:

```
@id == 1000
```

Los operandos en el caso anterior son @id y 1000. Mientras que el símbolo "==" (ver comparadores es el comparador.

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

#### Comparadores

Los comparadores peremitidos de una operación son:

| Comparador| Descripción|
|-----------|------------|
| == | Este es el comparador de igualdad. En el caso de comparar contra un Array, actua como 'IN'|
| != | Distinto o no igual a. Sobre un array actua como un 'NOT IN'|
| > , <, <= , >= | Comparadores de desigualdad. Solo aplica con  valores integer, float.

#### Comparar con array

Cuando el valor se compara con un array, entonces la operación "==" o "!=" actúan como "in" y "not in" respectivamente. Ej.

Para el siguiente JSON:

```json
{
	"valor" : [2,3,4,5,6],
	"valor" : [5,6,7]
}
```

La sigiente operación:

```python
>>> from jsonquery import *
>>> 
>>> jsonquery('archivo.json','/[@valor==5]')
>>> 
{ "valor": [2,3,4,5,6] }

```
En el vaso anterior se selecciona el primer array por que contiene el número 5.  En caso contrario:

```python 
>>> from jsonquery import *
>>> 
>>> jsonquery('archivo.json','/[@valor!=5]')
>>> 
{ }

```
En el caso anterior, retorna vacio ya que el 5 esta presente en ambos items.


#### Orden de precedencia

Las operaciones se realizan desde deracha a izquierda.

```
[ @id=='1001' and @type=='té' or @type=='cafe']
```

En el caso anterior el orden de ejecución es:

(@id=='1001' and @type=='té' ) or @type=='cafe'

La interscciín de las operaciones @id=='1001' y @type=='té'.  El resultado es la únion de los valores de la primera operación con el resultado de la tercera operación (a excepción de los valores repetidos).




---



**[/NODE_NAME]+**

Donde:

**NODE_NAME** : *NAME*[*INDICE*]\*[*QUERY*]\*

**NAME**: Secuencia de caracteres "a-z A-Z _"

**INDICE**: *DIGITO*+:*DIGITO*\*

**DIGITO**: 0-9

**QUERY**: *OPERACION* [ *OPERADOR* *OPERACION* ]\*  (***Los espacios son requeridos***)

**OPERACION**: *OPERANDO* *COMPARADOR* *OPERANDO*

**OPERANDO**: *FIELD* | *VALUE*

**FIELD**:  @*NAME* (**el @ es literal**) 

**VALUE**: 'STRING' | INTEGER

**COMPARADOR**: *== | != | > | < | <= | >= | in | notin*

**OPERACION**:  *and | or*

----

#### Ejemplos:

Tomando el siguiente JSON

```json
{
   "a" : {
      "b" : {
	"valor" : 1000	
      }		

   }

}

```

Se pueden ejecutar los siguientes consultas:

```
Consulta:   /a/b

Return:     [{ "valor": 1000 }]

Consulta:   /a  

Return:    [{ "b": { "valor": 1000 }}]

Consulta:  /a/b/valor

Return:    1000

```

Se pueden seleccionar elementos directamente a través de su número de indice si se trata de un array:

```json

{ "a" : { "b" : [ { "name" : "a", "valor" : 1000 },{"name" : "b","valor" :2000},{"name" : "c","valor": 3000}]}}
```

Consultas:

```
Consulta:  /a/b[0]

Return:    [{ "name" : "a", "valor" : 1000 }]

Consulta: /a/b[2]

Return:   [{"name" : "c","valor": 3000}]

(Aún no implementado)

Consulta:  /a/b[0:2]

Return:  [ { "name" : "a", "valor" : 1000 },{"name" : "b","valor" :2000},{"name" : "c","valor": 3000}]

```

Query sobre un set.

Adicionalmente se pueden realizar consultas sobre el set de datos de un nodo seleccionado. Para esto se debe agrega la consulta dentro de parantesis cuadrados y estos seleccionan items que puede contner el nodo filtrando por los criterios que se deseen utilizar.

Ej:   /a/b[ @valor == 1000 ]

El ejemplo anterior aplica la consulta sobre cada item de "B" que tenga el campo "valor" igual a 1000. El simbolo @hace referencia a un campo sobre el nodo o el valor de un alista dentro del nodo, en este caso el nodo B

Ej:  /a/b[ @valor >= 1000 and @valor < 3000 ]

Este ejemplo retorna todos los valores dentro del array en el nodo b que tengan como valor en la propiedad "valor", valores mayores o iguales a 1000 y menores a 3000. El resultado debería ser el siguiente:

```javascript
[ { "name" : "a", "valor" : 1000 },{"name" : "b","valor" :2000}]
```
