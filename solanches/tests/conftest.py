from unittest import mock

import pytest
import mongomock

DB_TEST = mongomock.MongoClient().tests_solanches


@pytest.fixture(scope='session', autouse=True)
def teardown():
    mock.patch('solanches.authenticate.jwt_required', lambda x: x).start()
    mock.patch('solanches.connect2db.DB', DB_TEST).start()
    mock.patch('solanches.models.DB', DB_TEST).start()
    yield


@pytest.fixture
def db_test():
    return DB_TEST


@pytest.fixture
def rest():
    from solanches import rest
    yield rest


@pytest.fixture
def controller():
    from solanches import controller
    yield controller
    from solanches import models
    models.DB.comercio.delete_many({})
    models.DB.cardapio.delete_many({})
    models.DB.produto.delete_many({})


@pytest.fixture
def models():
    from solanches import models
    yield models
    models.DB.comercio.delete_many({})
    models.DB.cardapio.delete_many({})
    models.DB.produto.delete_many({})
