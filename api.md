# API SoLanches 

API do projeto SoLanches que oferece funcionalidades CRUD de um sistema de comércios do ramo alimentício. 

## Consulta status do servidor da API

Retorna um JSON com informações sobre o servidor.

```
GET /status
```

Exemplo

```
curl http://api/status
```

Resposta

```
Status: 200 OK
```
```
{
    "service": "API-SoLanches",
    "started_at": 1598458984,
    "status": "operacional",
    "timestamp": 1598485633
}
```

## Cadastra o comércio

Cadastra um comércio no banco de dados. Um comércio é formado por um JSON com os campos nome, do tipo string, e attributes, do tipo dict, que possui o campo telefone como obrigatório. Ambos os campos, nome e attributes, são obrigatórios. 

```
POST /comercio
```

Exemplo

```
curl \
    -d '{
             "nome": "lanche_feliz",
             "attributes": {
                 "telefone": "123456"
             }
         }' \
    -H "Content-Type: application/json" \
    -X POST http://api/comercio
```

Resposta

```
Status: 201 CREATED
```
```
{
    "id": "3671361e6d5dc1ee674156beed67b1fd",
    "attributes": {
         "telefone": "123456"
    },
    "cardápio": "3671361e6d5dc1ee674156beed67b1fd",
    "created_at": 1628721657.488885,
    "nome": "lanche_feliz"
}
```

Exemplo

```
curl \
    -d '{
             "nome": "lanche_feliz"
         }' \
    -H "Content-Type: application/json" \
    -X POST http://api/comercio
```

Resposta

```
Status: 400 BAD REQUEST
```
```
{
   "message": "Erro: atributos não informados",
   "status_code" : 400
}
```

## Lista comércios 

Retorna uma lista com todos os comércios cadastrados no sistema.

```
GET  /comercios
```

Exemplo

```
curl http://api/comercios
```

Resposta

```
Status: 200 OK
```
```
[
    {
        "id": "3671361e6d5dc1ee674156beed67b1fd",
        "attributes": {
             "telefone": "123456"
        },
        "cardápio": "3671361e6d5dc1ee674156beed67b1fd",
        "created_at": 1628721657.488885,
        "nome": "lanche_feliz"
    }
]
```

## Retorna um comércio por id

Recupera um comércio pelo id. O id é passado na URL e o retorno é um JSON com o comércio recuperado.

```
GET /comercio?id=
```

Exemplo

```
curl http://api/comercio?id=3671361e6d5dc1ee674156beed67b1fd
```

Resposta

```
Status: 200 OK
```
```
{
    "id": "3671361e6d5dc1ee674156beed67b1fd",
    "attributes": {
         "telefone": "123456"
    },
    "cardápio": "3671361e6d5dc1ee674156beed67b1fd",
    "created_at": 1628721657.488885,
    "nome": "lanche_feliz"
}
```

Exemplo

```
curl http://api/comercio?id=123
```

Resposta

```
Status: 400 BAD REQUEST
```
```
{
   "message": "Erro: comércio com id 123 não cadastrado!",
   "status_code" : 400
}
```

## Retorna comércio por nome

Recupera um comércio a partir do nome passado na URL.

```
GET /comercio/<comercio_nome>
```

Exemplo

```
curl http://api/comercio/lanche_feliz
```

Resposta

```
Status: 200 OK
```
```
{
    "id": "3671361e6d5dc1ee674156beed67b1fd",
    "attributes": {
         "telefone": "123456"
    },
    "cardápio": "3671361e6d5dc1ee674156beed67b1fd",
    "created_at": 1628721657.488885,
    "nome": "lanche_feliz"
}
```

## Cadastra produto no cardápio de um comércio

Para realizar o cadastrado de um produto no cardápio de um comércio, a requisição deve enviar no body um JSON com o campo `nome`, que é obrigatório, e o campo `attributes`, que é opcional. O `nome` do produto deve ser uma string e os `attributes` um dict.

```
POST /comercio/<comercio_nome>/produto
```

Exemplo

```
curl \
    -d '{
             "nome": "produto"
         }' \
    -H "Content-Type: application/json" \
    -X POST http://api/comercio/lanche_feliz/produto
```

Resposta

```
Status: 201 CREATED
```
```
{
   "message": "Produto com o id c3h2foe6di3e1ee6bd3ctb4r adicionado!",
}
```

Exemplo

```
curl \
    -d '{
             "nome": "produto"
         }' \
    -H "Content-Type: application/json" \
    -X POST http://api/comercio/abc_da_xuxa/produto
```

Resposta

```
Status: 400 BAD REQUEST
```
```
{
   "message": "Erro: comércio com nome abc_da_xuxa não cadastrado!",
   "status_code" : 400
}
```

## Adiciona um produto aos destaques do cardápio

Para adicionar um produto aos destaques, a requisição deve enviar no body um JSON com o campo `destaques`, que é obrigatório. Além disso, este mesmo produto já deve está cadastrado no cardápio do comércio.  

```
POST /comercio/<comercio_nome>/destaques
```

Exemplo

```
curl \
    -d '{
             "destaques": ["c3h2foe6di3e1ee6bd3ctb4r"]
         }' \
    -H "Content-Type: application/json" \
    -X POST http://api/comercio/lanche_feliz/destaques
```

Resposta

```
Status: 201 CREATED
```
```
{
   "message": "destaques adicionados!",
}
```

Exemplo

```
curl \
    -d '{
             "destaques": ["1234"]
         }' \
    -H "Content-Type: application/json" \
    -X POST http://api/comercio/lanche_feliz/destaques
```

Resposta

```
Status: 400 BAD REQUEST
```
```
{
   "message": "Erro: produto precisa fazer parte do cardápio do comércio",
   "status_code" : 400
}
```

## Recupera o cardápio de um comércio

Retorna o cardápio de um comércio, com os produtos e os destaques cadastrados.

```
GET /comercio/<comercio_nome>/cardapio
```

Exemplo

```
curl http://api/comercio/lanche_feliz/cardapio
```

Resposta

```
Status: 200 OK
```
```
{
    "id": "3671361e6d5dc1ee674156beed67b1fd",
    "created_at": 1628721657.488885,
    "destaques": ["c3h2foe6di3e1ee6bd3ctb4r"],
    "produtos": ["c3h2foe6di3e1ee6bd3ctb4r"]
}
```

Exemplo

```
curl http://api/comercio/abc_da_xuxa/cardapio
```

Resposta

```
Status: 400 BAD REQUEST
```
```
{
   "message": "Erro: comércio com nome abc_da_xuxa não cadastrado!",
   "status_code" : 400
}
```

## Deleta produto por id

Deleta produto do cardápio de comércio. O nome do comércio e o id do produto são passados na URL.

```
DELETE /comercio/<comercio_nome>/produto/<id_produto>
```

Exemplo

```
curl http://api/comercio/lanche_feliz/produto/c3h2foe6di3e1ee6bd3ctb4r
```

Resposta

```
Status: 200 OK
```
```
{
    "id": "3671361e6d5dc1ee674156beed67b1fd",
    "created_at": 1628721657.488885,
    "destaques": [],
    "produtos": []
}
```

Exemplo

```
curl http://api/comercio/lanche_feliz/produto/b1cef4d8hb611df8c443a1
```

Resposta

```
Status: 400 BAD REQUEST
```
```
{
   "message": "Erro: produto precisa fazer parte do cardápio do comércio",
   "status_code" : 400 
}
```