import sys

from unittest import TestCase

from utils.db_api.database import Client
from data.config import DB_PASSWORD


class Parent:
    client = Client(DB_PASSWORD, 'Tests')
    full_data = {'test_token': 'test_token' + sys.version, 'test_id': 'test_id'}
    data_with_id = {'test_id': 'test_id'}


class TestClient1(TestCase, Parent):
    def test_insert(self):
        result = self.client.insert(self.full_data, 'tokens')
        self.assertTrue(result.acknowledged)
        self.assertIsNotNone(result.inserted_id)


class TestClient2(TestCase, Parent):
    def test_get(self):
        result = self.client.get({'test_token': 'test_token' + sys.version}, 'tokens')
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)
        self.assertEqual(result['test_id'], self.full_data['test_id'])

    def test_get_all(self):
        result = self.client.get_all('tokens')
        self.assertIsNotNone(result)

    def test_update(self):
        result = self.client.update({'test_token': 'test_token' + sys.version}, {'test_token': 'test_token1' +
                                                                                               sys.version}, 'tokens')
        self.assertTrue(result.acknowledged)
        self.assertIsNotNone(result.modified_count)
        updated_data = self.client.get(self.data_with_id, 'tokens')
        self.assertEqual(updated_data['test_token'], 'test_token1' + sys.version)


class TestClient3(TestCase, Parent):
    def test_delete(self):
        result = self.client.delete(self.data_with_id, 'tokens')
        self.assertIsNotNone(result)
        self.assertTrue(result.acknowledged)
        data = self.client.get(self.data_with_id, 'tokens')
        self.assertIsNone(data)
