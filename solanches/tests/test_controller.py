import pytest

def test_get_comercios_sistema_vazio(controller):
    assert controller.get_comercios() == [];
    
def test_get_comercios_com_sucesso(controller):
    comercio_name = "comercio_test"
    comercio_attributes = {
        "telefone": "98765-4321"
    }

    new_comercio = controller.cadastra_comercio(comercio_name, comercio_attributes)
    result = [new_comercio]
    assert controller.get_comercios() == result;

def test_get_comercio_by_name_cadastrado(controller):
    comercio_name = "comercio_test"
    comercio_attributes = {
        "telefone": "98765-4321"
    }
    new_comercio = controller.cadastra_comercio(comercio_name, comercio_attributes)
    
    assert controller.get_comercio_by_name(comercio_name) == new_comercio

def test_get_comercio_by_name_inexistente(controller):
    with pytest.raises(Exception) as execinfo:
        comercio_name = 'comercio_sem_id'
        controller.get_comercio_by_name(comercio_name)
    assert str(execinfo.value) == f'Erro: comercio com nome {comercio_name} nao cadastrado!'

def test_get_comercio_com_sucesso(controller):
    comercio_name = "comercio_test"
    comercio_attributes = {
        "telefone": "98765-4321"
    }
    new_comercio = controller.cadastra_comercio(comercio_name, comercio_attributes)
    assert controller.get_comercio(new_comercio["_id"]) == new_comercio

def test_get_comercio_inexistente(controller):
    with pytest.raises(Exception) as execinfo:
        id_inexistente = "98765"
        controller.get_comercio(id_inexistente)
    assert str(execinfo.value) == f'Erro: comercio com id {id_inexistente} não cadastrado!'
