from pymongo import MongoClient
import pandas as pd

client = MongoClient(
    "mongodb+srv://tberkane:43QcccltS7Y89I2D@cluster0.07kae.mongodb.net/epfl_courses?retryWrites=true&w=majority")
collection = client.epfl_courses.courses

collection.drop()

l = lambda s: tuple(s.split('/'))

df = pd.read_excel('api/data/INplan2021-2022.xlsx', sheet_name='MASTER',
                   header=None, names=['code', 'name', 'teachers', 'sections', 'credits'], usecols='A:D,U', converters={'teachers': l, 'sections': l}, skiprows=9, nrows=10)

data = df.to_dict(orient='records')

collection.insert_many(data)
