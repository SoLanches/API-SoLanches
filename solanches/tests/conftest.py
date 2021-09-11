from unittest import mock

import pytest

from solanches.connect2db import MONGO_CLIENT


@pytest.fixture(scope='session', autouse=True)
def teardown():
    with mock.patch('solanches.connect2db.DB', MONGO_CLIENT['tests_solanches']):
        yield
        from solanches import models
        models.DB.comercio.drop()
        models.DB.cardapio.drop()
        models.DB.produto.drop()


@pytest.fixture
def rest():
    with mock.patch('solanches.models.DB', MONGO_CLIENT['tests_solanches']):
        from solanches import rest
        yield rest


@pytest.fixture
def controller():
    with mock.patch('solanches.models.DB', MONGO_CLIENT['tests_solanches']):
        from solanches import controller
        yield controller
        from solanches import models
        models.DB.comercio.delete_many({})
        models.DB.cardapio.delete_many({})
        models.DB.produto.delete_many({})
