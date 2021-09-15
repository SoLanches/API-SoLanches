# **API SoLanches**

API do projeto [SoLanches](https://github.com/SoLanches) que oferece funcionalidades *CRUD* de um sistema de comércios do ramo alimentício. 

## Consulta status do servidor da API [GET]

Retorna um *JSON* com informações sobre o servidor.

+ URL

    ```
    GET /status
    ```

+ **Exemplo**

    + Request

        ```
        curl http://api/status
        ```

    + Response

        ```
        Status: 200 OK
        ```
        ```
        {
            "service": "api-solanches",
            "started_at": 1631664230.6867428,
            "status": "operacional",
            "timestamp": 1631664351.918028
        }
        ```

## Cadastra o comércio [POST]

Adiciona um comércio no banco de dados e retorna um *JSON* com o comércio adicionado. A requisição deve enviar no body um *JSON* com os campos `nome` e `attributes`, o último contendo obrigatoriamente os campos `endereco` e `horarios`.

+ URL

    ```
    POST /comercio
    ```

+ Body

    | Parameters | Type | Requirement | Description |
    |---|---|---|---|
    | `nome` | string | obrigatório | o nome do comercio.|
    | `attributes` | dict | obrigatório | as informações de cadastro do comércio.|
    | `endereco` | string | obrigatório | o endereço do comercio, no campo `attributes`.|
    | `horarios` | string | obrigatório | os horários do comercio, no campo `attributes`.|

+ **Exemplos**

    + Request

        ```
        curl \
            -d '{
                    "nome": "lanche_feliz",
                    "attributes": {
                        "endereco": "rua, numero - bairro - cidade/UF",
                        "horarios": "terça-feira - domingo, 17:00 - 23:00",
                        "categoria": "lanchonete"
                    }
                }' \
            -H "Content-Type: application/json" \
            -X POST http://api/comercio
        ```

    + Response

        ```
        Status: 201 CREATED
        ```
        ```
        {
            "id": "3671361e6d5dc1ee674156beed67b1fd",
            "attributes": {
                "endereco": "rua, numero - bairro - cidade/UF",
                "horarios": "terça-feira - domingo, 17:00 - 23:00",
                "categoria": "lanchonete"
            },
            "cardápio": "3671361e6d5dc1ee674156beed67b1fd",
            "created_at": 1628721657.488885,
            "nome": "lanche_feliz"
        }
        ```

    + Request

        ```
        curl \
            -d '{
                    "nome": "lanche_feliz"
                }' \
            -H "Content-Type: application/json" \
            -X POST http://api/comercio
        ```

    + Response

        ```
        Status: 400 BAD REQUEST
        ```
        ```
        {
            "message": "Erro: campo attributes não informado!",
            "status_code" : 400
        }
        ```

## Lista os comércios [GET]

Retorna uma lista com todos os comércios cadastrados no sistema, sendo também possível o retorno de um dicionário com o agrupamento dos comércios por categoria, onde as chaves do dicionário são as categorias e os valores são uma lista de comércios.

+ URL

    ```
    GET  /comercios?categories=
    ```

    | Parameters | Type | Requirement | Description |
    |---|---|---|---|
    | `categories` | string | opcional | `"true"` para agrupar os comércios por categoria, `"false"` caso o contrário.|

+ **Exemplos**

    + Request

        ```
        curl http://api/comercios
        ```

    + Response

        ```
        Status: 200 OK
        ```
        ```
        [
            {
                "id": "3671361e6d5dc1ee674156beed67b1fd",
                "attributes": {
                    "endereco": "rua, numero - bairro - cidade/UF",
                    "horarios": "terça-feira - domingo, 17:00 - 23:00",
                    "categoria": "lanchonete"
                },
                "cardápio": "3671361e6d5dc1ee674156beed67b1fd",
                "created_at": 1628721657.488885,
                "nome": "lanche_feliz"
            }
        ]
        ```

    + Request

        ```
        curl http://api/comercios?categories=true
        ```

    + Response

        ```
        Status: 200 OK
        ```
        ```
        {
            "lanchonete": [
                {
                    "id": "3671361e6d5dc1ee674156beed67b1fd",
                    "attributes": {
                        "endereco": "rua, numero - bairro - cidade/UF",
                        "horarios": "terça-feira - domingo, 17:00 - 23:00",
                        "categoria": "lanchonete"
                    },
                    "cardápio": "3671361e6d5dc1ee674156beed67b1fd",
                    "created_at": 1628721657.488885,
                    "nome": "lanche_feliz"
                }
            ]
        }
        ```

## Acessa o comércio por ID [GET]

Retorna um *JSON* contendo o comércio cadastrado com o id informado na URL.

+ URL
    ```
    GET /comercio?id=
    ```

    | Parameters | Type | Requirement | Description |
    |---|---|---|---|
    | `id` | string | obrigatório | o id do comércio cadastrado. |

+ **Exemplos**

    + Request

        ```
        curl http://api/comercio?id=3671361e6d5dc1ee674156beed67b1fd
        ```

    + Response

        ```
        Status: 200 OK
        ```
        ```
        {
            "id": "3671361e6d5dc1ee674156beed67b1fd",
            "attributes": {
                "endereco": "rua, numero - bairro - cidade/UF",
                "horarios": "terça-feira - domingo, 17:00 - 23:00",
                "categoria": "lanchonete"
            },
            "cardápio": "3671361e6d5dc1ee674156beed67b1fd",
            "created_at": 1628721657.488885,
            "nome": "lanche_feliz"
        }
        ```

    + Request

        ```
        curl http://api/comercio?id=0
        ```

    + Response

        ```
        Status: 400 BAD REQUEST
        ```
        ```
        {
            "message": "Erro: comércio com id 0 não cadastrado!",
            "status_code" : 400
        }
        ```

## Acessa o comércio por NOME [GET]

Retorna um *JSON* contendo o comércio cadastrado com o nome informado na URL.

+ URL

    ```
    GET /comercio/<comercio_nome>
    ```

    | Parameters | Type | Requirement | Description |
    |---|---|---|---|
    | `comercio_nome` | string | obrigatório | o nome do comércio cadastrado. |

+ **Exemplos**

    + Request

        ```
        curl http://api/comercio/lanche_feliz
        ```

    + Response

        ```
        Status: 200 OK
        ```
        ```
        {
            "id": "3671361e6d5dc1ee674156beed67b1fd",
            "attributes": {
                "endereco": "rua, numero - bairro - cidade/UF",
                "horarios": "terça-feira - domingo, 17:00 - 23:00",
                "categoria": "lanchonete"
            },
            "cardápio": "3671361e6d5dc1ee674156beed67b1fd",
            "created_at": 1628721657.488885,
            "nome": "lanche_feliz"
        }
        ```

    + Request

        ```
        curl http://api/comercio/so_lanche
        ```

    + Response

        ```
        Status: 400 BAD REQUEST
        ```
        ```
        {
            "message": "Erro: comércio com nome so_lanche não cadastrado!",
            "status_code" : 400
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

## Retorna produto de um comercio

Recupera um json do produto através do nome do comércio e o id do produto. 

```
GET  /comercio/<nome_comercio>/produtos/<produto_id>
```

Exemplo

```
curl http://api/comercio/lanche_feliz/produto/c666ae577afa4776148c2e09b9545320cbbbfac1
```

Resposta

```
Status: 200 OK
```
```
{
    "_id": "c666ae577afa4776148c2e09b9545320cbbbfac1",
    "attributes": {},
    "created_at": 1630117957.674759,
    "nome": "empanado_de_frango"
}
```

Exemplo

```
curl http://api/comercio/lanche_feliz/produto/ioasjfoankfn
```

Resposta

```
Status: 400 BAD REQUEST
```
```
{
    "message": "Erro: produto não cadastrado no sistema",
    "status_code": 400
}
```

Exemplo

```
curl http://api/comercio/lanche_bom/produto/c666ae577afa4776148c2e09b9545320cbbbfac1
```

Resposta

```
Status: 400 BAD REQUEST
```
```
{
    "message": "Erro: produto não faz parte desse comércio",
    "status_code": 400
}
```

## Lista produtos de um comercio

Retorna uma lista com todos os produtos cadastrados no comércio, sendo também possível o retorno de um dicionário com o agrupamento dos produtos por categoria, onde as chaves do dicionário são as categorias e os valores são uma lista de produtos.

```
GET  /comercio/<nome_comercio>/produtos?categories=
```

Exemplo

```
curl http://api/comercio/lanche_feliz/produtos
```

Resposta

```
Status: 200 OK
```
```
[
    {
        "_id" : "42685f4d9216a4f36f45876fff6323f1fe70c51e",
        "attributes" : {
            "categoria" : "coxinha"
        },
        "created_at" : 1630631958.37054,
        "nome" : "coxinha de frango"
    }
]
```

Exemplo

```
curl http://api/comercio/lanche_feliz/produtos?categories=true
```

Resposta

```
Status: 200 OK
```
```
{
    "coxinha": [
        {
            "_id" : "42685f4d9216a4f36f45876fff6323f1fe70c51e",
            "attributes" : {
                "categoria" : "coxinha"
            },
            "created_at" : 1630631958.37054, 
            "nome" : "coxinha de frango"
        }
    ]
}
```

## Lista ids dos produtos de um comercio

Retorna uma lista com todos os ids dos produtos cadastrados no comércio.

```
GET  /comercio/<nome_comercio>/produtos/ids
```

Exemplo

```
curl http://api/comercio/lanche_feliz/produtos/ids
```

Resposta

```
Status: 200 OK
```
```
[
    "3d3f5f603fe10d0dc519e6fc94e4df04928cf3df",
    "3752b85753550e2a5a691efdbbb406df97474903",
    "9ef383839b477c683b0f58d74fbb6fa4db56628e"
]
```

## Edita produto no cardápio de um comércio

Para realizar a edição de um produto no cardápio de um comércio, a requisição deve enviar no body um JSON com o campo `attributes`, opcional, contendo as informações para atualização e o campo `nome`, opcional, com o novo nome do produto. O `attributes` do produto deve ser um dict e o `nome` uma string. O nome do comércio e o id do produto são passados na URL.

```
PATCH /comercio/<comercio_nome>/produto/<produto_id>
```

Exemplo

```
curl \
    -d '{
            "attributes": {
                "categoria": "salgado"
            }
        }' \
    -H "Content-Type: application/json" \
    -X PATCH http://api/comercio/lanche_feliz/produto/c3h2foe6di3e1ee6bd3ctb4r
```

Resposta

```
Status: 200 OK
```
```
{
    "_id": "c3h2foe6di3e1ee6bd3ctb4r",
    "attributes": {
        "categoria": "salgado"
    },
    "created_at": 1631106735.893032,
    "nome": "produto"
}
```

Exemplo

```
curl \
    -d '{
            "nome": "pastel de frango"
        }' \
    -H "Content-Type: application/json" \
    -X PATCH http://api/comercio/lanche_feliz/produto/c3h2foe6di3e1ee6bd3ctb4r
```

Resposta

```
Status: 200 OK
```
```
{
    "_id": "c3h2foe6di3e1ee6bd3ctb4r",
    "attributes": {
        "categoria": "salgado"
    },
    "created_at": 1631106735.893032,
    "nome": "pastel de frango"
}
```

Exemplo

```
curl \
    -d '{
            "attributes": {
                "valor": 3.00
            },
            "nome": "pastel de frango com queijo"
        }' \
    -H "Content-Type: application/json" \
    -X PATCH http://api/comercio/lanche_feliz/produto/c3h2foe6di3e1ee6bd3ctb4r
```

Resposta

```
Status: 200 OK
```
```
{
    "_id": "c3h2foe6di3e1ee6bd3ctb4r",
    "attributes": {
        "categoria": "salgado",
        "valor": 3.00
    },
    "created_at": 1631106735.893032,
    "nome": "pastel de frango com queijo"
}
```

Exemplo

```
curl \
    -d '{
            "attributes": "salgado"
        }' \
    -H "Content-Type: application/json" \
    -X PATCH http://api/comercio/lanche_feliz/produto/c3h2foe6di3e1ee6bd3ctb4r
```

Resposta

```
400 BAD REQUEST
```
```
{
    "message": "Erro: attributes inválidos!",
    "status_code": 400
}
```

## Adiciona um produto aos destaques do cardápio

Adiciona um produto aos destaques do cardapio de um comércio e retorna o cardapio atualizado. O nome do comércio e o id do produto são passados na URL. O produto, ao qual os id corresponde, já deve estar cadastrado no cardápio do comércio.

```
POST /comercio/<comercio_nome>/destaques/<produto_id>
```

Exemplo

```
curl -x POST http://api/comercio/lanche_feliz/destaques/c3h2foe6di3e1ee6bd3ctb4r
```

Resposta

```
Status: 201 CREATED
```
```
{
    "_id": "3671361e6d5dc1ee674156beed67b1fd",
    "created_at": 1628721657.488885,
    "destaques": [
        "c3h2foe6di3e1ee6bd3ctb4r"
    ],
    "produtos": [
        "c3h2foe6di3e1ee6bd3ctb4r",
        "3d3f5f603fe10d0dc519e6fc",
        "3752b85753550e2a5a691efd"
    ]
}
```

Exemplo

```
curl -x POST http://api/comercio/lanche_feliz/destaques/7522b85753550e2a5a691abe
```

Resposta

```
Status: 400 BAD REQUEST
```
```
{
    "message": "Erro: produto não faz parte do cardápio do comércio!",
    "status_code": 400
}
```

## Remove um produto dos destaques do cardápio

Remove um produto dos destaques do cardapio de um comércio e retorna o cardapio atualizado. O nome do comércio e o id do produto são passados na URL. O produto, ao qual o id corresponde, já deve estar cadastrado no cardápio do comércio.

```
DELETE /comercio/<comercio_nome>/destaques/<produto_id>
```

Exemplo

```
curl -x DELETE http://api/comercio/lanche_feliz/destaques/c3h2foe6di3e1ee6bd3ctb4r
```

Resposta

```
Status: 200 OK
```
```
{
    "_id": "3671361e6d5dc1ee674156beed67b1fd",
    "created_at": 1628721657.488885,
    "destaques": [],
    "produtos": [
        "c3h2foe6di3e1ee6bd3ctb4r",
        "3d3f5f603fe10d0dc519e6fc",
        "3752b85753550e2a5a691efd"
    ]
}
```

Exemplo

```
curl -x DELETE http://api/comercio/lanche_feliz/destaques/c3h2foe6di3e1ee6bd3ctb4r
```

Resposta

```
Status: 400 BAD REQUEST
```
```
{
    "message": "Erro: produto com id c3h2foe6di3e1ee6bd3ctb4r não está nos destaques!",
    "status_code": 400
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
curl -x DELETE http://api/comercio/lanche_feliz/produto/c3h2foe6di3e1ee6bd3ctb4r
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
curl -x DELETE http://api/comercio/lanche_feliz/produto/b1cef4d8hb611df8c443a1
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

## Adiciona categoria ao cardápio de um comércio

Adiciona uma categoria ao comércio. O nome do comércio deve ser passado na URL. O campo `categoria` é obrigatório e deve conter uma string com o nome da categoria. O retorno é um JSON do cardápio do comércio.

```
POST /comercio/<comercio_nome>/categoria
```

Exemplo

```
curl \
    -d '{
            "categoria": "categoria inovação"
        }' \
    -H "Content-Type: application/json" \
    -X POST http://api/comercio/lanche_feliz/categoria
```

Resposta

```
Status: 201 CREATED
```
```
{
    "_id": "3671361e6d5dc1ee674156beed67b1fd",
    "categorias": [
        "categoria inovação"
    ],
    "created_at": 1631625353.1946077,
    "destaques": [],
    "produtos": []
}
```

Exemplo

```
curl \
    -d '{
            "categoria": ""
        }' \
    -H "Content-Type: application/json" \
    -X POST http://api/comercio/lanche_feliz/categoria
```

Resposta

```
Status: 400 BAD REQUEST
```
```
{
    "message": "Erro: categoria não informada!",
    "status_code": 400
}
```

## Remove categoria de um cardápio

Remove uma categoria. O nome do comércio deve ser passado na URL. O campo `categoria` é obrigatório e deve conter uma string com o nome da categoria a ser removida. O retorno é um JSON do cardápio do comércio.

```
DELETE /comercio/<comercio_nome>/categoria
```

Exemplo

```
curl \
    -d '{
            "categoria": "categoria inovação"
        }' \
    -H "Content-Type: application/json" \
    -X DELETE http://api/comercio/lanche_feliz/categoria
```

Resposta

```
Status: 200 OK
```
```
{
    "_id": "d81d37521e2ee08c5b50ac4f5c9bed652634fb95",
    "categorias": [],
    "created_at": 1631625353.1946077,
    "destaques": [],
    "produtos": []
}
```

Exemplo

```
curl \
    -d '{
            "categoria": "categoria que não existe"
        }' \
    -H "Content-Type: application/json" \
    -X DELETE http://api/comercio/lanche_feliz/categoria
```

Resposta

```
Status: 400 BAD REQUEST
```
```
{
    "message": "Erro: categoria não faz parte do comércio",
    "status_code": 400
}
```