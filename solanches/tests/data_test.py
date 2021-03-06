PRODUTOS_COMERCIO = [
    {
         "_id": "2d7a8e01d2c90840c2f7c0801ae881d6a9ce7f50",
        "nome": "comercio_test1",
        "attributes": {}
    }

]


CARDAPIO = {
    "_id": "6b6aae29176271992b0278509f15a63900f1f1a9",
    "created_at": 1631415578.674395,
    "destaques": [],
    "produtos": []
}


COMERCIO = {
    "_id": "6b6aae29176271992b0278509f15a63900f1f1a9",
    "attributes": {
        "cnpj": "12384140",
        "email": "teste@gmail.com",
        "endereco": "rua dos pombos",
        "horarios": [],
        "link_imagem": "vazio",
        "redes_sociais": [],
        "tags": [],
        "telefone": "839618171"
    },
    "cardapio": "6b6aae29176271992b0278509f15a63900f1f1a9",
    "created_at": 1631415578.674395,
    "nome": "solanches"
}


COMERCIOS = [
    {
        "_id": "1d7a8e01d2c90840c2f7c0801ae881d6a9ce7f48",
        "nome": "comercio1",
        "attributes": {"telefone": "37", "categoria":"1"}
    },
    {
        "_id": "2d7a8e01d2c90840c2f7c0801ae881d6a9ce7f48",
        "nome": "comercio2",
        "attributes": {"telefone": "38", "categoria":"2"}
    },
    {
        "_id": "3d7a8e01d2c90840c2f7c0801ae881d6a9ce7f48",
        "nome": "comercio3",
        "attributes": {"telefone": "39", "categoria":"3"}
    }
]

COMERCIO_EDITADO = {
    "_id": "1d7a8e01d2c90840c2f7c0801ae881d6a9ce7f48",
    "nome": "comercio1",
    "attributes": {"telefone": "4002-8922", "categoria": "1"}
}

PRODUTO = {
    "_id": "d763e108f053ad2354ff9285b70c48cfc770d9f7",
    "attributes": {
        "categoria": "sa",
        "descricao": "descrição do produto de teste1",
        "imagem": "link de imagem",
        "preco": 20.5
    },
    "created_at": 1631415611.4404533,
    "nome": "produto"
}


CARDAPIO = {

    "_id": "1d7a8e01d2c90840c2f7c0801ae881d6a9ce7f48",
    "created_at": 1631415578.674395,
    "destaques": [],
    "produtos": [
        "d763e108f053ad2354ff9285b70c48cfc770d9f7"
    ]
}

PRODUTO_EDITADO = {
    "_id": "d763e108f053ad2354ff9285b70c48cfc770d9f7",
    "attributes": {
        "categoria": "sa",
        "descricao": "descrição atualizada",
        "imagem": "link de imagem",
        "preco": 20.5
    },
    "created_at": 1631415611.4404533,
    "nome": "produto"
}

COMERCIO_NO_BD = {
    "_id" : "tested01f3670d20bb66c0f0711dee397c61cb84",
    "nome" : "comercio teste",
    "password" : "minha senha",
    "attributes" : {
        "endereco" : "Av. Brasília",
        "categoria" : "Lanchonete",
        "horarios" : [1, 2, 3]
    },
    "created_at" : 1631804210.31025,
    "cardapio" : "fcb22d01f3670d20bb66c0f0711dee397c61cb84"
}

COMERCIO = {
    "id": "3671361e6d5dc1ee674156beed67b1fd",
    "attributes": {
         "endereco": "orestes fialho",
         "horarios": "11h-22h"
    },
    "password": "3671361e6d5dc1ee674156beed67b1fd",
    "created_at": 1628721657.488885,
    "nome": "lanche_feliz"
}

COMERCIO_TESTE = {
    "_id": "idtestecomercio",
    "nome": "comercio2",
    "attributes": {"telefone": "40", "categoria":"4"}
}

PRODUTO_TESTE = {
    "_id": "idtesteproduto",
    "nome": "produto comercio2",
    "attributes": {"preco": "40"},
}

PRODUTOS_TESTE = [
    {
        "_id": "2d7a8e01d2c90840c2f7c0801ae881d6a9ce7f50",
        "nome": "produto comercio2",
        "attributes": {"preco": "45"}
    },
    {
        "_id": "2d7a8e01d2c90840c2f7c0801ae881d6a9ce7f51",
        "nome": "produto comercio2",
        "attributes": {"preco": "45"}
    },
    {
        "_id": "2d7a8e01d2c90840c2f7c0801ae881d6a9ce7f52",
        "nome": "produto comercio2",
        "attributes": {"preco": "45"}
   }
]

PRODUTO_NO_BD = {
    "_id" : "tested01f3670d20bb66c0f0711dee397c61cb84",
    "nome" : "comercio teste",
    "created_at" : 1631804210.31025,
    "attributes": {"preco": "45"}
}


CARDAPIO_TESTE = {
    "_id": "idteste",
    "produtos": [],
    "destaques": [],
    "categorias": []
}

CARDAPIO_MODELS_TEST = {
    "_id": "id do cardapio",
    "categorias": [],
    "created_at": 1632159992.3423245,
    "destaques": [],
    "produtos": []
}

PRODUTO_CARDAPIO_MODELS_TEST = {
    "_id": "id do produto",
    "attributes": {
        "categoria": "nome da categoria"
    },
    "created_at": 1632249299.7731967,
    "nome": "nome do produto"
}

CARDAPIO_COM_PRODUTO_MODELS_TEST = {
    "_id": "id do cardapio",
    "categorias": [],
    "created_at": 1632159992.3423245,
    "destaques": [],
    "produtos": ["id do produto"]
}

CARDAPIO_COM_DESTAQUE_MODELS_TEST = {
    "_id": "id do cardapio",
    "categorias": [],
    "created_at": 1632159992.3423245,
    "destaques": ["id do produto"],
    "produtos": ["id do produto"]
}

CARDAPIO_COM_CATEGORIA_MODELS_TEST = {
    "_id": "id do cardapio",
    "categorias": ["nome da categoria"],
    "created_at": 1632159992.3423245,
    "destaques": [],
    "produtos": []
}
