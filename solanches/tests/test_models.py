from unittest import mock
import copy

import pytest

from . data_test import *


class TestComercio:
    
    @pytest.fixture
    def um_comercio(self):
        return copy.deepcopy(COMERCIO_NO_BD)

    @pytest.fixture
    def comercio_no_bd(self, db_test):
        db_test.comercio.insert_one(COMERCIO_NO_BD)

    @mock.patch('solanches.models.Cardapio.save')
    def test_create_and_save_comercio(self, mock_cardapio_save, models):
        nome = "Nome do comercio"
        password = "password"
        attributes = {"key1": "value1", "key2": ["value1", "value2"]}
        cardapio_id = "id do cardapio"
        mock_cardapio_save.return_value = cardapio_id

        novo_comercio = models.Comercio(nome, password, attributes)
        novo_comercio.save()
        comercio_saved = novo_comercio.to_dict()

        assert comercio_saved.get("_id")
        assert comercio_saved.get("created_at")
        assert comercio_saved.get("cardapio")
        assert comercio_saved.get("cardapio") == cardapio_id
        assert "password" not in comercio_saved
        assert comercio_saved.get("nome") == nome
        assert comercio_saved.get("attributes") == attributes

    def test_get_comercio_by_id(self, models, um_comercio, comercio_no_bd):
        comercio_id = um_comercio.get("_id")
        um_comercio.pop("password")
        comercio = models.Comercio.get_by_id(comercio_id)
        assert comercio == um_comercio
        assert "password" not in comercio

    def test_get_comercio_by_id_nao_cadastrado(self, models, comercio_no_bd):
        comercio_id = "id aleatório"
        comercio = models.Comercio.get_by_id(comercio_id)
        assert not comercio

    def test_get_comercio_by_name(self, models, um_comercio, comercio_no_bd):
        comercio_name = um_comercio["nome"]
        um_comercio.pop("password")
        comercio = models.Comercio.get_by_name(comercio_name)
        assert comercio == um_comercio
        assert "password" not in comercio

    def test_get_comercio_by_name_nao_cadastrado(self, models, comercio_no_bd):
        comercio_name = ""
        comercio = models.Comercio.get_by_name(comercio_name)
        assert not comercio

    def test_get_all_comercios(self, models, um_comercio, comercio_no_bd):
        um_comercio.pop("password")
        result = models.Comercio.get_all()
        assert isinstance(result, list)
        assert um_comercio in result
        assert all("password" not in comercio for comercio in result)

    def test_get_all_comercios_vazio(self, models):
        result = models.Comercio.get_all()
        assert isinstance(result, list)
        assert result == []

    def test_update_comercio_attributes(self, models, um_comercio, comercio_no_bd, db_test):
        comercio_id = um_comercio.get("_id")
        new_attributes = {"attributes": {"at1": "v1", "at2": "v2"}}
        models.Comercio.update(comercio_id, new_attributes)
        query = {"_id": comercio_id}
        result = db_test.comercio.find_one(query)
        updated_attributes = result.get("attributes")
        assert all(attr in new_attributes.get("attributes") for attr in updated_attributes)

    @mock.patch("solanches.models.Comercio.get_by_name")
    @mock.patch("solanches.models.Cardapio.get_by_id")
    def test_get_cardapio(self, mock_get_cardapio_by_id, mock_get_comercio_by_name, models, um_comercio, comercio_no_bd):
        comercio_nome = um_comercio["nome"]
        cardapio_id = um_comercio["cardapio"]
        mock_get_comercio_by_name.return_value = um_comercio
        models.Comercio.get_cardapio(comercio_nome)
        param = mock_get_cardapio_by_id.call_args[0][0]
        assert param == cardapio_id

    @mock.patch("solanches.models.Comercio.get_cardapio")
    @mock.patch("solanches.models.Cardapio.add_produto")
    def test_add_produto(self, mock_cardapio_add_produto, mock_get_cardapio, models, um_comercio, comercio_no_bd):
        comercio_nome = um_comercio["nome"]
        cardapio_id = um_comercio["cardapio"]
        produto_data = {"nome": "produto", "attributes": {"at1": "v1"}}

        mock_get_cardapio.return_value = {"_id": cardapio_id}
        result = models.Comercio.add_produto(comercio_nome, produto_data)
        get_cardapio_param = mock_get_cardapio.call_args[0][0]
        cardapio_add_produto_params = mock_cardapio_add_produto.call_args[0]

        assert get_cardapio_param == comercio_nome
        assert cardapio_add_produto_params == (cardapio_id, produto_data)
        assert isinstance(result, mock.Mock)

    @mock.patch("solanches.models.Comercio.get_by_name")
    @mock.patch("solanches.models.Cardapio.get_produto")
    def test_get_produto(self, mock_cardapio_get_produto, mock_get_comercio_by_name, models, um_comercio, comercio_no_bd):
        produto_id = "id irrelevante"
        comercio_nome = um_comercio["nome"]
        cardapio_id = um_comercio["cardapio"]
        mock_get_comercio_by_name.return_value = um_comercio

        result = models.Comercio.get_produto(comercio_nome, produto_id)
        get_comercio_by_name_param = mock_get_comercio_by_name.call_args[0][0]
        get_produto_cardapio_param = mock_cardapio_get_produto.call_args[0]

        assert get_comercio_by_name_param == comercio_nome
        assert get_produto_cardapio_param == (cardapio_id, produto_id)
        assert isinstance(result, mock.Mock)

    @mock.patch("solanches.models.Comercio.get_by_name")
    @mock.patch("solanches.models.Cardapio.get_produtos")
    def test_get_produtos(self, mock_cardapio_get_produtos, mock_get_comercio_by_name, models, um_comercio, comercio_no_bd):
        comercio_nome = um_comercio["nome"]
        cardapio_id = um_comercio["cardapio"]
        mock_get_comercio_by_name.return_value = um_comercio

        result = models.Comercio.get_produtos(comercio_nome)
        get_comercio_by_name_param = mock_get_comercio_by_name.call_args[0][0]
        get_produtos_cardapio_param = mock_cardapio_get_produtos.call_args[0][0]

        assert get_comercio_by_name_param == comercio_nome
        assert get_produtos_cardapio_param == cardapio_id
        assert isinstance(result, mock.Mock)

    @mock.patch("solanches.models.Comercio.get_by_name")
    @mock.patch("solanches.models.Cardapio.get_produtos_ids")
    def test_get_produtos_ids(self, mock_cardapio_get_produtos_ids, mock_get_comercio_by_name, models, um_comercio, comercio_no_bd):
        comercio_nome = um_comercio["nome"]
        cardapio_id = um_comercio["cardapio"]
        mock_get_comercio_by_name.return_value = um_comercio

        result = models.Comercio.get_produtos_ids(comercio_nome)
        get_comercio_by_name_param = mock_get_comercio_by_name.call_args[0][0]
        get_produtos_ids_cardapio_param = mock_cardapio_get_produtos_ids.call_args[0][0]

        assert get_comercio_by_name_param == comercio_nome
        assert get_produtos_ids_cardapio_param == cardapio_id
        assert isinstance(result, mock.Mock)

    @mock.patch("solanches.models.Comercio.get_by_name")
    @mock.patch("solanches.models.Cardapio.get_destaques")
    def test_get_destaques(self, mock_cardapio_get_destaques, mock_get_comercio_by_name, models, um_comercio, comercio_no_bd):
        comercio_nome = um_comercio["nome"]
        cardapio_id = um_comercio["cardapio"]
        mock_get_comercio_by_name.return_value = um_comercio

        result = models.Comercio.get_destaques(comercio_nome)
        get_comercio_by_name_param = mock_get_comercio_by_name.call_args[0][0]
        get_destaques_cardapio_param = mock_cardapio_get_destaques.call_args[0][0]

        assert get_comercio_by_name_param == comercio_nome
        assert get_destaques_cardapio_param == cardapio_id
        assert isinstance(result, mock.Mock)

    @mock.patch("solanches.models.Comercio.get_by_name")
    @mock.patch("solanches.models.Cardapio.add_destaque")
    def test_add_destaque(self, mock_cardapio_add_destaques, mock_get_comercio_by_name, models, um_comercio, comercio_no_bd):
        comercio_nome = um_comercio["nome"]
        cardapio_id = um_comercio["cardapio"]
        novo_destaque = "novo destaque"
        mock_get_comercio_by_name.return_value = um_comercio

        models.Comercio.add_destaque(comercio_nome, novo_destaque)
        get_comercio_by_name_param = mock_get_comercio_by_name.call_args[0][0]
        add_destaques_cardapio_params = mock_cardapio_add_destaques.call_args[0]

        assert get_comercio_by_name_param == comercio_nome
        assert add_destaques_cardapio_params == (cardapio_id, novo_destaque)

    @mock.patch("solanches.models.Cardapio.update_produto")
    def test_update_produto(self, mock_cardapio_update_produto, models, um_comercio, comercio_no_bd):
        produto_id = "id de um produto"
        fields = {"campo": "valor"}
        models.Comercio.update_produto(produto_id, fields)
        update_produto_cardapio_params = mock_cardapio_update_produto.call_args[0]
        assert update_produto_cardapio_params == (produto_id, fields)
    
    @mock.patch("solanches.models.Cardapio.remove_cardapio")
    @mock.patch("solanches.models.Comercio.id")
    def test_remove_comercio(self, mock_comercio_id, mock_remove_cardapio, models, um_comercio, db_test, comercio_no_bd):
        comercio_nome = um_comercio["nome"]
        cardapio_id = um_comercio["cardapio"]
        mock_comercio_id.return_value = cardapio_id

        result = models.Comercio.remove_comercio(comercio_nome)
        comercio_id_param = mock_comercio_id.call_args[0][0]
        remove_cardapio_param = mock_remove_cardapio.call_args[0][0]

        assert comercio_id_param == comercio_nome
        assert remove_cardapio_param == cardapio_id
        assert result

    def test_verify_password_senha_correta(self, models, um_comercio, db_test, comercio_no_bd):
        comercio_nome = um_comercio["nome"]
        senha = um_comercio["password"]
        result = models.Comercio.verify_password(comercio_nome, senha)
        assert result

    def test_verify_password_senha_incorreta(self, models, um_comercio, db_test, comercio_no_bd):
        comercio_nome = um_comercio["nome"]
        senha = "senha incorreta"
        result = models.Comercio.verify_password(comercio_nome, senha)
        assert not result

    @mock.patch("solanches.models.Cardapio.remove_produto")
    @mock.patch("solanches.models.Comercio.get_by_name")
    def test_remove_produto(self, mock_comercio_get_by_name, mock_remove_produto_cardapio, models, um_comercio, db_test, comercio_no_bd):
        comercio_nome = um_comercio["nome"]
        cardapio_id = um_comercio["cardapio"]
        produto_id = "id do produto"
        mock_comercio_get_by_name.return_value = um_comercio

        models.Comercio.remove_produto(comercio_nome, produto_id)
        remove_produto_cardapio_params = mock_remove_produto_cardapio.call_args[0]
        assert remove_produto_cardapio_params == (cardapio_id, produto_id)
    
    @mock.patch("solanches.models.Cardapio.remove_produto_destaques")
    @mock.patch("solanches.models.Comercio.get_by_name")
    def test_remove_produto_destaques(self, mock_comercio_get_by_name, mock_remove_produto_cardapio, models, um_comercio, db_test, comercio_no_bd):
        comercio_nome = um_comercio["nome"]
        cardapio_id = um_comercio["cardapio"]
        produto_id = "id do produto"
        mock_comercio_get_by_name.return_value = um_comercio

        models.Comercio.remove_produto_destaques(comercio_nome, produto_id)
        remove_produto_cardapio_params = mock_remove_produto_cardapio.call_args[0]
        assert remove_produto_cardapio_params == (cardapio_id, produto_id)

    @mock.patch("solanches.models.Comercio.get_by_name")
    def test_get_categoria(self, mock_comercio_get_by_name, models, um_comercio):
        comercio_nome = um_comercio["nome"]
        categoria = um_comercio.get("attributes").get("categoria")
        mock_comercio_get_by_name.return_value = um_comercio
        result = models.Comercio.get_categoria(comercio_nome)
        assert result == categoria

    @mock.patch("solanches.models.Cardapio.get_produto_categoria")
    def test_get_produto_categoria(self, mock_cardapio_get_produto_categoria, models, um_comercio):
        produto_id = "id do produto"
        expected_return = "categoria"
        mock_cardapio_get_produto_categoria.return_value = expected_return
        result = models.Comercio.get_produto_categoria(produto_id)
        assert result == expected_return
    
    @mock.patch("solanches.models.Comercio.get_by_name")
    @mock.patch("solanches.models.Cardapio.add_categoria")
    def test_add_categoria(self, mock_cardapio_add_categoria, mock_get_comercio_by_name, models, um_comercio, comercio_no_bd):
        comercio_nome = um_comercio["nome"]
        cardapio_id = um_comercio["cardapio"]
        nova_categoria = "nova categoria"
        mock_get_comercio_by_name.return_value = um_comercio

        models.Comercio.adiciona_categoria(comercio_nome, nova_categoria)
        get_comercio_by_name_param = mock_get_comercio_by_name.call_args[0][0]
        add_categoria_cardapio_params = mock_cardapio_add_categoria.call_args[0]

        assert get_comercio_by_name_param == comercio_nome
        assert add_categoria_cardapio_params == (cardapio_id, nova_categoria)

    @mock.patch("solanches.models.Cardapio.remove_categoria")
    @mock.patch("solanches.models.Comercio.get_by_name")
    def test_remove_categoria(self, mock_comercio_get_by_name, mock_cardapio_remove_categoria, models, um_comercio, db_test, comercio_no_bd):
        comercio_nome = um_comercio["nome"]
        cardapio_id = um_comercio["cardapio"]
        categoria = "categoria"
        mock_comercio_get_by_name.return_value = um_comercio

        models.Comercio.remove_categoria(comercio_nome, categoria)
        remove_categoria_cardapio_params = mock_cardapio_remove_categoria.call_args[0]
        assert remove_categoria_cardapio_params == (cardapio_id, categoria)

    @mock.patch("solanches.models.Cardapio.get_categorias")
    @mock.patch("solanches.models.Comercio.get_by_name")
    def test_get_cardapio_categorias(self, mock_comercio_get_by_name, mock_cardapio_get_categorias, models, um_comercio, db_test, comercio_no_bd):
        comercio_nome = um_comercio["nome"]
        cardapio_id = um_comercio["cardapio"]
        expected_result = ["c1", "c2"]
        mock_comercio_get_by_name.return_value = um_comercio
        mock_cardapio_get_categorias.return_value = expected_result

        result = models.Comercio.get_cardapio_categorias(comercio_nome)
        get_categorias_cardapio_params = mock_cardapio_get_categorias.call_args[0][0]
        assert get_categorias_cardapio_params == cardapio_id
        assert result == expected_result

class TestCardapio:

    @pytest.fixture
    def um_produto(self):
        return copy.deepcopy(PRODUTO_CARDAPIO_MODELS_TEST)

    @pytest.fixture
    def um_cardapio(self):
        return copy.deepcopy(CARDAPIO_MODELS_TEST)

    @pytest.fixture
    def cardapio_no_bd(self, db_test):
        db_test.cardapio.insert_one(CARDAPIO_MODELS_TEST)

    @pytest.fixture
    def um_cardapio_com_produto(self):
        return copy.deepcopy(CARDAPIO_COM_PRODUTO_MODELS_TEST)
    
    @pytest.fixture
    def cardapio_com_produto_no_bd(self, db_test):
        db_test.cardapio.insert_one(CARDAPIO_COM_PRODUTO_MODELS_TEST)

    @pytest.fixture
    def um_cardapio_com_destaque(self):
        return copy.deepcopy(CARDAPIO_COM_DESTAQUE_MODELS_TEST)

    @pytest.fixture
    def cardapio_com_destaque_no_bd(self, db_test):
        db_test.cardapio.insert_one(CARDAPIO_COM_DESTAQUE_MODELS_TEST)
   
    @pytest.fixture
    def um_cardapio_com_categoria(self):
        return copy.deepcopy(CARDAPIO_COM_CATEGORIA_MODELS_TEST)

    @pytest.fixture
    def cardapio_com_categoria_no_bd(self, db_test):
        db_test.cardapio.insert_one(CARDAPIO_COM_CATEGORIA_MODELS_TEST)

    def test_create_and_save_cardapio(self, models):
        cardapio_id = "id do cardapio"

        novo_cardapio = models.Cardapio(cardapio_id)
        novo_cardapio.save()
        cardapio_saved = novo_cardapio.to_dict()

        assert cardapio_saved.get("_id")
        assert cardapio_saved.get("_id") == cardapio_id
        assert cardapio_saved.get("created_at")
        assert isinstance(cardapio_saved.get("categorias"), list)
        assert not cardapio_saved.get("categorias")
        assert isinstance(cardapio_saved.get("destaques"), list)
        assert not cardapio_saved.get("destaques")
        assert isinstance(cardapio_saved.get("produtos"), list)
        assert not cardapio_saved.get("produtos")

    def test_get_cardapio_by_id(self, models, um_cardapio, cardapio_no_bd):
        cardapio_id = um_cardapio.get("_id")
        cardapio = models.Cardapio.get_by_id(cardapio_id)
        assert cardapio == um_cardapio

    def test_get_cardapio_by_id_nao_cadastrado(self, models, cardapio_no_bd):
        cardapio_id = "id nao cadastrado"
        cardapio = models.Cardapio.get_by_id(cardapio_id)
        assert not cardapio

    def test_get_all_cardapios(self, models, um_cardapio, cardapio_no_bd):
        cardapios = models.Cardapio.get_all()
        assert isinstance(cardapios, list)
        assert um_cardapio in cardapios

    def test_get_all_cardapios_vazio(self, models):
        cardapios = models.Cardapio.get_all()
        assert isinstance(cardapios, list)
        assert cardapios == []

    @mock.patch("solanches.models.Produto.save")
    @mock.patch("solanches.models.Cardapio.get_by_id")
    def test_add_produto_cardapio(self, mock_get_cardapio_by_id, mock_save_produto, models, um_cardapio, cardapio_no_bd):
        cardapio_id = um_cardapio.get("_id")
        produto_id = "id do produto"
        produto_data = {"nome": "produto", "attributes": {"at1": "v1"}}
        mock_get_cardapio_by_id.return_value = um_cardapio
        mock_save_produto.return_value = produto_id
        
        result = models.Cardapio.add_produto(cardapio_id, produto_data)
        
        produtos = um_cardapio.get("produtos")
        get_cardapio_by_id_param = mock_get_cardapio_by_id.call_args[0][0]
        assert get_cardapio_by_id_param == cardapio_id
        assert len(produtos) == 1
        assert produto_id in produtos
        assert isinstance(result, models.Produto)
        
    @mock.patch("solanches.models.Produto.remove_produtos")
    @mock.patch("solanches.models.Cardapio.get_produtos")
    def test_remove_cardapio(self, mock_get_produtos, mock_remove_produtos, models, um_cardapio, cardapio_no_bd):
        cardapio_id = um_cardapio.get("_id")
        produtos = um_cardapio.get("produtos")
        mock_get_produtos.return_value = produtos
        
        models.Cardapio.remove_cardapio(cardapio_id)
        
        get_produtos_param = mock_get_produtos.call_args[0][0]
        remove_produtos_param = mock_remove_produtos.call_args[0][0]
        assert get_produtos_param == cardapio_id
        assert remove_produtos_param == produtos

    @mock.patch("solanches.models.Cardapio.get_by_id")
    def test_add_produto_destaque(self, mock_get_cardapio_by_id, models, um_cardapio, cardapio_no_bd):
        cardapio_id = um_cardapio.get("_id")
        produto_id = "id do produto"
        mock_get_cardapio_by_id.return_value = um_cardapio

        models.Cardapio.add_destaque(cardapio_id, produto_id)

        destaques = um_cardapio["destaques"]
        get_cardapio_by_id_param = mock_get_cardapio_by_id.call_args[0][0]
        assert get_cardapio_by_id_param == cardapio_id
        assert len(destaques) == 1
        assert produto_id in destaques

    @mock.patch("solanches.models.Produto.get_by_id")
    @mock.patch("solanches.models.Cardapio.get_by_id")
    def test_get_produto_cardapio(self, mock_get_cardapio_by_id, mock_get_produto_by_id, models, um_cardapio_com_produto, um_produto, cardapio_com_produto_no_bd):
        cardapio_id = um_cardapio_com_produto.get("_id")
        produto_id = um_produto.get("_id")
        mock_get_cardapio_by_id.return_value = um_cardapio_com_produto
        mock_get_produto_by_id.return_value = um_produto
        
        produto = models.Cardapio.get_produto(cardapio_id, produto_id)
        
        get_cardapio_by_id_param = mock_get_cardapio_by_id.call_args[0][0]
        get_produto_by_id_param = mock_get_produto_by_id.call_args[0][0]
        assert get_cardapio_by_id_param == cardapio_id
        assert get_produto_by_id_param == produto_id
        assert produto == um_produto

    @mock.patch("solanches.models.Produto.get_by_id")
    @mock.patch("solanches.models.Cardapio.get_by_id")
    def test_get_produto_cardapio_nao_cadastrado(self, mock_get_cardapio_by_id, mock_get_produto_by_id, models, um_cardapio, cardapio_no_bd):
        cardapio_id = um_cardapio.get("_id")
        produto_id = "id nao cadastrado"
        mock_get_cardapio_by_id.return_value = um_cardapio
        mock_get_produto_by_id.return_value = None
        produto = models.Cardapio.get_produto(cardapio_id, produto_id)
        assert not produto

    @mock.patch("solanches.models.Produto.get_by_id")
    @mock.patch("solanches.models.Cardapio.get_by_id")
    def test_get_produtos_cardapio(self, mock_get_cardapio_by_id, mock_get_produto_by_id, models, um_cardapio_com_produto, um_produto, cardapio_com_produto_no_bd):
        cardapio_id = um_cardapio_com_produto.get("_id")
        produto_id = um_produto.get("_id")
        mock_get_cardapio_by_id.return_value = um_cardapio_com_produto
        mock_get_produto_by_id.return_value = um_produto
        
        produtos = models.Cardapio.get_produtos(cardapio_id)
        
        get_cardapio_by_id_param = mock_get_cardapio_by_id.call_args[0][0]
        get_produto_by_id_param = mock_get_produto_by_id.call_args[0][0]
        assert get_cardapio_by_id_param == cardapio_id
        assert get_produto_by_id_param == produto_id
        assert isinstance(produtos, list)
        assert um_produto in produtos

    @mock.patch("solanches.models.Produto.get_by_id")
    @mock.patch("solanches.models.Cardapio.get_by_id")
    def test_get_produtos_cardapio_vazio(self, mock_get_cardapio_by_id, mock_get_produto_by_id, models, um_cardapio, cardapio_no_bd):
        cardapio_id = um_cardapio.get("_id")
        mock_get_cardapio_by_id.return_value = um_cardapio
        mock_get_produto_by_id.return_value = None
        
        produtos = models.Cardapio.get_produtos(cardapio_id)
        get_cardapio_by_id_param = mock_get_cardapio_by_id.call_args[0][0]
        assert get_cardapio_by_id_param == cardapio_id
        assert isinstance(produtos, list)
        assert produtos == []
    
    @mock.patch("solanches.models.Cardapio.get_by_id")
    def test_get_produtos_ids_cardapio(self, mock_get_cardapio_by_id, models, um_cardapio_com_produto, um_produto, cardapio_com_produto_no_bd):
        cardapio_id = um_cardapio_com_produto.get("_id")
        produto_id = um_produto.get("_id")
        mock_get_cardapio_by_id.return_value = um_cardapio_com_produto
        
        produtos = models.Cardapio.get_produtos_ids(cardapio_id)

        get_cardapio_by_id_param = mock_get_cardapio_by_id.call_args[0][0]
        assert get_cardapio_by_id_param == cardapio_id
        assert isinstance(produtos, list)
        assert produto_id in produtos

    @mock.patch("solanches.models.Cardapio.get_by_id")
    def test_get_produtos_ids_cardapio_vazio(self, mock_get_cardapio_by_id, models, um_cardapio, cardapio_no_bd):
        cardapio_id = um_cardapio.get("_id")
        mock_get_cardapio_by_id.return_value = um_cardapio
        
        produtos = models.Cardapio.get_produtos_ids(cardapio_id)
        
        get_cardapio_by_id_param = mock_get_cardapio_by_id.call_args[0][0]
        assert get_cardapio_by_id_param == cardapio_id
        assert isinstance(produtos, list)
        assert produtos == []

    @mock.patch("solanches.models.Cardapio.get_by_id")
    def test_get_destaques_cardapio(self, mock_get_cardapio_by_id, models, um_cardapio_com_destaque, um_produto, cardapio_com_destaque_no_bd):
        cardapio_id = um_cardapio_com_destaque.get("_id")
        produto_id = um_produto.get("_id")
        mock_get_cardapio_by_id.return_value = um_cardapio_com_destaque
        
        destaques = models.Cardapio.get_destaques(cardapio_id)
        
        get_cardapio_by_id_param = mock_get_cardapio_by_id.call_args[0][0]
        assert get_cardapio_by_id_param == cardapio_id
        assert isinstance(destaques, list)
        assert len(destaques) == 1
        assert produto_id in destaques 

    @mock.patch("solanches.models.Cardapio.get_by_id")
    def test_get_destaques_cardapio_vazio(self, mock_get_cardapio_by_id, models, um_cardapio, cardapio_no_bd):
        cardapio_id = um_cardapio.get("_id")
        mock_get_cardapio_by_id.return_value = um_cardapio
        
        destaques = models.Cardapio.get_destaques(cardapio_id)
        
        get_cardapio_by_id_param = mock_get_cardapio_by_id.call_args[0][0]
        assert get_cardapio_by_id_param == cardapio_id
        assert isinstance(destaques, list)
        assert destaques == []

    @mock.patch("solanches.models.Produto.update")
    def test_update_produto(self, mock_update_produto, models, um_produto):
        produto_id = um_produto.get("_id")
        fields = {"attributes": {"at1": "v1"}}
        
        models.Cardapio.update_produto(produto_id, fields)
        
        update_produto_params = mock_update_produto.call_args[0]
        assert update_produto_params == (produto_id, fields)

    @mock.patch("solanches.models.Produto.remove")
    @mock.patch("solanches.models.Cardapio.get_by_id")
    def test_remove_produto_cardapio(self, mock_get_cardapio_by_id, mock_remove_produto, models, um_cardapio_com_destaque, um_produto, cardapio_com_destaque_no_bd):
        cardapio_id = um_cardapio_com_destaque.get("_id")
        produto_id = um_produto.get("_id")
        mock_get_cardapio_by_id.return_value = um_cardapio_com_destaque
        
        models.Cardapio.remove_produto(cardapio_id, produto_id)
        
        produtos = um_cardapio_com_destaque.get("produtos")
        destaques = um_cardapio_com_destaque.get("destaques")
        get_cardapio_by_id_param = mock_get_cardapio_by_id.call_args[0][0]
        remove_produto_param = mock_remove_produto.call_args[0][0]
        assert get_cardapio_by_id_param == cardapio_id
        assert remove_produto_param == produto_id
        assert isinstance(produtos, list)
        assert produto_id not in produtos
        assert produto_id not in destaques

    @mock.patch("solanches.models.Cardapio.get_by_id")
    def test_remove_produto_destaques_cardapio(self, mock_get_cardapio_by_id, models, um_cardapio_com_destaque, um_produto, cardapio_com_destaque_no_bd):
        cardapio_id = um_cardapio_com_destaque.get("_id")
        produto_id = um_produto.get("_id")
        mock_get_cardapio_by_id.return_value = um_cardapio_com_destaque
        
        models.Cardapio.remove_produto_destaques(cardapio_id, produto_id)
        
        produtos = um_cardapio_com_destaque.get("produtos")
        destaques = um_cardapio_com_destaque.get("destaques")
        get_cardapio_by_id_param = mock_get_cardapio_by_id.call_args[0][0]
        assert get_cardapio_by_id_param == cardapio_id
        assert isinstance(produtos, list)
        assert produto_id in produtos
        assert produto_id not in destaques

    @mock.patch("solanches.models.Produto.get_categoria")
    def test_get_produto_categoria(self, mock_get_categoria_produto, models, um_produto):
        produto_id = um_produto.get("_id")
        categoria = um_produto.get("attributes").get("categoria")
        mock_get_categoria_produto.return_value = categoria
        
        result = models.Cardapio.get_produto_categoria(produto_id)

        get_categoria_produto_param = mock_get_categoria_produto.call_args[0][0]
        assert get_categoria_produto_param == produto_id
        assert result == categoria
    
    @mock.patch("solanches.models.Cardapio.get_by_id")
    def test_add_categoria_cardapio(self, mock_get_cardapio_by_id, models, um_cardapio, cardapio_no_bd):
        cardapio_id = um_cardapio.get("_id")
        categoria = "nome da categoria"
        mock_get_cardapio_by_id.return_value = um_cardapio
        
        models.Cardapio.add_categoria(cardapio_id, categoria)
        
        categorias = um_cardapio.get("categorias")
        get_cardapio_by_id_param = mock_get_cardapio_by_id.call_args[0][0]
        assert get_cardapio_by_id_param == cardapio_id
        assert isinstance(categorias, list)
        assert len(categorias) == 1
        assert categoria in categorias

    @mock.patch("solanches.models.Cardapio.get_by_id")
    def test_remove_categoria_cardapio(self, mock_get_cardapio_by_id, models, um_cardapio_com_categoria, cardapio_com_categoria_no_bd):
        cardapio_id = um_cardapio_com_categoria.get("_id")
        categoria = um_cardapio_com_categoria.get("categorias")[0]
        mock_get_cardapio_by_id.return_value = um_cardapio_com_categoria
        
        models.Cardapio.remove_categoria(cardapio_id, categoria)
        
        categorias = um_cardapio_com_categoria["categorias"]
        get_cardapio_by_id_param = mock_get_cardapio_by_id.call_args[0][0]
        assert get_cardapio_by_id_param == cardapio_id
        assert isinstance(categorias, list)
        assert len(categorias) == 0
        assert categoria not in categorias

    @mock.patch("solanches.models.Cardapio.get_by_id")
    def test_get_categorias_cardapio(self, mock_get_cardapio_by_id, models, um_cardapio_com_categoria, cardapio_com_categoria_no_bd):
        cardapio_id = um_cardapio_com_categoria.get("_id")
        expected_result = um_cardapio_com_categoria.get("categorias")
        mock_get_cardapio_by_id.return_value = um_cardapio_com_categoria
        
        categorias = models.Cardapio.get_categorias(cardapio_id)
        
        get_cardapio_by_id_param = mock_get_cardapio_by_id.call_args[0][0]
        assert get_cardapio_by_id_param == cardapio_id
        assert isinstance(categorias, list)
        assert categorias == expected_result

    @mock.patch("solanches.models.Cardapio.get_by_id")
    def test_get_categorias_cardapio_vazio(self, mock_get_cardapio_by_id, models, um_cardapio, cardapio_no_bd):
        cardapio_id = um_cardapio.get("_id")
        mock_get_cardapio_by_id.return_value = um_cardapio
        
        categorias = models.Cardapio.get_categorias(cardapio_id)
        
        get_cardapio_by_id_param = mock_get_cardapio_by_id.call_args[0][0]
        assert get_cardapio_by_id_param == cardapio_id
        assert isinstance(categorias, list)
        assert categorias == []


class TestProduto:
    
    @pytest.fixture
    def um_produto(self):
        return copy.deepcopy(PRODUTO_NO_BD)

    @pytest.fixture
    def produto_no_bd(self, db_test):
        db_test.produto.insert(PRODUTO_NO_BD)

    def test_create_and_save_produto(self, models):
        nome = "nome do produto"
        attributes = {"preco": "40"}

        novo_produto = models.Produto(nome, attributes)
        novo_produto.save()
        produto_saved = novo_produto.to_dict()

        assert produto_saved.get("_id")
        assert produto_saved.get("created_at")
        assert produto_saved.get("nome") == nome
        assert produto_saved.get("attributes") == attributes

    def test_update_produto(self, models, um_produto, produto_no_bd, db_test):
        produto_id = um_produto.get("_id")
        new_attributes = {"nome": "pastel de frango açucarado", "attributes": {"valor": "3"}}
        models.Produto.update(produto_id, new_attributes)
        
        query = {"_id": produto_id}
        result = db_test.produto.find_one(query)

        updated_name = result.get("nome")
        updated_attributes = result.get("attributes")
        
        assert all(attr in new_attributes.get("attributes") for attr in updated_attributes)
        assert new_attributes.get("nome") == updated_name

    def test_get_by_id(self, models, um_produto, produto_no_bd):
        produto_id = um_produto.get("_id")
        produto = models.Produto.get_by_id(produto_id)
        assert produto == um_produto

    def test_get_produto_by_id_nao_cadastrado(self, models, produto_no_bd):
        produto_id = "id aleatório"
        produto = models.Produto.get_by_id(produto_id)
        assert not produto
    
    def test_remove_produtos(self, models, um_produto, produto_no_bd, db_test):
        id_produto = um_produto.get("_id")
        models.Produto.remove_produtos([id_produto])
        query = {"_id": id_produto}
        result = db_test.produto.find_one(query)
        assert not result
  
    def test_get_all_produtos(self, models, um_produto, produto_no_bd):
        result = models.Produto.get_all()
        assert isinstance(result, list)
        assert um_produto in result

    def test_remove_um_produto(self, models, um_produto, db_test, produto_no_bd):
        produto_id = um_produto.get("_id")
        models.Produto.remove(produto_id)
        query = {"_id": produto_id}
        result = db_test.produto.find_one(query)
        assert not result
    
    @mock.patch("solanches.models.Produto.get_by_id")
    def test_get_categoria(self, mock_produto_get_by_id, models, um_produto, db_test, produto_no_bd):
        produto_id = um_produto.get("_id")
        categoria = um_produto.get("attributes").get("categoria", "")
        mock_produto_get_by_id.return_value = um_produto
        result = models.Produto.get_categoria(produto_id)
        assert result == categoria


class TestBlockList:

    @pytest.fixture
    def um_token(self):
        return "token"

    @pytest.fixture
    def token_no_bd(self, db_test):
        token = {"_id": "token"}
        db_test.block_list.insert_one(token)

    def test_create_and_save_produto(self, models, um_token, db_test):
        token = um_token
        novo_token = models.BlockList(token)
        id_novo_token = novo_token.save()

        query = {"_id": id_novo_token}
        result = db_test.block_list.find_one(query)

        assert result
        assert result.get("_id") == id_novo_token
        assert result.get("date")

    def test_contains_false(self, models):
        token = "token"
        result = models.BlockList.contains(token)
        assert not result

    def test_contains_true(self, models, token_no_bd):
        token = "token"
        result = models.BlockList.contains(token)
        assert result
