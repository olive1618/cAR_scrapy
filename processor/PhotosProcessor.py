import os
import random
import uuid
import re
import urllib.request
import requests
import datetime

import boto3
from dbConnection import DBConnection

#testDb = DBConnection()
class PhotosProcessor:
    dbClient = 'mongodb://localhost:27017/'
    database = 'cars-database'
    collection = 'photos-metadata'

    def __init__(self, collection=None, database=None, url=None):
        '''Set up default database or take custom params'''
        if url is not None:
            self.dbClient = url
        if database is not None:
            self.database = database
        if collection is not None:
            self.collection = collection

    def ProcessAllPhotos(self, toDisk):
        numScrapped = 0
        if toDisk:
            CarMetaDataDB = DBConnection(collection='car_and_driver')
            PhotoMetaDataDB = DBConnection(collection=self.collection)
            rawCursor = CarMetaDataDB.get_all_docs_with_photos_urls()
            for idx, carMetaDoc in enumerate(rawCursor):
                year = carMetaDoc['year']
                make = carMetaDoc['make_url_alias']
                model = carMetaDoc['model_url_alias']
                arrayOfImgs = carMetaDoc.get("imgs_indv_url",None)
                if arrayOfImgs is not None:
                    for img in carMetaDoc['imgs_indv_url']:
                        for k in img.keys():
                            imageSize = k
                            imageUrl = img[k]
                            dupCheck = PhotoMetaDataDB.docExists({
                                "make":make,
                                "year":year,
                                "model":model,
                                "image-original-url":imageUrl
                            })
                            print(dupCheck)
                            if not dupCheck:                            
                                rndName = self.GenerateRandomTag(str(img[k]))
                                doc = {
                                    "year":year,
                                    "make":make,
                                    "model":model,
                                    "image-size":imageSize,
                                    "image-name": rndName + '.jpg',
                                    'image-original-url':imageUrl,
                                    "collection-source":"Car-And-Driver",
                                    'collection-time':datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                }
                                self.ProcessPhotoFromUrlToDisk(imageUrl, rndName)
                                PhotoMetaDataDB.create_doc(doc)
                                numScrapped += 1
                                print(numScrapped)
                                print(idx)
                                print('***')
        else:
            #TODO build the s3 uploader
            pass

    def ProcessPhotoFromUrlToDisk(self, url, name):
        # Create Local file from URL Image::
        #***********************
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            with open('photos/' + name + '.jpg', 'wb') as f:
                for chunk in r.iter_content(1024):
                    if chunk:
                        f.write(chunk)

    def ProcessPhotoFromUrlToS3(self, url, name):
        #Get File from URL and load into memory...push it to s3 right away.
        #***********************
        s3 = boto3.client('s3')
        with urllib.request.urlopen(url) as response:
            rawImg = response
            s3.upload_fileobj(rawImg, "car-raw-photos", name + '.jpg')

    def GetAllPhotosFromDiskAndUploadTos3(self):
        '''Uploads photos from a photos folder to s3'''
        #Get all jpgs from a folder and upload them::
        #***********************
        s3 = boto3.client('s3')
        files = [f for f in os.listdir('photos') if re.match('[\w]+.*\.jpg', f)]
        print(files)
        for idx,file in enumerate(files):
            fileUri = "photos/" + file
            s3.upload_file(fileUri, "car-raw-photos", str(file))

    def GetAllPhotosFromDiskAndUploadToGridFs(self):
        '''Uploads photos from a photos folder to GridFS'''
        #Get all jpgs from a folder and upload them::
        #***********************
        PhotoDB = DBConnection()
        PhotoMetaDataDB = DBConnection(collection=self.collection)

        files = [f for f in os.listdir('photos') if re.match('[\w]+.*\.jpg', f)]
        for idx,file in enumerate(files):
            print(file)
            with open('photos/' + file, 'rb') as f:
                id = PhotoDB.createImgDoc(f, file)
                PhotoMetaDataDB.update_photo_meta_by_image_name(file,id)

    def GenerateRandomTag(self, photoName):
        def uuidCustom():
            seed = random.getrandbits(32)
            while True:
                yield seed
                seed += 1
        unique_sequence = uuidCustom()
        photoName = photoName + str(next(unique_sequence))
        return str(uuid.uuid5(uuid.uuid4(), photoName))
