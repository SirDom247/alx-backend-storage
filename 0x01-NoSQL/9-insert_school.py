#!/usr/bin/env python3
"""
PyMongo operations: inserting new documents
"""


def insert_school(mongo_collection, **kwargs):
    """ Inserts a new document in a mongodb collection
        based on on kwargs
        Return: id generated for inserted document
    """
    return mongo_collection.insert_one(kwargs).inserted_id
