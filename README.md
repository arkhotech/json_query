# JSON Query

(python)

### Sitaxis

La jerarquía de elementos en JSON está sparada por el simbolo "/".


**[/NODE_NAME]+**

Donde:

NODE_NAME : NAME[INDICE]*[QUERY]*

NAME: Secuencia de caracteres "a-z A-Z _"

INDICE: DIGITO+:DIGITO*

DIGITO: 0-9

QUERY: OPERACION [ OPERADOR OPERACION ]*

OPERACION: OPERANDO COMPARADOR OPERANDO

OPERANDO: FIELD | VALUE

FIELD:  @NAME 

VALUE: 'STRING' | INTEGER

COMPARADOR: == | != | > | < | <= | >= | in | notin

OPERACION:  and | or

Ejemplos:

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

