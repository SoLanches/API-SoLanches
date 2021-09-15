# **API SoLanches**

API do projeto [SoLanches](https://github.com/SoLanches) que oferece funcionalidades *CRUD* de um sistema de comércios do ramo alimentício. 

## Consulta o status do servidor da API [GET]

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
    | `nome` | string | obrigatório | o nome do comercio. |
    | `attributes` | dict | obrigatório | as informações de cadastro do comércio. |
    | `endereco` | string | obrigatório | o endereço do comercio, no campo `attributes`. |
    | `horarios` | string | obrigatório | os horários do comercio, no campo `attributes`. |

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

## Lista os comércios [GET]

Retorna uma lista com todos os comércios cadastrados no sistema, sendo também possível o retorno de um dicionário com o agrupamento dos comércios por categoria, onde as chaves do dicionário são as categorias e os valores são uma lista de comércios.

+ URL

    ```
    GET  /comercios?categories=
    ```

    | Parameters | Type | Requirement | Description |
    |---|---|---|---|
    | `categories` | string | opcional | `"true"` para agrupar os comércios por categoria, `"false"` caso o contrário. |

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

## Cadastra o produto no cardápio do comércio [POST]

Adiciona um produto no banco de dados, referenciando-o no cardápio do comércio cadastrado com o nome informado na URL e retorna um *JSON* com o produto adicionado. A requisição deve enviar no body um *JSON* com os campos `nome` e `attributes`.

+ URL

    ```
    POST /comercio/<comercio_nome>/produto
    ```

    | Parameters | Type | Requirement | Description |
    |---|---|---|---|
    | `comercio_nome` | string | obrigatório | o nome do comércio cadastrado. |

+ Body

    | Parameters | Type | Requirement | Description |
    |---|---|---|---|
    | `nome` | string | obrigatório | o nome do produto. |
    | `attributes` | dict | opcional | as informações de cadastro do produto. |

+ **Exemplos**

    + Request
        ```
        curl \
            -d '{
                    "nome": "produto"
                }' \
            -H "Content-Type: application/json" \
            -X POST http://api/comercio/lanche_feliz/produto
        ```

    + Response

        ```
        Status: 201 CREATED
        ```
        ```
        {
            "message": "Produto com o id c3h2foe6di3e1ee6bd3ctb4r adicionado!",
        }
        ```
    
    + Request
        ```
        curl \
            -d '{
                    "nome": "produto",
                    "attributes":{
                        "categoria": "doce"
                    }
                }' \
            -H "Content-Type: application/json" \
            -X POST http://api/comercio/lanche_feliz/produto
        ```

    + Response

        ```
        Status: 201 CREATED
        ```
        ```
        {
            "message": "Produto com o id 3d3f5f603fe10d0dc519e6fc adicionado!",
        }
        ```

    + Request

        ```
        curl \
            -d '{
                    "nome": "produto"
                }' \
            -H "Content-Type: application/json" \
            -X POST http://api/comercio/so_lanche/produto
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

## Acessa o produto do comércio [GET]

Retorna um *JSON* contendo o produto cadastrado no comércio. O nome do comércio e o id do produto devem ser informados na URL.

+ URL

    ```
    GET  /comercio/<nome_comercio>/produtos/<produto_id>
    ```

    | Parameters | Type | Requirement | Description |
    |---|---|---|---|
    | `comercio_nome` | string | obrigatório | o nome do comércio cadastrado. |
    | `produto_id` | string | obrigatório | o id do produto cadastrado no comércio. |

+ **Exemplos**

    + Request

        ```
        curl http://api/comercio/lanche_feliz/produto/c3h2foe6di3e1ee6bd3ctb4r
        ```

    + Response

        ```
        Status: 200 OK
        ```
        ```
        {
            "_id": "c3h2foe6di3e1ee6bd3ctb4r",
            "created_at": 1631106735.893032,
            "nome": "produto"
        }
        ```

    + Request

        ```
        curl http://api/comercio/lanche_feliz/produto/0
        ```

    + Response

        ```
        Status: 400 BAD REQUEST
        ```
        ```
        {
            "message": "Erro: produto não cadastrado no sistema",
            "status_code": 400
        }
        ```

## Edita o produto no cardápio do comércio [PATCH]

Atuliza as informaçõa do produto no cardápio de um comércio. A requisição deve enviar no body um *JSON* com o campo `nome` ou o campo `attributes`. O nome do comércio e o id do produto devem ser informados na URL.

+ URL

    ```
    PATCH /comercio/<comercio_nome>/produto/<produto_id>
    ```

    | Parameters | Type | Requirement | Description |
    |---|---|---|---|
    | `comercio_nome` | string | obrigatório | o nome do comércio cadastrado. |
    | `produto_id` | string | obrigatório | o id do produto cadastrado no comércio. |

+ Body

    | Parameters | Type | Requirement | Description |
    |---|---|---|---|
    | `nome` | string | obrigatório | o novo nome do produto. |
    | `attributes` | dict | opcional | as novas informações de cadastro do produto. |

+ **Exemplos**
    
    + Request

        ```
        curl \
            -d '{
                    "nome": "pastel de frango"
                }' \
            -H "Content-Type: application/json" \
            -X PATCH http://api/comercio/lanche_feliz/produto/c3h2foe6di3e1ee6bd3ctb4r
        ```

   + Response

        ```
        Status: 200 OK
        ```
        ```
        {
            "_id": "c3h2foe6di3e1ee6bd3ctb4r",
            "created_at": 1631106735.893032,
            "nome": "pastel de frango"
        }
        ```

    + Request

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

    + Response

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

    + Request

        ```
        curl \
            -d '{
                    "attributes": {
                        "valor": 5.00
                    },
                    "nome": "bolo no pote"
                }' \
            -H "Content-Type: application/json" \
            -X PATCH http://api/comercio/lanche_feliz/produto/3d3f5f603fe10d0dc519e6fc
        ```

    + Response

        ```
        Status: 200 OK
        ```
        ```
        {
            "_id": "3d3f5f603fe10d0dc519e6fc",
            "attributes": {
                "categoria": "doce",
                "valor": 3.00
            },
            "created_at": 1630117957.674759,
            "nome": "bolo no pote"
        }
        ```

    + Request

        ```
        curl \
            -d '{
                    "attributes": "valor"
                }' \
            -H "Content-Type: application/json" \
            -X PATCH http://api/comercio/lanche_feliz/produto/c3h2foe6di3e1ee6bd3ctb4r
        ```

    + Response

        ```
        400 BAD REQUEST
        ```
        ```
        {
            "message": "Erro: attributes inválidos!",
            "status_code": 400
        }
        ```

## Lista os produtos do comércio [GET]

Retorna uma lista com todos os produtos cadastrados no comércio com o nome informado na URL, sendo também possível o retorno de um dicionário com o agrupamento dos produtos por categoria, onde as chaves do dicionário são as categorias e os valores são uma lista de produtos.

+ URL

    ```
    GET  /comercio/<nome_comercio>/produtos?categories=
    ```

    | Parameters | Type | Requirement | Description |
    |---|---|---|---|
    | `comercio_nome` | string | obrigatório | o nome do comércio cadastrado. |
    | `categories` | string | opcional | `"true"` para agrupar os produtos por categoria, `"false"` caso o contrário. |

+ **Exemplos**

    + Request

        ```
        curl http://api/comercio/lanche_feliz/produtos
        ```

    + Response
        ```
        Status: 200 OK
        ```
        ```
        [
            {
                "_id": "c3h2foe6di3e1ee6bd3ctb4r",
                "attributes": {
                    "categoria": "salgado"
                },
                "created_at": 1631106735.893032,
                "nome": "pastel de frango"
            }
            {
                "_id": "3d3f5f603fe10d0dc519e6fc",
                "attributes": {
                    "categoria": "doce",
                    "valor": 3.00
                },
                "created_at": 1630117957.674759,
                "nome": "bolo no pote"
            }
        ]
        ```

    + Request

        ```
        curl http://api/comercio/lanche_feliz/produtos?categories=true
        ```

    + Response

        ```
        Status: 200 OK
        ```
        ```
        {
            "salgado": [
                {
                    "_id": "c3h2foe6di3e1ee6bd3ctb4r",
                    "attributes": {
                        "categoria": "salgado"
                    },
                    "created_at": 1631106735.893032,
                    "nome": "pastel de frango"
                }
            ],
            "doce": [
                {
                    "_id": "3d3f5f603fe10d0dc519e6fc",
                    "attributes": {
                        "categoria": "doce",
                        "valor": 3.00
                    },
                    "created_at": 1630117957.674759,
                    "nome": "bolo no pote"
                }            
            ]
        }
        ```

## Adiciona o produto aos destaques do cardápio

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