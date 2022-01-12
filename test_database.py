import sys

from unittest import TestCase

from database import Client
from config import DB_PASSWORD


class Parent:
    client = Client(DB_PASSWORD, 'Tests', 'tokens')
    full_data = {'test_token': 'test_token' + sys.version, 'test_id': 'test_id'}
    data_with_id = {'test_id': 'test_id'}


class TestClient1(TestCase, Parent):
    async def test_insert(self):
        result = await self.client.insert(self.full_data)
        self.assertTrue(result.acknowledged)
        self.assertIsNotNone(result.inserted_id)


class TestClient2(TestCase, Parent):
    async def test_get(self):
        result = await self.client.get({'test_token': 'test_token' + sys.version})
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)
        self.assertEqual(result['test_id'], self.full_data['test_id'])

    async def test_get_all(self):
        result = await self.client.get_all()
        self.assertIsNotNone(result)

    async def test_update(self):
        result = await self.client.update({'test_token': 'test_token' + sys.version}, {'test_token': 'test_token1' +
                                                                                               sys.version})
        self.assertTrue(result.acknowledged)
        self.assertIsNotNone(result.modified_count)
        updated_data = await self.client.get(self.data_with_id)
        self.assertEqual(updated_data['test_token'], 'test_token1' + sys.version)


class TestClient3(TestCase, Parent):
    async def test_delete(self):
        result = await self.client.delete(self.data_with_id)
        self.assertIsNotNone(result)
        self.assertTrue(result.acknowledged)
        data = await self.client.get(self.data_with_id)
        self.assertIsNone(data)
