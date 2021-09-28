from unittest import mock
import pytest

from . data_test import CARDAPIO, COMERCIO, COMERCIOS, COMERCIO_TESTE, PRODUTO_TESTE, PRODUTOS_TESTE, CARDAPIO_TESTE
from solanches.errors import SolanchesNotFoundError
from solanches.errors import SolanchesBadRequestError


@pytest.fixture
def um_cardapio():
    cardapio = CARDAPIO
    return cardapio


@pytest.fixture
def um_comercio():
    comercio = COMERCIO
    return comercio


@pytest.fixture
def comercios():
    return COMERCIOS


@mock.patch('solanches.controller.Comercio.get_all')
def test_get_comercios_sistema_vazio_has_categories_true(mock_comercio_get_all, controller):
    mock_comercio_get_all.return_value = []
    has_categories = True
    result = controller.get_comercios(has_categories)
    assert isinstance(result, dict)


@mock.patch('solanches.controller._get_comercios_categoria')
@mock.patch('solanches.controller.Comercio.get_all')
def test_get_comercios_sistema_vazio_sem_has_categories(mock_comercio_get_all, mock_get_comercios_categoria, controller):
    mock_comercio_get_all.return_value = []
    result = controller.get_comercios()
    assert result == [];
    assert not mock_get_comercios_categoria.called


@mock.patch('solanches.controller.Comercio.get_categoria')
@mock.patch('solanches.controller.Comercio.get_all')
def test_get_comercios_com_comercios_no_bd_categories_true(mock_comercio_get_all, mock_comercio_get_categoria, controller, comercios):
    mock_comercio_get_all.return_value = comercios
    mock_comercio_get_categoria.return_value = "categoria"
    has_categories = True
    result = controller.get_comercios(has_categories)
    assert isinstance(result, dict)
    assert "categoria" in result
    assert all(comercio in result.get("categoria") for comercio in comercios)


@mock.patch('solanches.controller._get_comercios_categoria')
@mock.patch('solanches.controller.Comercio.get_all')
def test_get_comercios_com_comercios_no_bd_sem_has_categories(mock_comercio_get_all, mock_get_comercios_categoria, controller, comercios):
    mock_comercio_get_all.return_value = comercios
    has_categories = False
    result = controller.get_comercios(has_categories)
    assert isinstance(result, list)
    assert not mock_get_comercios_categoria.called
    assert all(comercio in result for comercio in comercios)


@mock.patch('solanches.controller.Comercio.get_categoria')
@mock.patch('solanches.controller.Comercio.get_all')
def test_get_comercios_com_comercios_no_bd_categories_true(mock_comercio_get_all, mock_comercio_get_categoria, controller, comercios):
    mock_comercio_get_all.return_value = comercios
    mock_comercio_get_categoria.return_value = "categoria"
    has_categories = True
    result = controller.get_comercios(has_categories)
    assert isinstance(result, dict)
    assert "categoria" in result
    assert all(comercio in result.get("categoria") for comercio in comercios)


@mock.patch('solanches.controller.Comercio.get_by_id')
def test_get_comercio_by_id_nao_cadastrado(mock_comercio_by_id, controller):
    id_invalido = "nao estou cadastrado" 
    mock_comercio_by_id.return_value = None
    
    with pytest.raises(SolanchesNotFoundError) as excinfo:
        controller.get_comercio_by_id(id_invalido)
    assert str(excinfo.value.message) == f'Erro: comercio com id {id_invalido} não cadastrado!'


@mock.patch('solanches.controller.Comercio.get_by_id')
def test_get_comercio_by_id_com_id_nao_str(mock_comercio_by_id, controller):
    id_invalido = 123
    with pytest.raises(SolanchesBadRequestError) as excinfo:
        controller.get_comercio_by_id(id_invalido)
    assert str(excinfo.value.message) == f'Erro: comercio com id {id_invalido} inválido!'


@mock.patch('solanches.controller.Comercio.get_by_id')
def test_get_comercio_by_id_valido(mock_comercio_by_id, controller, um_comercio):
    id_valido = "id valido"
    expected_return = um_comercio
    mock_comercio_by_id.return_value = expected_return
    result = controller.get_comercio_by_id(id_valido)
    assert result == expected_return


@mock.patch('solanches.controller.Comercio.get_by_name')
def test_get_comercio_by_name_nao_cadastrado(mock_comercio_by_name, controller):
    nome_invalido = "nao estou cadastrado" 
    mock_comercio_by_name.return_value = None
    
    with pytest.raises(SolanchesNotFoundError) as excinfo:
        controller.get_comercio_by_name(nome_invalido)
    assert str(excinfo.value.message) == f'Erro: comercio com o nome {nome_invalido} não cadastrado!'


@mock.patch('solanches.controller.Comercio.get_by_name')
def test_get_comercio_by_name_com_nome_nao_str(mock_comercio_by_name, controller):
    nome_invalido = 123
    with pytest.raises(SolanchesBadRequestError) as excinfo:
        controller.get_comercio_by_name(nome_invalido)
    assert str(excinfo.value.message) == f'Erro: nome de comercio inválido!'


@mock.patch('solanches.controller.Comercio.get_by_name')
def test_get_comercio_by_name_valido(mock_comercio_by_name, controller, um_comercio):
    nome_valido = "id valido"
    expected_return = um_comercio
    mock_comercio_by_name.return_value = expected_return
    result = controller.get_comercio_by_name(nome_valido)
    assert result == expected_return


@mock.patch('solanches.models.Comercio.get_by_name')
def test_remove_comercio_inexistente(mock_comercio_by_name, controller):
    mock_comercio_by_name.return_value = None
    with pytest.raises(SolanchesNotFoundError) as excinfo:
      comercio_nome = 'comercio_sem_id'
      controller.remove_comercio(comercio_nome)
    assert str(excinfo.value.message) == f'Erro: comercio com o nome {comercio_nome} não cadastrado!'


def test_remove_comercio_nome_invalido(controller):
    with pytest.raises(SolanchesBadRequestError) as excinfo:
        comercio_nome_invalido = None
        controller.remove_comercio(comercio_nome_invalido)
    assert str(excinfo.value.message) == f'Erro: nome de comercio invalido'


@mock.patch('solanches.controller.Comercio.get_by_name')
@mock.patch('solanches.controller.Comercio.get_cardapio')
def test_get_cardapio_sucesso(mock_get_cardapio, mock_comercio_by_name,controller, um_cardapio):
    mock_get_cardapio.return_value = um_cardapio
    mock_comercio_by_name.return_value = um_comercio
    
    nome_comercio = 'solanches'

    result = controller.get_cardapio(nome_comercio)
    assert result == CARDAPIO
    assert isinstance(result, dict)


def test_get_cardapio_by_nome_comercio_invalido(controller):
    nome_invalido = 123
    with pytest.raises(SolanchesBadRequestError) as excinfo:
        controller.get_cardapio(nome_invalido)
    assert str(excinfo.value.message) == 'Erro: nome de comercio inválido!'


@mock.patch('solanches.controller.Comercio.get_by_name')
@mock.patch('solanches.controller.Comercio.get_cardapio')
def test_get_cardapio_by_nome_comercio_valido(mock_get_cardapio, mock_comercio_by_name, controller, um_cardapio, um_comercio):
    mock_get_cardapio.return_value = um_cardapio
    mock_comercio_by_name.return_value = um_comercio
    nome = 'solanches'

    result = controller.get_cardapio(nome)
    
    assert result == um_cardapio
    assert isinstance(result, dict)


@mock.patch('solanches.controller.Comercio.get_cardapio')
def test_get_cardapio_nao_encontrado(mock_get_cardapio, controller):
    mock_get_cardapio.return_value = None
    nome = 'TEXAS'
    with pytest.raises(SolanchesNotFoundError) as excinfo:
         controller.get_cardapio(nome)
    assert str(excinfo.value.message) == 'Erro: comercio com o nome TEXAS não cadastrado!'


@mock.patch('solanches.models.Comercio.get_by_name')
@mock.patch('solanches.models.Comercio.get_produto')
def test_get_produto_by_id_sucesso(mock_get_produto, mock_get_by_name, controller):
    comercio_nome = 'comercio2'
    produto_id = '213123121e'
    mock_get_by_name.return_value = COMERCIO_TESTE
    mock_get_produto.return_value = PRODUTO_TESTE

    result = controller.get_produto(comercio_nome, produto_id)
    assert result == PRODUTO_TESTE


@mock.patch('solanches.models.Comercio.get_by_name')
@mock.patch('solanches.models.Comercio.get_produto')
def test_get_produto_by_id_invalido(mock_get_produto, mock_get_by_name, controller):
    comercio_nome = 'comercio2'
    produto_id = 123
    with pytest.raises(SolanchesBadRequestError) as excinfo:
        controller.get_produto(comercio_nome, produto_id)
    assert str(excinfo.value.message) == "Erro: produto com id inválido!"


@mock.patch('solanches.models.Comercio.get_by_name')
@mock.patch('solanches.models.Comercio.get_produto')
def test_get_produto_by_id_comercio_inexistente(mock_get_produto, mock_get_by_name, controller):
    comercio_nome = 'comercio inexistente'
    produto_id = '213123121e'
    mock_get_by_name.return_value = None
    with pytest.raises(SolanchesNotFoundError) as excinfo:
        controller.get_produto(comercio_nome, produto_id)
    assert str(excinfo.value.message) == f'Erro: comercio com o nome {comercio_nome} não cadastrado!'


@mock.patch('solanches.models.Comercio.get_by_name')
@mock.patch('solanches.models.Comercio.get_produto')
def test_get_produto_by_id_inexistente(mock_get_produto, mock_get_by_name, controller):
    comercio_nome = 'comercio2'
    produto_id = '213123121e'
    mock_get_by_name.return_value = COMERCIO_TESTE
    mock_get_produto.return_value = None
    with pytest.raises(SolanchesNotFoundError) as e:
      comercio_nome = 'comercio_sem_id'
      controller.get_produto(comercio_nome, produto_id)


@mock.patch('solanches.models.Comercio.get_by_name')
@mock.patch('solanches.models.Comercio.get_produtos')
def test_get_produtos_has_categories_false(mock_get_produtos, mock_get_by_name, controller):
    comercio_nome = 'comercio2'
    mock_get_by_name.return_value = COMERCIO_TESTE
    mock_get_produtos.return_value = PRODUTOS_TESTE

    result = controller.get_produtos(comercio_nome, False)
    assert result == PRODUTOS_TESTE
    assert isinstance(result, list)


@mock.patch('solanches.models.Comercio.get_produto_categoria')
@mock.patch('solanches.models.Comercio.get_by_name')
@mock.patch('solanches.models.Comercio.get_produtos')
def test_get_produtos_has_categories_true(mock_get_produtos, mock_get_by_name, mock_get_produto_categoria, controller):
    comercio_nome = 'comercio2'
    mock_get_by_name.return_value = COMERCIO_TESTE
    mock_get_produtos.return_value = PRODUTOS_TESTE
    mock_get_produto_categoria.return_value = "categoria"

    result = controller.get_produtos(comercio_nome, True)
    assert all(produto in result.get("categoria") for produto in PRODUTOS_TESTE)
    assert isinstance(result, dict)


@mock.patch('solanches.models.Comercio.get_by_name')
@mock.patch('solanches.models.Comercio.get_produtos')
def test_get_produtos_comercio_inexistente(mock_get_produto, mock_get_by_name, controller):
    comercio_nome = 'nome qualquer'
    mock_get_by_name.return_value = None
    with pytest.raises(SolanchesNotFoundError) as e:
        controller.get_produtos(comercio_nome)
    assert str(e.value.message) == f'Erro: comercio com o nome {comercio_nome} não cadastrado!'


@mock.patch('solanches.models.Comercio.get_by_name')
@mock.patch('solanches.models.Comercio.remove_comercio')
def test_remove_comercio_sucesso(mock_remove_comercio, mock_get_by_name,  controller):
    comercio_nome = 'comercio_test'
    mock_get_by_name.return_value = {'produtos': []}
    mock_remove_comercio.return_value = 1
    result = controller.remove_comercio(comercio_nome)
    assert result == 1


@mock.patch('solanches.models.Comercio.get_by_name')
def test_adiciona_categoria_comercio_inexistente(mock_get_by_name, controller):
    nome_invalido = "comercioinvalido"
    categoria = "lanches"
    mock_get_by_name.return_value = None
    with pytest.raises(SolanchesNotFoundError) as excinfo:
        controller.adiciona_categoria(nome_invalido, categoria)
    assert str(excinfo.value.message) == f'Erro: comercio com o nome {nome_invalido} não cadastrado!'


@mock.patch('solanches.models.Comercio.get_by_name')
def test_adiciona_categoria_invalida(mock_get_by_name, controller):
    nome_comercio = 'comercio'
    categoria = None
    mock_get_by_name.return_value = COMERCIO_TESTE
    with pytest.raises(SolanchesBadRequestError) as excinfo:
        controller.adiciona_categoria(nome_comercio, categoria)
    assert str(excinfo.value.message) == f'Erro: valor de categoria inválida!'


@mock.patch('solanches.models.Comercio.get_cardapio_categorias')
@mock.patch('solanches.models.Comercio.get_by_name')
def test_adiciona_categoria_existente(mock_get_by_name, mock_get_categorias, controller):
    nome_invalido = 'comercio'
    categoria = 'salgados'
    mock_get_by_name.return_value = COMERCIO_TESTE
    mock_get_categorias.return_value = ['lanches', 'salgados']
    with pytest.raises(SolanchesBadRequestError) as excinfo:
        controller.adiciona_categoria(nome_invalido, categoria)
    assert str(excinfo.value.message) == f'Erro: categoria já cadastrada nesse comércio!'


@mock.patch('solanches.models.Comercio.adiciona_categoria')
@mock.patch('solanches.models.Comercio.get_cardapio')
@mock.patch('solanches.models.Comercio.get_cardapio_categorias')
@mock.patch('solanches.models.Comercio.get_by_name')
def test_adiciona_categoria_sucesso(mock_get_by_name, mock_get_categorias, mock_get_cardapio, mock_add_categoria, controller):
    nome_comercio = "comercio"
    categoria = 'salgados'
    expected_updated_menu = {'produtos': 'Cardápio exemplo','destaques': [], 'categorias': ['lanches', 'salgados']}
    mock_get_by_name.return_value = COMERCIO_TESTE
    mock_get_categorias.return_value = []
    mock_get_cardapio.return_value = expected_updated_menu
    result = controller.adiciona_categoria(nome_comercio, categoria)
    assert result == expected_updated_menu


@mock.patch('solanches.controller.get_cardapio')
@mock.patch('solanches.models.Comercio.get_produtos_ids')
@mock.patch('solanches.models.Comercio.get_by_name')
@mock.patch('solanches.models.Comercio.remove_produto')
def test_remove_produto_sucesso(mock_remove_produto, mock_get_by_name, mock_get_produtos_ids, mock_get_cardapio, controller):
    mock_get_by_name.return_value = COMERCIO_TESTE
    comercio_nome = 'comercio2'
    produto_id = 'idtesteproduto'
    mock_get_produtos_ids.return_value = [PRODUTO_TESTE['_id']]
    mock_get_cardapio.return_value = CARDAPIO_TESTE
    result = controller.remove_produto(comercio_nome, produto_id)
    assert CARDAPIO_TESTE == result


@mock.patch('solanches.models.Comercio.get_produtos_ids')
@mock.patch('solanches.models.Comercio.get_by_name')
def test_remove_produto_fora_comercio(mock_get_by_name, mock_get_produtos_ids, controller):
    mock_get_by_name.return_value = COMERCIO_TESTE
    comercio_nome = 'comercio2'
    produto_id = 'idtesteproduto'
    mock_get_produtos_ids.return_value = []
    with pytest.raises(SolanchesNotFoundError) as e:
        controller.remove_produto(comercio_nome, produto_id)
    assert str(e.value.message) == f'Erro: produto com o id {produto_id} não cadastrado no comercio!'
 

@mock.patch('solanches.models.Comercio.get_by_name')
def test_remove_produto_comercio_inexistente(mock_get_by_name, controller):
    mock_get_by_name.return_value = None
    comercio_nome = 'comercio2'
    produto_id = 'idtesteproduto'
    with pytest.raises(SolanchesNotFoundError) as e:
        controller.remove_produto(comercio_nome, produto_id)
    assert str(e.value.message) == f'Erro: comercio com o nome {comercio_nome} não cadastrado!'
