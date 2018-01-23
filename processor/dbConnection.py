from pymongo import MongoClient
import gridfs

class DBConnection:
    #dbClient = MongoClient('mongodb://localhost:27017/')
    dbClient = MongoClient('mongodb://10.0.0.234:27017/?ssl=true&ssl_cert_reqs=CERT_NONE')
    dbClient['admin'].authenticate('ryan', 'C!imbon0', mechanism='SCRAM-SHA-1')
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

    def createImgDoc(self, doc, name):
        db = self.dbClient['photos']
        caranddriver = gridfs.GridFS(db)
        a = caranddriver.put(doc, filename=name)
        return a

        #Get File from db:
        # newDoc = fs.get(a).read()
        # savename = fs.get(a).filename
        # with open('photos2/sp-' + str(savename), 'wb') as f:
        #     f.write(newDoc)

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
        results = self.collection.find_one({"year":doc['year'], "model":doc['model'], "make":doc['make'], "image-original-url":doc['image-original-url']})
        return results != None

    def update_one_doc(self, doc):
        '''Updates a document by id.'''
        self.collection.update_one({'_id': doc['_id']}, {"$set": doc}, upsert=False)

    def update_photo_meta_by_image_name(self, name, id):
        doc = self.collection.find_one({"image-name":name})
        doc['image-id'] = id
        self.collection.update_one({'_id': doc['_id']}, {"$set": doc}, upsert=False)


