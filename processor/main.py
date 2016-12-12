from PhotosProcessor import PhotosProcessor

processor = PhotosProcessor()
processor.ProcessAllPhotos(True)
#processor.ProcessPhotoFromUrlToDisk('http://blog.caranddriver.com/wp-content/uploads/2016/11/2017-Volkswagen-Golf-R-101-876x535.jpg', processor.GenerateRandomTag('test'))

# import csv
# import re
# import random
# from dbConnection import DBConnection

# testDb = DBConnection()
# dbc = testDb.finderrors()
# for idx,r in enumerate(dbc):
#     make = r['model']
#     model = r['make']
#     doc = {
#         '_id':r['_id'],
#         'model':model,
#         'make': make,
#         'year': r['year'],
#         'source-id': r['source-id']
#     }
#     testDb.update_one_doc(doc)



# with open("vehicles.csv") as fileobject:
#     r = csv.reader(fileobject, delimiter=',', quotechar='"')
#     for index,row in enumerate(r):
#         if index % 10000 == 0:
#             print(index)
#         doc = {
#             "year":row[63],
#             "make":row[46],
#             "model":row[47],
#             "driveTran":row[24],
#             "transmission":row[57],
#             "engineCylinders":row[22],
#             "engineDisplacement":row[23],
#             "MpgData": row[48],
#             "cityMpg":row[58],
#             "cityMpgAvg":row[59],
#             "highwayMpg":row[60],
#             "highwayMpgAvg": row[61],
#             "seats":row[62],
#             "fuelType":row[30],
#             "createdOn":row[77],
#             "source-id":2
#         }
#         dupCheck = testDb.find_dups(doc)
#         if not dupCheck:
#             testDb.create_doc(doc)
