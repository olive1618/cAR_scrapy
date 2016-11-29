#1245
from dbConnection import DBConnection
import random

models = ["BMW", "Audi", "Mercedes", "Ford", "Toyota", "Porsche"]
makes = ["335i","Fiesta", "S650", "SL55", "TT", "R8", "Corolla", "Boxster", "911", "A6"]
year = ["2016","2015", "2014", "2013", "2012", "2011", "2010", "2009", "2008"]

carDoc = []

# for i in range(1000):
#     ranModel = random.choice(models)
#     ranMakes = random.choice(makes)
#     ranYear = random.choice(year)
#     carDoc.append({"model": ranModel, "make":ranMakes, "year": ranYear})
#testDb = DBConnection()
#testDb.create_docs(carDoc)
