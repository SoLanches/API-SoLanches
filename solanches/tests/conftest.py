from unittest import mock

import pytest
import mongomock


DB_TEST = mongomock.MongoClient().tests_solanches

@pytest.fixture(scope='session', autouse=True)
def teardown():
    with mock.patch('solanches.connect2db.DB', DB_TEST):
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
    with mock.patch('solanches.models.DB', DB_TEST):
        from solanches import controller
        yield controller
        from solanches import models
        models.DB.comercio.delete_many({})
        models.DB.cardapio.delete_many({})
        models.DB.produto.delete_many({})
