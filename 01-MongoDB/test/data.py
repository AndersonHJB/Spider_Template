# 数据存储函数，Mongodb
import pymongo
from faker import Faker
import random
def judge(insert_data, collection):
    if isinstance(insert_data, list):
        collection.insert_many(insert_data)
    elif isinstance(insert_data, dict):
        collection.insert_one(insert_data)
    else:
        print("插入的数据不支持，函数：judge！")

def write_mongodb(db_name="default_db", table_name="default_table", insert_data="None"):
    print("正在连接数据库...")
    client = pymongo.MongoClient(host="localhost", port=27017)
    print("连接成功!")
    # client = pymongo.MongoClient("mongodb://localhost:27017/")
    # db = client.test
    print("创建数据库...")
    db = client[db_name]
    print(f"数据库: {db_name} 创建成功!")
    # collection = db.students
    print("创建数据库表...")
    collection = db[table_name]
    print(f"{table_name} 表创建成功!")
    print(f"use insert one function, insert data: {insert_data}")
    # collection.insert_one(insert_data)
    judge(insert_data, collection)
    print("插入成功!")

def generate_data():
    """数据生成，便于测试"""
    faker = Faker()
    data_lst = []
    for i in range(100):
        dict_data = {
            "id": i,
            "name": faker.name(),
            "email": faker.email(),
            "address": faker.address(),
            "age": random.randint(18, 23),
        }
        data_lst.append(dict_data)
    return data_lst

if __name__ == '__main__':
    # data = {
    #     "name": "aiyc",
    #     "age": 19,
    #     "school": "CHINA"
    # }
    for d in generate_data():
        write_mongodb(db_name="20220506-four", 
            table_name="day", 
            insert_data=d)


