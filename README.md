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
from json_path import JsonQuery
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





## Sitaxis

La jerarquía de elementos en JSON está sparada por el simbolo "/".


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

Return:     { "valor": 1000 }

Consulta:   /a  

Return:    { "b": { "valor": 1000 }}

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

Return:    { "name" : "a", "valor" : 1000 }

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

