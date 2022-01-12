from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import results


class Client:
    """
    Class for manipulating MongoDB cluster
    """

    def __init__(self, password, db_name: str, collection_name: str):
        """
        Initializing client object with access to database
        :param password: password to account
        :param db_name: name of database in current cluster
        :param collection_name: name of collection in current database
        """
        cluster = AsyncIOMotorClient(f'mongodb+srv://mezgoodle:{password}@telegramia.jkq5x.mongodb.net/'
                                     f'telegramia?retryWrites=true&w=majority')
        db = cluster[db_name]
        self.collection = db[collection_name]

    def insert(self, data: dict) -> results.InsertOneResult:
        """
        Method for inserting data in collection
        :param data: dictionary with field name and value
        :return: result of inserting
        """
        try:
            return self.collection.insert_one(data)
        except Exception as e:
            print('Error:', e)

    def get(self, query: dict) -> dict:
        """
        Method for getting data from collection
        :param query: dictionary with field name and value
        :return: the document that matches the query
        """
        try:
            return self.collection.find_one(query)
        except Exception as e:
            print('Error:', e)

    def get_all(self, query: dict = None) -> list:
        """
        Method for getting all data from collection
        :return: the list of documents
        """
        if query is None:
            query = {}
        try:
            return self.collection.find(query)
        except Exception as e:
            print('Error:', e)

    def update(self, query: dict, data: dict) -> results.UpdateResult:
        """
        Method for updating data in collection
        :param query: dictionary with field name and value
        :param data: dictionary with the old field name in document and the new value
        :return: result of updating
        """
        try:
            return self.collection.update_one(query, {'$set': data})
        except Exception as e:
            print('Error:', e)

    def delete(self, query: dict) -> results.DeleteResult:
        """
        Method for deleting data in collection
        :param query: dictionary with field name and value
        :return: result of deleting
        """
        try:
            return self.collection.delete_one(query)
        except Exception as e:
            print('Error:', e)
