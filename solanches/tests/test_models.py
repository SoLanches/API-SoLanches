from unittest import mock
import copy

import pytest

from . data_test import COMERCIO_NO_BD


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
        comercio_id = um_comercio["_id"]
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
        comercio_id = um_comercio["_id"]
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
