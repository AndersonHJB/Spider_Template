import pymongo
from bson.objectid import ObjectId
import random
import time

from faker import Faker

# student1 = student1 = {"id": "2701111",
# "name": "Jordan",
# "age": 20,
# "gender": "male",
# }

def db(db_name="default_name", table_name="default_table"):
    print("Setting up database and relaying a connection...")
    client = pymongo.MongoClient(host="localhost", port=27017)
    print("Connection successful.")
    # db = client.test
    # collection = db[db_name]
    # print("Creating database...")
    db = client[db_name]
    # print(f"Database: {db_name} successfully created!")

    # print("Setting up database table...")
    collection = db[table_name]
    # print(f"{table_name} successfully created!")
    # print(result)
    # r = collection.find_one({'_id': ObjectId('6269e588f748936926cd54e9')})
    # time.sleep(3)
    r = collection.find({"age": "$gt: 18"})
    for i in r:
        print(i)
    # print(r)
    # for id in range(100):
    #     r = collection.find_one({"id": id})
    #     print(r)
    #     with open("data_txt.txt", "a+", encoding="utf-8") as f:
    #         print(f.write(str(r) + "\n"))

def generate_data():
    faker = Faker()
    data_lst = []
    for i in range(100):
        dict_data = {
            "id": i,
            "name": faker.name(),
            "email": faker.email(),
            "address": faker.address(),
            "age": random.randint(1, 150),
        }
        data_lst.append(dict_data)
    return data_lst



if __name__ == "__main__":
    # data = {
    #     "name": "aiyc",
    #     "grade": 12,
    #     "age": random.randint(1, 150),
    # }
    # db(insert_data=generate_data())
    # db(db_name="today", table_name="table_name", insert_data=generate_data())
    db(db_name="today", table_name="table_name")
    # print(generate_data())