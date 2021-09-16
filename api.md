# **API SoLanches**

API do projeto [SoLanches](https://github.com/SoLanches) que oferece funcionalidades *CRUD* de um sistema de comércios do ramo alimentício. 

### Recursos disponíveis para acesso via API:

* [**Status do servidor**](#consulta-o-status-do-servidor-da-api-get)
* [**Login no servidor**](#references)
* [**Logout do servidor**](#references)
* [**Cadastro do comércio**](#cadastra-o-comércio-post)
* [**Acesso ao comércio por ID**](#acessa-o-comércio-por-id-get)
* [**Acesso ao comércio por nome**](#acessa-o-comércio-por-nome-get)
* [**Edição do comércio**](#references)
* [**Listagem dos comércios**](#lista-os-comércios-get)
* [**Remoção do comércio**](#references)
* [**Cadastro do produto**](#cadastra-o-produto-no-cardápio-do-comércio-post)
* [**Acesso ao produto por ID**](#acessa-o-produto-do-comércio-get)
* [**Edição do produto**](#edita-o-produto-no-cardápio-do-comércio-patch)
* [**Listagem dos proutos**](#lista-os-produtos-do-comércio-get)
* [**Remoção do produto**](#references)
* [**Acesso ao cardápio**](#references)
* [**Adição do produto aos destaques**](#references)
* [**Remoção do produto dos destaques**](#references)
* [**Adição de categoria ao cardápio**](#references)
* [**Remoção de categoria do cardápio**](#references)

## Consulta o status do servidor da API [GET]

Retorna um *JSON* com informações sobre o servidor.

+ URL

    ```
    GET /status
    ```

+ **Exemplos**

    + Request

        ```
        curl -L -X GET 'https://solanches.herokuapp.com/status'
        ```

    + Response

        ```
        Status: 200 OK
        ```
        ```
        {
            "service": "api-solanches",
            "started_at": 1631743808.996303,
            "status": "operacional",
            "timestamp": 1631748110.637761
        }
        ```

## Cadastra o comércio [POST]

Adiciona um comércio no banco de dados e retorna um *JSON* contendo o comércio adicionado. A requisição deve enviar no body um *JSON* com os campos `nome`, `password` e `attributes`, o último contendo obrigatoriamente os campos `endereco` e `horarios`.

+ URL

    ```
    POST /comercio
    ```

+ Body

    | Parameters | Type | Requirement | Description |
    |---|---|---|---|
    | `nome` | string | obrigatório | o nome do comercio. |
    | `password` | string | obrigatório | a senha para login no sistema. |
    | `attributes` | dict | obrigatório | as informações de cadastro do comércio. |
    | `endereco` | string | obrigatório | o endereço do comercio, no campo `attributes`. |
    | `horarios` | string | obrigatório | os horários do comercio, no campo `attributes`. |

+ **Exemplos**
    
    + Request

        ```
        curl -L -X POST 'https://solanches.herokuapp.com/comercio' \
        -H 'Content-Type: application/json' \
        --data-raw '{
            "nome": "lanche_feliz",
            "password": "123",
            "attributes": {
                "endereco": "rua, numero - bairro - cidade(UF)",
                "horarios": "terça-feira - domingo, 17:00 - 23:00"
            }
        }'
        ```

    + Response

        ```
        Status: 201 CREATED
        ```
        ```
        {
            "_id": "26fbb13bb782457bfea36c43869a3b405268a7a7",
            "attributes": {
                "endereco": "rua, numero - bairro - cidade(UF)",
                "horarios": "terça-feira - domingo, 17:00 - 23:00"
            },
            "cardapio": "26fbb13bb782457bfea36c43869a3b405268a7a7",
            "created_at": 1631744493.2539248,
            "nome": "lanche_feliz"
        }
        ```

    + Request

        ```
        curl -L -X POST '0.0.0.0:5000/comercio' \
        -H 'Content-Type: application/json' \
        --data-raw '{
            "nome": "petisqueiro",
            "password": "123",
            "attributes": {
                "endereco": "rua, numero - bairro - cidade(UF)",
                "horarios": "sexta-feira - domingo, 19:00 - 23:00",
                "categoria": "bar"
            }
        }'
        ```

    + Response

        ```
        Status: 201 CREATED
        ```
        ```
        {
            "_id": "56c914f159915c2e696f3ef3e52d21329c153a74",
            "attributes": {
                "categoria": "bar",
                "endereco": "rua, numero - bairro - cidade(UF)",
                "horarios": "sexta-feira - domingo, 19:00 - 23:00"
            },
            "cardapio": "56c914f159915c2e696f3ef3e52d21329c153a74",
            "created_at": 1631749569.914476,
            "nome": "petisqueiro"
        }
        ```
    
    + Request

        ```
        curl -L -X POST 'https://solanches.herokuapp.com/comercio' \
        -H 'Content-Type: application/json' \
        --data-raw '{
            "nome": "lanche_feliz",
            "password": "123",
            "attributes": {
                "endereco": "rua, numero - bairro - cidade(UF)"
            }
        }'
        ```

    + Response

        ```
        Status: 400 BAD REQUEST
        ```
        ```
        {
            "message": "Erro: campo horarios não informado!",
            "status_code": 400
        }
        ```

    + Request

        ```
        curl -L -X POST 'https://solanches.herokuapp.com/comercio' \
        -H 'Content-Type: application/json' \
        --data-raw '{
            "nome": "lanche_feliz",
            "password": "123",
            "attributes": {
                "endereco": "rua, numero - bairro - cidade(UF)",
                "horarios": "terça-feira - domingo, 17:00 - 23:00"
            }
        }'
        ```

    + Response

        ```
        Status: 409 CONFLICT
        ```
        ```
        {
            "status_code": 409,
            "error": "Comércio já cadastrado no banco de dados!"
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
        curl -L -X GET 'https://solanches.herokuapp.com/comercio?id=26fbb13bb782457bfea36c43869a3b405268a7a7'
        ```

    + Response

        ```
        Status: 200 OK
        ```
        ```
        {
            "_id": "26fbb13bb782457bfea36c43869a3b405268a7a7",
            "attributes": {
                "categoria": "lanchonete",
                "endereco": "rua, numero - bairro - cidade(UF)",
                "horarios": "terça-feira - domingo, 17:00 - 23:00"
            },
            "cardapio": "26fbb13bb782457bfea36c43869a3b405268a7a7",
            "created_at": 1631744493.2539248,
            "nome": "lanche_feliz"
        }
        ```

    + Request

        ```
        curl -L -X GET 'https://solanches.herokuapp.com/comercio?id=0'
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
        curl -L -X GET 'https://solanches.herokuapp.com/comercio/lanche_feliz'
        ```

    + Response

        ```
        Status: 200 OK
        ```
        ```
        {
            "_id": "26fbb13bb782457bfea36c43869a3b405268a7a7",
            "attributes": {
                "categoria": "lanchonete",
                "endereco": "rua, numero - bairro - cidade(UF)",
                "horarios": "terça-feira - domingo, 17:00 - 23:00"
            },
            "cardapio": "26fbb13bb782457bfea36c43869a3b405268a7a7",
            "created_at": 1631744493.2539248,
            "nome": "lanche_feliz"
        }
        ```

    + Request

        ```
        curl -L -X GET 'https://solanches.herokuapp.com/comercio/so_lanche'
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

## Edita o comércio [PATCH]

Atualiza as informações do comércio com o nome informado na URL e retorna um *JSON* contendo o comércio atualizado. A requisição deve enviar no body um *JSON* com o campo `attributes`.

+ URL

    ```
    PATCH /comercio/<comercio_nome>
    ```

    | Parameters | Type | Requirement | Description |
    |---|---|---|---|
    | `comercio_nome` | string | obrigatório | o nome do comércio cadastrado. |

+ Body

    | Parameters | Type | Requirement | Description |
    |---|---|---|---|
    | `attributes` | dict | obrigatório | as novas informações de cadastro do comércio. |

+ **Exemplos**
    
    + Request

        ```
        curl -L -X PATCH 'https://solanches.herokuapp.com/comercio/lanche_feliz' \
        -H 'Content-Type: application/json' \
        --data-raw '{
            "attributes": {
                "categoria": "lanchonete"
            }
        }'
        ```

    + Response

        ```
        Status: 200 OK
        ```
        ```
        {
            "_id": "26fbb13bb782457bfea36c43869a3b405268a7a7",
            "attributes": {
                "categoria": "lanchonete",
                "endereco": "rua, numero - bairro - cidade(UF)",
                "horarios": "terça-feira - domingo, 17:00 - 23:00"
            },
            "cardapio": "26fbb13bb782457bfea36c43869a3b405268a7a7",
            "created_at": 1631744493.2539248,
            "nome": "lanche_feliz"
        }
        ```

    + Request
    
        ```
        curl -L -X PATCH 'https://solanches.herokuapp.com/comercio/so_lanche' \
        -H 'Content-Type: application/json' \
        --data-raw '{
            "attributes": {
                "endereco": "rua, numero - bairro - cidade(UF)"
            }
        }'
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
    | `categories` | string | opcional | `true` para agrupar os comércios por categoria, `false` caso o contrário. |

+ **Exemplos**

    + Request

        ```
        curl -L -X GET 'https://solanches.herokuapp.com/comercios'
        ```

    + Response

        ```
        Status: 200 OK
        ```
        ```
        [
            {
                "_id": "26fbb13bb782457bfea36c43869a3b405268a7a7",
                "attributes": {
                    "categoria": "lanchonete",
                    "endereco": "rua, numero - bairro - cidade(UF)",
                    "horarios": "terça-feira - domingo, 17:00 - 23:00"
                },
                "cardapio": "26fbb13bb782457bfea36c43869a3b405268a7a7",
                "created_at": 1631744493.2539248,
                "nome": "lanche_feliz"
            },
            {
                "_id": "56c914f159915c2e696f3ef3e52d21329c153a74",
                "attributes": {
                    "categoria": "bar",
                    "endereco": "rua, numero - bairro - cidade(UF)",
                    "horarios": "sexta-feira - domingo, 19:00 - 23:00"
                },
                "cardapio": "56c914f159915c2e696f3ef3e52d21329c153a74",
                "created_at": 1631749569.914476,
                "nome": "petisqueiro"
            }
        ]
        ```

    + Request

        ```
        curl -L -X GET 'https://solanches.herokuapp.com/comercios?categories=true'
        ```

    + Response

        ```
        Status: 200 OK
        ```
        ```
        {
            "bar": [
                {
                    "_id": "56c914f159915c2e696f3ef3e52d21329c153a74",
                    "attributes": {
                        "categoria": "bar",
                        "endereco": "rua, numero - bairro - cidade(UF)",
                        "horarios": "sexta-feira - domingo, 19:00 - 23:00"
                    },
                    "cardapio": "56c914f159915c2e696f3ef3e52d21329c153a74",
                    "created_at": 1631749569.914476,
                    "nome": "petisqueiro"
                }
            ],
            "lanchonete": [
                {
                    "_id": "26fbb13bb782457bfea36c43869a3b405268a7a7",
                    "attributes": {
                        "categoria": "lanchonete",
                        "endereco": "rua, numero - bairro - cidade(UF)",
                        "horarios": "terça-feira - domingo, 17:00 - 23:00"
                    },
                    "cardapio": "26fbb13bb782457bfea36c43869a3b405268a7a7",
                    "created_at": 1631744493.2539248,
                    "nome": "lanche_feliz"
                }
            ]
        }
        ```

## Remove o comércio [DELETE]

Deleta um comércio do banco de dados com o nome informado na URL e retorna um *JSON* contendo a mensagem de confirmação.

+ URL

    ```
    DELETE /comercio/<comercio_nome>
    ```

    | Parameters | Type | Requirement | Description |
    |---|---|---|---|
    | `comercio_nome` | string | obrigatório | o nome do comércio cadastrado. |

+ **Exemplos**

    + Request

        ```
        curl -L -X DELETE 'https://solanches.herokuapp.com/comercio/petisqueiro'
        ```

    + Response

        ```
        Status: 200 OK
        ```
        ```
        {
            "message": "comercio petisqueiro removido com sucesso."
        }
        ```

    + Request

        ```
        curl -L -X DELETE 'https://solanches.herokuapp.com/comercio/so_lanche'
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

Atuliza as informaçõa do produto no cardápio de um comércio e retrona um *JSON* contendo o produto atualizado. A requisição deve enviar no body um *JSON* com o campo `nome` ou o campo `attributes`. O nome do comércio e o id do produto devem ser informados na URL.

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

## Remove o produto do comércio [DELETE]

Deleta um produto do banco de dados e suas referências no cardápio do comércio e retorna um *JSON* contendo o cardápio atualizado. O nome do comércio e o id do produto devem ser informados na URL.

+ URL

    ```
    DELETE /comercio/<comercio_nome>/produto/<id_produto>
    ```

    | Parameters | Type | Requirement | Description |
    |---|---|---|---|
    | `comercio_nome` | string | obrigatório | o nome do comércio cadastrado. |
    | `produto_id` | string | obrigatório | o id do produto cadastrado no comércio. |

+ **Exemplos**

    + Request

        ```
        curl -x DELETE http://api/comercio/lanche_feliz/produto/3d3f5f603fe10d0dc519e6fc
        ```

    + Response

        ```
        Status: 200 OK
        ```
        ```
        {
            "id": "3671361e6d5dc1ee674156beed67b1fd",
            "created_at": 1628721657.488885,
            "destaques": [],
            "produtos": ["c3h2foe6di3e1ee6bd3ctb4r"]
        }
        ```

    + Request

        ```
        curl -x DELETE http://api/comercio/lanche_feliz/produto/0
        ```

    + Response

        ```
        Status: 400 BAD REQUEST
        ```
        ```
        {
        "message": "Erro: produto precisa fazer parte do cardápio do comércio",
        "status_code" : 400 
        }
        ```

## Acessa o cardápio de um comércio [GET]

Retorna um *JSON* contendo o cardápio com as categorias, os produtos e os destaques do comércio com o nome informado na URL.

+ URL

    ```
    GET /comercio/<comercio_nome>/cardapio
    ```

    | Parameters | Type | Requirement | Description |
    |---|---|---|---|
    | `comercio_nome` | string | obrigatório | o nome do comércio cadastrado. |

+ **Exemplos**

    + Request

        ```
        curl http://api/comercio/lanche_feliz/cardapio
        ```

    + Response

        ```
        Status: 200 OK
        ```
        ```
        {
            "id": "3671361e6d5dc1ee674156beed67b1fd",
            "created_at": 1628721657.488885,
            "categorias": [],
            "destaques": [],
            "produtos": [
                "c3h2foe6di3e1ee6bd3ctb4r"
            ]
        }
        ```

    + Request

        ```
        curl http://api/comercio/so_lanche/cardapio
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

## Adiciona o produto aos destaques do cardápio [POST]

Adiciona o id do produto, cadastrado no comércio, aos destaques do cardápio e retorna um *JSON* contendo o cardápio atualizado. O nome do comércio e o id do produto devem ser informados na URL.

+ URL

    ```
    POST /comercio/<comercio_nome>/destaques/<produto_id>
    ```

    | Parameters | Type | Requirement | Description |
    |---|---|---|---|
    | `comercio_nome` | string | obrigatório | o nome do comércio cadastrado. |
    | `produto_id` | string | obrigatório | o id do produto cadastrado no comércio. |

+ **Exemplos**
    
    + Request

        ```
        curl -x POST http://api/comercio/lanche_feliz/destaques/c3h2foe6di3e1ee6bd3ctb4r
        ```

    + Response

        ```
        Status: 201 CREATED
        ```
        ```
        {
            "_id": "3671361e6d5dc1ee674156beed67b1fd",
            "created_at": 1628721657.488885,
            "categorias": [],
            "destaques": [
                "c3h2foe6di3e1ee6bd3ctb4r"
            ],
            "produtos": [
                "c3h2foe6di3e1ee6bd3ctb4r"
            ]
        }
        ```

    + Request

        ```
        curl -x POST http://api/comercio/lanche_feliz/destaques/0
        ```

    + Response

        ```
        Status: 400 BAD REQUEST
        ```
        ```
        {
            "message": "Erro: produto não faz parte do cardápio do comércio!",
            "status_code": 400
        }
        ```

## Remove o produto dos destaques do cardápio [DELETE]

Deleta o id do produto contido nos destaques do cardápio do comércio e retorna um *JSON* contendo o cardápio atualizado. O nome do comércio e o id do produto são passados na URL.

+ URL

    ```
    DELETE /comercio/<comercio_nome>/destaques/<produto_id>
    ```

+ **Exemplos**

    + Request

        ```
        curl -x DELETE http://api/comercio/lanche_feliz/destaques/c3h2foe6di3e1ee6bd3ctb4r
        ```
    
    + Response

        ```
        Status: 200 OK
        ```
        ```
        {
            "_id": "3671361e6d5dc1ee674156beed67b1fd",
            "created_at": 1628721657.488885,
            "categorias": [],
            "destaques": [],
            "produtos": [
                "c3h2foe6di3e1ee6bd3ctb4r"
            ]
        }
        ```

    + Request

        ```
        curl -x DELETE http://api/comercio/lanche_feliz/destaques/0
        ```

    + Response

        ```
        Status: 400 BAD REQUEST
        ```
        ```
        {
            "message": "Erro: produto com id 0 não está nos destaques!",
            "status_code": 400
        }
        ```

## Adiciona categoria ao cardápio do comércio [POST]

Adiciona uma categoria à lista de categorias do cardápio do comércio com o nome informado na URL retorna um *JSON* contendo o cardápio atualizado. A requisição deve enviar no body um *JSON* com o campo `categoria`.

+ URL

    ```
    POST /comercio/<comercio_nome>/categoria
    ```

    | Parameters | Type | Requirement | Description |
    |---|---|---|---|
    | `comercio_nome` | string | obrigatório | o nome do comércio cadastrado. |

+ Body

    | Parameters | Type | Requirement | Description |
    |---|---|---|---|
    | `categoria` | string | obrigatório | o nome da categoria. |


+ **Exemplos**

    + Request
        ```
        curl \
            -d '{
                    "categoria": "bebidas"
                }' \
            -H "Content-Type: application/json" \
            -X POST http://api/comercio/lanche_feliz/categoria
        ```

    + Response

        ```
        Status: 201 CREATED
        ```
        ```
        {
            "_id": "3671361e6d5dc1ee674156beed67b1fd",
            "categorias": [
                "bebidas"
            ],
            "created_at": 1628721657.488885,
            "destaques": [],
            "produtos": [
                "c3h2foe6di3e1ee6bd3ctb4r"
            ]
        }
        ```

    + Request

        ```
        curl \
            -d '{
                    "categoria": ""
                }' \
            -H "Content-Type: application/json" \
            -X POST http://api/comercio/lanche_feliz/categoria
        ```

    + Response

        ```
        Status: 400 BAD REQUEST
        ```
        ```
        {
            "message": "Erro: categoria não informada!",
            "status_code": 400
        }
        ```

## Remove a categoria do cardápio [DELETE]

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
    "created_at": 1628721657.488885,
    "destaques": [],
    "produtos": [
        "c3h2foe6di3e1ee6bd3ctb4r"
    ]
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