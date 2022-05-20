import json

import pymongo
from bson.objectid import ObjectId
def read_mongodb(db_name="default_db", table_name="default_table"):
    print("正在连接数据库...")
    client = pymongo.MongoClient(host="localhost", port=27017)
    print("连接成功!")
    # client = pymongo.MongoClient("mongodb://localhost:27017/")
    # db = client.test
    print("连接数据库...")
    db = client[db_name]
    print(f"数据库: {db_name} 连接成功。")
    # collection = db.students
    print("连接指定数据库表...")
    collection = db[table_name]
    print(f"{table_name} 表连接成功!")
    # r = collection.find_one({'_id': ObjectId('62746a6e6e85582fac7038a4')})
    # for id in range(100):
    #     r = collection.find_one({"id": id})
    #     print(r)
    #     with open("data_txt.txt", "a+", encoding="utf-8")as f:
    #         print(f.write(str(r) + "\n"))
    # r = collection.find({"age": {"$gt": 18}})
    r = collection.find({"name": {"$regex": '^T.*'}})
    print(r)
    # # print(r)
    for i in r:
        print(i)
if __name__ == '__main__':
    read_mongodb(db_name="20220506-four", table_name="day")