# **API SoLanches**

API do projeto [SoLanches](https://github.com/SoLanches) que oferece funcionalidades *CRUD* de um sistema para comércios do ramo alimentício.

### Recursos disponíveis para acesso via API:

* [**Status do servidor**](#consulta-o-status-do-servidor-da-api-get)
* [**Login no servidor**](#efetua-login-no-servidor-post)
* [**Logout no servidor**](#efetua-logout-no-servidor-delete)
* [**Cadastro do comércio**](#cadastra-o-comércio-post)
* [**Acesso ao comércio por ID**](#acessa-o-comércio-por-id-get)
* [**Acesso ao comércio por nome**](#acessa-o-comércio-por-nome-get)
* [**Edição do comércio**](#edita-o-comércio-patch)
* [**Listagem dos comércios**](#lista-os-comércios-get)
* [**Remoção do comércio**](#remove-o-comércio-delete)
* [**Cadastro do produto**](#cadastra-o-produto-no-cardápio-do-comércio-post)
* [**Acesso ao produto por ID**](#acessa-o-produto-do-comércio-get)
* [**Edição do produto**](#edita-o-produto-no-cardápio-do-comércio-patch)
* [**Listagem dos proutos**](#lista-os-produtos-do-comércio-get)
* [**Remoção do produto**](#remove-o-produto-do-comércio-delete)
* [**Acesso ao cardápio**](#acessa-o-cardápio-de-um-comércio-get)
* [**Adição do produto aos destaques**](#adiciona-o-produto-aos-destaques-do-cardápio-post)
* [**Remoção do produto nos destaques**](#remove-o-produto-dos-destaques-do-cardápio-delete)
* [**Adição de categoria ao cardápio**](#adiciona-categoria-ao-cardápio-do-comércio-post)
* [**Remoção de categoria no cardápio**](#remove-a-categoria-do-cardápio-delete)

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

## Efetua login no servidor [POST]

Permite o acesso às rotas da API que necessitam de autenticação e retorna um *JSON* contendo o token de acesso. A requisição deve enviar no body um *JSON* contendo os campos `nome` e `password`.

+ URL

    ```
    POST /login
    ```

+ Body

    | Parameters | Type | Requirement | Description |
    |---|---|---|---|
    | `nome` | string | obrigatório | o nome do comercio. |
    | `password` | string | obrigatório | a senha cadastrada para login no sistema. |

+ **Exemplos**
    
    + Request

        ```
        curl -L -X POST 'https://solanches.herokuapp.com/login' \
        -H 'Content-Type: application/json' \
        --data-raw '{
            "nome": "<comercio_nome>",
            "password": "<senha>"
        }'
        ```

    + Response

        ```
        Status: 200 OK
        ```
        ```
        {
            "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjI2ZmJiMTNiYjc4MjQ1N2JmZWEzNmM0Mzg2OWEzYjQwNTI2OGE3YTciLCJleHAiOjE2MzE3NTM5Mzh9.FZ05Ip4pyXi2lzrqaxR-YDIyxfhLq0Xsn5N7ROICKzc"
        }
        ```

    + Request

        ```
        curl -L -X POST 'https://solanches.herokuapp.com/login' \
        -H 'Content-Type: application/json' \
        --data-raw '{
            "nome": "<comercio_nome>",
            "password": ""
        }'
        ```

    + Response

        ```
        Status:  400 BAD REQUEST
        ```
        ```
        {
            "error": "SolanchesBadRequestError",
            "message": "Erro! Senha incorreta",
            "status_code": 400
        }
        ```

## Efetua logout no servidor [DELETE]

Encerra o acesso às rotas da API que necessitam de autenticação e retorna um *JSON* contendo a mensagem de encerramento. A requisição deve enviar no headers o campo `authorization`.

+ URL

    ```
    DELETE /logout
    ```

+ Headers

    | Parameters | Type | Requirement | Description |
    |---|---|---|---|
    | `authorization` | string | obrigatório | o token obtido ao ser feito o login. |

+ **Exemplos**
    
    + Request

        ```
        curl -L -X DELETE 'https://solanches.herokuapp.com/logout' \
        -H 'authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjI2ZmJiMTNiYjc4MjQ1N2JmZWEzNmM0Mzg2OWEzYjQwNTI2OGE3YTciLCJleHAiOjE2MzE3NTM5Mzh9.FZ05Ip4pyXi2lzrqaxR-YDIyxfhLq0Xsn5N7ROICKzc'
        ```

    + Response

        ```
        Status: 200 OK
        ```
        ```
        {
            "message": "Logout feito com sucesso",
            "status_code": 200
        }
        ```

    + Request

        ```
        curl -L -X DELETE 'https://solanches.herokuapp.com/logout' \
        -H 'authorization: 0'
        ```

    + Response

        ```
        Status: 400 BAD REQUEST
        ```
        ```
        {
            "error": "SolanchesBadRequestError",
            "message": "Error: Token inválido ou expirado.",
            "status_code": 400
        }
        ```

    + Request

        ```
        curl -L -X DELETE 'https://solanches.herokuapp.com/logout'
        ```

    + Response

        ```
        Status: 401 UNAUTHORIZED
        ```
        ```
        {
            "error": "SolanchesNotAuthorizedError",
            "message": "Error: Você não tem permissão para acessar essa rota.",
            "status_code": 401
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
    | `password` | string | obrigatório | a senha para efetuar login no sistema. |
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
        curl -L -X POST 'https://solanches.herokuapp.com/comercio' \
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
            "error": "SolanchesBadRequestError",
            "message": "Erro: campo horarios não informados!",
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
        Status: 400 BAD REQUEST
        ```
        ```
        {
            "error": "SolanchesBadRequestError",
            "message": "Erro: comercio com nome Test já cadastrado!",
            "status_code": 400
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
        Status: 404 NOT FOUND
        ```
        ```
        {
            "error": "SolanchesNotFoundError",
            "message": "Erro: comercio com o nome 0 não cadastrado!",
            "status_code": 404
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
        Status: 404 NOT FOUND
        ```
        ```
        {   
            "error": "SolanchesNotFoundError",
            "message": "Erro: comércio com nome so_lanche não cadastrado!",
            "status_code" : 404
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
        Status: 404 NOT FOUND
        ```
        ```
        {   
            "error": "SolanchesNotFoundError",
            "message": "Erro: comércio com nome so_lanche não cadastrado!",
            "status_code" : 400
        }
        ```

    + Request
    
        ```
        curl -L -X PATCH 'https://solanches.herokuapp.com/comercio/so_lanche' \
        -H 'Content-Type: application/json' \
        --data-raw '{
            "attributes": {
            }
        }'
        ```

    + Response

        ```
        Status: 400 BAD REQUEST
        ```
        ```
        {
            "error": "SolanchesBadRequestError",
            "message": "Erro: attributes inválidos",
            "status_code": 400
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
        Status: 404 NOT FOUND
        ```
        ```
        {
            "error": "SolanchesNotFoundError",
            "message": "Erro: comércio com nome so_lanche não cadastrado!",
            "status_code" : 404
        }
        ```

## Cadastra o produto no cardápio do comércio [POST]

Adiciona um produto no banco de dados, referenciando-o no cardápio do comércio cadastrado com o nome informado na URL e retorna um *JSON* contendo o produto adicionado. A requisição deve enviar no body um *JSON* com os campos `nome` e `attributes`.

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
        curl -L -X POST 'https://solanches.herokuapp.com/comercio/lanche_feliz/produto' \
        -H 'Content-Type: application/json' \
        --data-raw '{
            "nome":"produto"
        }'
        ```

    + Response

        ```
        Status: 201 CREATED
        ```
        ```
        {
            "_id" : "b3f58d70b4085c572eb84ee4619be3e6e0005d22",
            "nome" : "produto",
            "attributes" : {},
            "created_at" : 1632156256.37596
        }
        ```
    
    + Request

        ```
        curl -L -X POST 'https://solanches.herokuapp.com/comercio/lanche_feliz/produto' \
        -H 'Content-Type: application/json' \
        --data-raw '{
            "nome":"produto",
            "attributes":{
                "categoria": "doce"
            }
        }'
        ```

    + Response

        ```
        Status: 201 CREATED
        ```
        ```
        {
            "_id" : "df191400d15d8cb8c9459cc327b6e1fec435ae09",
            "nome" : "produto",
            "attributes" : {
                "categoria" : "doce"
            },
            "created_at" : 1632156418.89367
        }
        ```

    + Request

        ```
        curl -L -X POST 'https://solanches.herokuapp.com/comercio/so_lanche/produto' \
        -H 'Content-Type: application/json' \
        --data-raw '{
            "nome":"produto",
            "attributes":{
                "categoria": "doce"
            }
        }'
        ```

    + Response

        ```
        Status: 400 BAD REQUEST
        ```
        ```
        {
            "error": "SolanchesBadRequestError",
            "message": "Erro: comércio com nome so_lanche não cadastrado!",
            "status_code" : 400
        }
        ```

## Acessa o produto do comércio [GET]

Retorna um *JSON* contendo o produto cadastrado no comércio. O nome do comércio e o id do produto devem ser informados na URL.

+ URL

    ```
    GET  /comercio/<nome_comercio>/produto/<produto_id>
    ```

    | Parameters | Type | Requirement | Description |
    |---|---|---|---|
    | `comercio_nome` | string | obrigatório | o nome do comércio cadastrado. |
    | `produto_id` | string | obrigatório | o id do produto cadastrado no comércio. |

+ **Exemplos**

    + Request

        ```
        curl -L -X GET 'https://solanches.herokuapp.com/comercio/lanche_feliz/produto/b3f58d70b4085c572eb84ee4619be3e6e0005d22'
        ```

    + Response

        ```
        Status: 200 OK
        ```
        ```
        {
            "_id": "b3f58d70b4085c572eb84ee4619be3e6e0005d22",
            "attributes": {},
            "created_at": 1632156256.3759577,
            "nome": "produto"
        }
        ```

    + Request

        ```
        curl -L -X GET 'https://solanches.herokuapp.com/comercio/lanche_feliz/produto/0'
        ```

    + Response

        ```
        Status: 404 NOT FOUND
        ```
        ```
        {
            "error": "SolanchesNotFoundError",
            "message": "Erro: produto com o id 0 não cadastrado no comercio!",
            "status_code": 404
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
        curl -L -X PATCH 'https://solanches.herokuapp.com/comercio/lanche_feliz/produto/b3f58d70b4085c572eb84ee4619be3e6e0005d22' \
        -H 'Content-Type: application/json' \
        --data-raw '{
            "nome": "pastel de frango"
        }'
        ```

   + Response

        ```
        Status: 200 OK
        ```
        ```
        {
            "_id": "b3f58d70b4085c572eb84ee4619be3e6e0005d22",
            "attributes": {},
            "created_at": 1632156256.3759577,
            "nome": "pastel de frango"
        }
        ```

    + Request

        ```
        curl -L -X PATCH 'https://solanches.herokuapp.com/comercio/lanche_feliz/produto/b3f58d70b4085c572eb84ee4619be3e6e0005d22' \
        -H 'Content-Type: application/json' \
        --data-raw '{
            "attributes": {
                "categoria": "salgado"
            }
        }'
        ```

    + Response

        ```
        Status: 200 OK
        ```
        ```
        {
            "_id": "b3f58d70b4085c572eb84ee4619be3e6e0005d22",
            "attributes": {
                "categoria": "salgado"
            },
            "created_at": 1632156256.3759577,
            "nome": "pastel de frango"
        }
        ```

    + Request

        ```
        curl -L -X PATCH 'https://solanches.herokuapp.com/comercio/lanche_feliz/produto/df191400d15d8cb8c9459cc327b6e1fec435ae09' \
        -H 'Content-Type: application/json' \
        --data-raw '{
            "attributes": {
                "valor": 5.00
            },
            "nome": "bolo no pote"
        }'
        ```

    + Response

        ```
        Status: 200 OK
        ```
        ```
        {
            "_id": "df191400d15d8cb8c9459cc327b6e1fec435ae09",
            "attributes": {
                "categoria": "doce",
                "valor": 5.0
            },
            "created_at": 1632156418.893673,
            "nome": "bolo no pote"
        }
        ```

    + Request

        ```
        curl -L -X PATCH 'https://solanches.herokuapp.com/comercio/lanche_feliz/produto/df191400d15d8cb8c9459cc327b6e1fec435ae09' \
        -H 'Content-Type: application/json' \
        --data-raw '{
            "attributes": "valor"
        }'
        ```

    + Response

        ```
        400 BAD REQUEST
        ```
        ```
        {   
            "error": "SolanchesBadRequestError",
            "message": "Erro: attributes inválidos!",
            "status_code": 400
        }
        ```

    + Request

        ```
        curl -L -X PATCH 'https://solanches.herokuapp.com/comercio/lanche_feliz/produto/0' \
        -H 'Content-Type: application/json' \
        --data-raw '{
            "attributes": {
            }
        }'
        ```

    + Response

        ```
        Status: 404 NOT FOUND
        ```
        ```
        {
            "error": "SolanchesNotFoundError",
            "message": "Erro: produto com o id 0 não cadastrado no comercio!",
            "status_code": 404
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
        curl -L -X GET 'https://solanches.herokuapp.com/comercio/lanche_feliz/produtos'
        ```

    + Response
        ```
        Status: 200 OK
        ```
        ```
        [
            {
                "_id": "b3f58d70b4085c572eb84ee4619be3e6e0005d22",
                "attributes": {
                    "categoria": "salgado"
                },
                "created_at": 1632156256.3759577,
                "nome": "pastel de frango"
            },
            {
                "_id": "df191400d15d8cb8c9459cc327b6e1fec435ae09",
                "attributes": {
                    "categoria": "doce",
                    "valor": 5.0
                },
                "created_at": 1632156418.893673,
                "nome": "bolo no pote"
            }
        ]
        ```

    + Request

        ```
        curl -L -X GET 'https://solanches.herokuapp.com/comercio/lanche_feliz/produtos?categories=true'
        ```

    + Response

        ```
        Status: 200 OK
        ```
        {
            "doce": [
                {
                    "_id": "df191400d15d8cb8c9459cc327b6e1fec435ae09",
                    "attributes": {
                        "categoria": "doce",
                        "valor": 5.0
                    },
                    "created_at": 1632156418.893673,
                    "nome": "bolo no pote"
                }
            ],
            "salgado": [
                {
                    "_id": "b3f58d70b4085c572eb84ee4619be3e6e0005d22",
                    "attributes": {
                        "categoria": "salgado"
                    },
                    "created_at": 1632156256.3759577,
                    "nome": "pastel de frango"
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
        curl -L -X DELETE 'https://solanches.herokuapp.com/comercio/lanche_feliz/produto/df191400d15d8cb8c9459cc327b6e1fec435ae09'
        ```

    + Response

        ```
        Status: 200 OK
        ```
        ```
        {
            "_id": "26fbb13bb782457bfea36c43869a3b405268a7a7",
            "categorias": [],
            "created_at": 1631744493.2539248,
            "destaques": [],
            "produtos": [
                "b3f58d70b4085c572eb84ee4619be3e6e0005d22"
            ]
        }
        ```

    + Request

        ```
        curl -L -X DELETE 'https://solanches.herokuapp.com/comercio/lanche_feliz/produto/0'
        ```

    + Response

        ```
        Status: 404 NOT FOUND
        ```
        ```
        {
            "error": "SolanchesNotFoundError",
            "message": "Erro: produto com o id 0 não cadastrado no comercio!",
            "status_code": 404
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
        curl -L -X GET 'https://solanches.herokuapp.com/comercio/lanche_feliz/cardapio'
        ```

    + Response

        ```
        Status: 200 OK
        ```
        ```
        {
            "_id": "26fbb13bb782457bfea36c43869a3b405268a7a7",
            "categorias": [
                "doce",
                "salgado"
            ],
            "created_at": 1631744493.25392,
            "destaques": [],
            "produtos": [
                "b3f58d70b4085c572eb84ee4619be3e6e0005d22"
            ]
        }
        ```

    + Request

        ```
        curl -L -X GET 'https://solanches.herokuapp.com/comercio/so_lanche/cardapio'
        ```

    + Response

        ```
        Status: 404 NOT FOUND
        ```
        ```
        {
            "error": "SolanchesNotFoundError",
            "message": "Erro: comércio com nome so_lanche não cadastrado!",
            "status_code" : 404
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
        curl -L -X POST 'https://solanches.herokuapp.com/comercio/lanche_feliz/destaques/b3f58d70b4085c572eb84ee4619be3e6e0005d22'
        ```

    + Response

        ```
        Status: 201 CREATED
        ```
        ```
        {
            "_id": "26fbb13bb782457bfea36c43869a3b405268a7a7",
            "categorias": [
                "doce",
                "salgado"
            ],
            "created_at": 1631744493.25392,
            "destaques": [
                "b3f58d70b4085c572eb84ee4619be3e6e0005d22"
            ],
            "produtos": [
                "b3f58d70b4085c572eb84ee4619be3e6e0005d22"
            ]
        }
        ```

    + Request

        ```
        curl -L -X POST 'https://solanches.herokuapp.com/comercio/lanche_feliz/destaques/0'
        ```

    + Response

        ```
        Status: 404 NOT FOUND
        ```
        ```
        {
            "error": "SolanchesNotFoundError",
            "message": "Erro: produto com o id 0 não cadastrado no comercio!",
            "status_code": 404
        }
        ```

## Remove o produto dos destaques do cardápio [DELETE]

Deleta o id do produto contido nos destaques do cardápio do comércio e retorna um *JSON* contendo o cardápio atualizado. O nome do comércio e o id do produto são passados na URL.

+ URL

    ```
    DELETE /comercio/<comercio_nome>/destaques/<produto_id>
    ```

    | Parameters | Type | Requirement | Description |
    |---|---|---|---|
    | `comercio_nome` | string | obrigatório | o nome do comércio cadastrado. |
    | `produto_id` | string | obrigatório | o id do produto cadastrado no comércio. |

+ **Exemplos**

    + Request

        ```
        curl -L -X DELETE 'https://solanches.herokuapp.com/comercio/lanche_feliz/destaques/b3f58d70b4085c572eb84ee4619be3e6e0005d22'
        ```
    
    + Response

        ```
        Status: 200 OK
        ```
        ```
        {
            "_id": "26fbb13bb782457bfea36c43869a3b405268a7a7",
            "categorias": [
                "doce",
                "salgado"
            ],
            "created_at": 1631744493.25392,
            "destaques": [],
            "produtos": [
                "b3f58d70b4085c572eb84ee4619be3e6e0005d22"
            ]
        }
        ```

    + Request

        ```
        curl -L -X DELETE 'https://solanches.herokuapp.com/comercio/lanche_feliz/destaques/0'
        ```

    + Response

        ```
        Status: 404 NOT FOUND
        ```
        ```
        {
            "error": "SolanchesNotFoundError",
            "message": "Erro: produto com o id 0 não cadastrado no comercio!",
            "status_code": 404
        }
        ```

## Adiciona categoria ao cardápio do comércio [POST]

Adiciona uma categoria à lista de categorias do cardápio do comércio com o nome informado na URL e retorna um *JSON* contendo o cardápio atualizado. A requisição deve enviar no body um *JSON* com o campo `categoria`.

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
        curl -L -X POST 'https://solanches.herokuapp.com/comercio/lanche_feliz/categoria' \
        -H 'Content-Type: application/json' \
        --data-raw '{
            "categoria": "bebidas"
        }'
        ```

    + Response

        ```
        Status: 201 CREATED
        ```
        ```
        {
            "_id": "26fbb13bb782457bfea36c43869a3b405268a7a7",
            "categorias": [
                "doce",
                "salgado",
                "bebidas"
            ],
            "created_at": 1631744493.25392,
            "destaques": [],
            "produtos": [
                "b3f58d70b4085c572eb84ee4619be3e6e0005d22"
            ]
        }
        ```

    + Request

        ```
        curl -L -X POST 'https://solanches.herokuapp.com/comercio/lanche_feliz/categoria' \
        -H 'Content-Type: application/json' \
        --data-raw '{
            "categoria": "doce"
        }'
        ```

    + Response

        ```
        Status: 400 BAD REQUEST
        ```
        ```
        {   
            "error": "SolanchesBadRequestError",
            "message": "Erro: categoria já cadastrada nesse comércio!",
            "status_code": 400
        }
        ```

## Remove a categoria do cardápio [DELETE]

Deleta uma categoria da lista de categorias do cardápio do comercio com o nome informado na URL e retorna um *JSON* contendo o cardápio atualizado.

+ URL

    ```
    DELETE /comercio/<comercio_nome>/categoria
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
        curl -L -X DELETE 'https://solanches.herokuapp.com/comercio/lanche_feliz/categoria' \
        -H 'Content-Type: application/json' \
        --data-raw '{
            "categoria": "bebidas"
        }'
        ```

    + Response

        ```
        Status: 200 OK
        ```
        ```
        {
            "_id": "26fbb13bb782457bfea36c43869a3b405268a7a7",
            "categorias": [
                "doce",
                "salgado"
            ],
            "created_at": 1631744493.25392,
            "destaques": [],
            "produtos": [
                "b3f58d70b4085c572eb84ee4619be3e6e0005d22"
            ]
        }
        ```

    + Request

        ```
        curl -L -X DELETE 'https://solanches.herokuapp.com/comercio/lanche_feliz/categoria' \
        -H 'Content-Type: application/json' \
        --data-raw '{
            "categoria": "sucos"
        }'
        ```

    + Response

        ```
        Status: 400 BAD REQUEST
        ```
        ```
        {   
            "error": "SolanchesBadRequestError",
            "message": "Erro: categoria não faz parte do comércio",
            "status_code": 400
        }
        ```