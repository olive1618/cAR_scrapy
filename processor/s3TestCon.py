import boto3
#import os
#import re
import urllib.request
#import requests

#Get File from URL and load into memory...push it to s3 right away.
#***********************
s3 = boto3.client('s3')
URL = 'http://blog.caranddriver.com/wp-content/uploads/2016/11/2017-Volkswagen-Golf-R-101-876x535.jpg'
with urllib.request.urlopen(URL) as response:
    rawImg = response
    s3.upload_fileobj(rawImg, "car-raw-photos", 'testStream.jpg')

# Create Local file from URL Image::
#***********************
# r = requests.get(URL, stream=True)
# if r.status_code == 200:
#     with open('test.jpg', 'wb') as f:
#         for chunk in r.iter_content(1024):
#             f += chunk

#Get all jpgs from a folder and upload them::
#***********************
#files = [f for f in os.listdir('photos') if re.match('[\w]+.*\.jpg', f)]
#print(files)
# for idx,file in enumerate(files):
#     print(idx)
#     fileUri = "photos/" + file
#     fileKey = "t" + str(idx) + ".jpg"
#     s3.upload_file(fileUri, "car-raw-photos", fileKey)
