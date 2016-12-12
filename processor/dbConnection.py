from pymongo import MongoClient

class DBConnection:
    dbClient = MongoClient('mongodb://localhost:27017/')
    database = dbClient['cars-database']
    collection = database['cars-collection']

    def __init__(self, collection=None, database=None, url=None):
        '''Set up default database or take custom params'''
        if url is not None:
            self.dbClient = MongoClient(url)
        if database is not None:
            self.database = self.dbClient[database]
        if collection is not None:
            self.collection = self.database[collection]

    #Generator/Cursor CRUD Returns
    def get_all_docs_generator(self):
        '''Returns a Generator to all documents'''
        return self.collection.find()

    def get_all_docs_with_photos_urls(self):
        '''Returns a Generator with documentst that contain'''
        return self.collection.find({"imgs_indv_url":{"$exists":True}})

    #Get Local Python Refs to docs:
    def create_doc(self, doc):
        '''Inserts Exactly One Document'''
        self.collection.save(doc)

    def create_docs(self, docs):
        '''Takes an array of doc objects'''
        self.collection.insert_many(docs)

    def remove_docs(self, doc):
        '''Removes many docs'''
        self.collection.delete_many({"_id":doc['_id']})

    def get_all_docs_to_local_reference(self):
        '''Returns a list of all documents. Use carefully!'''
        list_of_docs = []
        for docs in self.collection.find():
            list_of_docs.append(docs)
        return list_of_docs

    def docExists(self, doc):
        '''Checks if a document exists by a unique combination of year, model, and make props. Returns a boolean.'''
        results = self.collection.find_one({"year":doc['year'], "model":doc['model'], "make":doc['make']})
        return results != None

    def update_one_doc(self, doc):
        '''Updates a document by id.'''
        self.collection.update_one({'_id': doc['_id']}, {"$set": doc}, upsert=False)
    
    # def finderrors(self):
    #     cursor = self.collection.find({'source-id':1}, modifiers={"$snapshot": True})
    #     return cursor


