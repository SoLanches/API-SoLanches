# API SoLanches 

Esta API oferece funcionalidades CRUD de um sistema de comércios do ramo alimentício. 

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

Cadastra um comércio no banco de dados. Um comércio é formado por um JSON com os campos nome, do tipo string, e attributes, do tipo JSON. Ambos campos são obrigatórios. 

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

Lista todos comércios cadastrados no banco. A resposta é um JSON com todos os comércios do banco de dados.

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

## Lista comércio por id

Busca um comércio pelo id. O id é passado na URL, não pode ser nulo e deve ser uma string. O retorno é um JSON com o comércio recuperado.
```
GET /comercio?<id>
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

## Lista comércio por nome

Retorna um JSON com o comércio de nome equivalente ao que foi passado na URL. O nome do comércio passado não pode ser nulo e deve ser do tipo string.

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

Exemplo

```
curl http://api/comercio/abc_da_xuxa
```

Resposta

```
Status: 400 BAD REQUEST
```
```
{
   "message": "Erro: comércio de nome abc_da_xuxa não cadastrado!",
   "status_code" : 400
}
```

## Cadastra produto no comércio

Retorna um JSON informando que o produto foi cadastrado. O nome do comércio é passado na URL; não pode ser nulo e deve ser do tipo string. Já no body, deve ser passado o produto: um JSON com dois campos: nome e attributes, sendo este último, opcional. Nome deve ser do tipo string e attributes do tipo dict.

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

## Adiciona destaques (produtos) ao cardápio 

Retorna um JSON informando que o produto foi adicionado na lista de destaques. O nome do comércio é passado na URL; não pode ser nulo e deve ser do tipo string. Já no body, deve ser passado o destaque: um JSON com apenas um atributo chamado _destaques_, sendo este uma lista de strings; essas strings são os id's dos produtos. O(s) produto(s) já deve estar cadastrado no cardápio do comércio.

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

Retorna um JSON com os destaques e os produtos, entre outros campos, pertencentes àquele comércio. O nome do comércio passado na URL não pode ser nulo e deve ser uma string.

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
Status: TODO
```
```
{
   "message": "TODO",
   "status_code" : TODO
}
```

## Deleta produto por id

Deleta produto do cardápio de comércio. O nome do comércio e o id do produto, ambos passado na URL, não podem ser nulos e devem ser uma string.

```
DELETE /comercio/<comercio_nome>/produto/<id_produto>
```

Exemplo

```
curl http://api/comercio/lanche_feliz/produto/c3h2foe6di3e1ee6bd3ctb4r
```

Resposta

```
Status: 201 CREATED
```
```
{
    "message": "Produto com o id c3h2foe6di3e1ee6bd3ctb4r removido!
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





