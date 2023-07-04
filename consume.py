# import requests

# response = requests.get('http://127.0.0.1:8000/food')
# print(response.json())

from pymongo import MongoClient

# Establish a connection to the MongoDB server
client = MongoClient('mongodb://localhost:27017/')

# Check if the connection is successful
if 'FoodDB' in client.list_database_names():
    print('Successfully connected to the FoodDB database.')
else:
    print('Failed to connect to the FoodDB database.')
