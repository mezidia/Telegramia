# TODO: change lists to tuples
from pymongo import results, MongoClient


class Client:
    """
    Class for manipulating MongoDB cluster
    """

    def __init__(self, password, db_name: str = 'Telegramia'):
        """
        Initializing client object with access to database
        :param password: password to account
        :param db_name: name of database in current cluster
        """
        cluster = MongoClient(f'mongodb+srv://mezgoodle:{password}@telegramia.jkq5x.mongodb.net/'
                              f'telegramia?retryWrites=true&w=majority')
        self.db = cluster[db_name]

    def insert(self, data: dict, collection_name: str) -> results.InsertOneResult:
        """
        Method for inserting data in collection
        :param collection_name: name of the collection
        :param data: dictionary with field name and value
        :return: result of inserting
        """
        try:
            return self.db[collection_name].insert_one(data)
        except Exception as e:
            print('Error:', e)

    def get(self, query: dict, collection_name: str) -> dict:
        """
        Method for getting data from collection
        :param collection_name: name of the collection
        :param query: dictionary with field name and value
        :return: the document that matches the query
        """
        try:
            return self.db[collection_name].find_one(query)
        except Exception as e:
            print('Error:', e)

    def get_all(self, collection_name: str, query: dict = None) -> list:
        """
        Method for getting all data from collection
        :param collection_name: name of the collection
        :param query: dictionary with field name and value
        :return: the list of documents
        """
        if query is None:
            query = {}
        try:
            return self.db[collection_name].find(query)
        except Exception as e:
            print('Error:', e)

    def update(self, query: dict, data: dict, collection_name: str) -> results.UpdateResult:
        """
        Method for updating data in collection
        :param collection_name: name of the collection
        :param query: dictionary with field name and value
        :param data: dictionary with the old field name in document and the new value
        :return: result of updating
        """
        try:
            return self.db[collection_name].update_one(query, {'$set': data})
        except Exception as e:
            print('Error:', e)

    def delete(self, query: dict, collection_name: str) -> results.DeleteResult:
        """
        Method for deleting data in collection
        :param collection_name: name of the collection
        :param query: dictionary with field name and value
        :return: result of deleting
        """
        try:
            return self.db[collection_name].delete_one(query)
        except Exception as e:
            print('Error:', e)
