# Status code 200

## Status do servidor da API
```
GET /status
```

**Exemplo**
```
curl http://api/status
```

Resposta
```
Status: 200 OK
```

## Lista comércios
```
GET /comercios
```

**Exemplo**
```
curl http://api/comercios
```

Resposta
```
Status: 200 OK
```

## Retorna comércio por id
```
GET /comercio?id=
```

**Exemplo**
```
curl http://api/comercio?id=f397fbf5ae545af344549fbcf5623f8c042d369a
```

Resposta
```
Status: 200 OK
```

## Retorna comércio por nome
```
GET /comercio/<nome_comercio>
```

**Exemplo**
```
curl http://api/comercio/lanche_bom
```

Resposta
```
Status: 200 OK
```

**Exemplo**

Se o nome do comércio for um espaço em branco.
```
curl http://api/comercio/ 
```

Resposta
```
Status: 200 OK
```

## Recupera o cardápio de um comércio
```
GET /comercio/<comercio_nome>/cardapio
```

**Exemplo**

```
curl http://api/comercio/lanche_bom/cardapio
```

Resposta
```
Status: 200 OK
```

## Deleta produto por id
```
DELETE /comercio/<comercio_nome>/produto/<id_produto>
```

**Exemplo**
```
curl http://api/comercio/lanche_feliz/produto/3a7a5982a01608064a597a4857ec2a10e464365a
```

Resposta
```
Status: 200 OK
```

# Status code 201

## Cadastra comércio
```
POST /comercio
```

**Exemplo**
```
curl \
    -d '{
             "nome": "lanche_bom",
			 "attributes": {
				 "telefone": "13123"
				 }
         }' \
    -H "Content-Type: application/json" \
    -X POST http://api/comercio
```

Resposta
```
Status: 201 CREATED
```

## Cadastra produto no cardápio de um comércio
```
POST /comercio/<comercio_nome>/produto
```

**Exemplo**
```
curl \
    -d '{
             "nome": "empanado_de_frango",
             "attributes": {
				 "peso": "70g"
				 }
         }' \
    -H "Content-Type: application/json" \
    -X POST http://api/comercio/lanche_feliz/produto
```

Resposta
```
Status: 201 CREATED
```

**Exemplo**

Produto com campo ``attributes`` vazio.
```
curl \
    -d '{
             "nome": "empanado_de_frango",
             "attributes": {}
         }' \
    -H "Content-Type: application/json" \
    -X POST http://api/comercio/lanche_feliz/produto
```

Resposta
```
Status: 201 CREATED
```

**Exemplo**
```
curl \
    -d '{
             "nome": "empanado_de_frango"
         }' \
    -H "Content-Type: application/json" \
    -X POST http://api/comercio/lanche_feliz/produto
```

Resposta
```
Status: 201 CREATED
```

**Exemplo**

Qualquer outro campo passado, juntamente com o campo ``nome``, será aceito.
```
curl \
    -d '{
             "nome": "empanado_de_frango",
             "preco": 2.50
         }' \
    -H "Content-Type: application/json" \
    -X POST http://api/comercio/lanche_feliz/produto
```

Resposta
```
Status: 201 CREATED
```


# Status code 400

## Cadastra o comércio
```
POST /comercio
```

**Exemplo**

Caso o campo ``nome`` não esteja presente.
```
curl \
    -d '{
             "attributes": {
			     "telefone": "123456"
			      }
         }' \
    -H "Content-Type: application/json" \
    -X POST http://api/comercio
```

Resposta
```
Status: 400 BAD REQUEST
```

**Exemplo**

Campo ``attributes`` vazio.
```
curl \
    -d '{
             "nome": "lanche_feliz",
		     "attributes": {}
         }' \
    -H "Content-Type: application/json" \
    -X POST http://api/comercio
```

Resposta
```
Status: 400 BAD REQUEST
```

## Retorna comércio por id
```
GET /comercio?id=
```

**Exemplo**

Caso seja passado um ``id`` inexistente.
```
curl http://api/comercio?id=0811fc9a
```

Resposta
```
Status: 400 BAD REQUEST
```

## Retorna comércio por nome
```
GET /comercio/<nome_comercio>
```

**Exemplo**
```
curl http://api/comercio/lanche_delicioso
```

Resposta
```
Status: 400 BAD REQUEST
```

## Cadastra produto no cardápio de um comércio
```
POST /comercio/<comercio_nome>/produto
```

**Exemplo**

Caso tente cadastrar um produto em um comércio inexistente.
```
curl \
    -d '{
             "nome": "empanado_de_carne"
         }' \
    -H "Content-Type: application/json" \
    -X POST http://api/comercio/lanche_gostoso/produto
```

Resposta
```
Status: 400 BAD REQUEST
```

## Adiciona um produto aos destaques do cardápio
```
POST /comercio/<comercio_nome>/destaques
```

**Exemplo**

Destaque inexistente. 
```
curl \
    -d '{
			 "destaques": ["id"]
         }' \
    -H "Content-Type: application/json" \
    -X POST http://api/comercio/lanche_feliz/destaques
```

Resposta
```
Status: 400 BAD REQUEST
```

**Exemplo**

Destaque vazio.
```
curl \
    -d '{
			 "destaques": []
         }' \
    -H "Content-Type: application/json" \
    -X POST http://api/comercio/lanche_feliz/destaques
```

Resposta
```
Status: 400 BAD REQUEST
```

## Recupera o cardápio de um comércio
```
GET /comercio/<comercio_nome>/cardapio
```

**Exemplo**

Comércio com nome inexistente.
```
curl http://api/comercio/lanche_gostoso/cardapio
```

Resposta
```
Status: 400 BAD REQUEST
```

## Deleta produto por id
```
DELETE /comercio/<comercio_nome>/produto/<id_produto>
```

**Exemplo**

Caso o comércio não exista.
```
curl http://api/comercio/lanche_gostoso/produto/3a7a5982a01608064a597a4857ec2a10e464365a
```

Resposta
```
Status: 400 BAD REQUEST
```

**Exemplo**

Caso o produto não exista no cardápio.
```
curl http://api/comercio/lanche_feliz/produto/3aid7a5id43id65a
```

Resposta
```
Status: 400 BAD REQUEST
```

**Exemplo**

O comércio e o produto existem, mas o produto não está cadastrado no cardápio desse comércio.
```
curl http://api/comercio/lanche_bom/produto/836d9e3d8f9cb5be7772ab7eb6f4ef41155c1bab
```

Resposta
```
Status: 400 BAD REQUEST
```

# Status code 500

## Adiciona um produto aos destaques do cardápio
```
POST /comercio/<comercio_nome>/destaques
```

**Exemplo**

Caso o campo ``destaques`` não exista.
```
curl \
    -d '{
			 "campo_qualquer": ["3a7a5982a01608064a597a4857ec2a10e464365a"]
         }' \
    -H "Content-Type: application/json" \
    -X POST http://api/comercio/lanche_feliz/destaques
```

Resposta
```
Status: 500 INTERNAL SERVER ERROR
```