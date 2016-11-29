from pymongo import MongoClient

class DBConnection:
    dbClient = MongoClient('mongodb://localhost:27017/')
    database = dbClient['cars-database']
    collection = database['cars-collection']
    list_of_items_added = []

    def create_doc(self, doc):
        newest_id = self.collection.insert_one(doc)
        self.list_of_items_added.append(newest_id)

    def create_docs(self, docs):
        self.collection.insert_many(docs)

    def remove_doc(self, doc):
        self.collection.delete_many({"_id":doc['_id']})
        self.list_of_items_added.remove(doc['_id'])

    def get_all_docs(self):
        list_of_docs = []
        for docs in self.collection.find():
            list_of_docs.append(docs)
        return list_of_docs

    def update_one_doc(self, doc):
        self.collection.update_one({'_id': doc['_id']}, doc, upsert=False)



