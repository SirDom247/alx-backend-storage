#!/usr/bin/env python3
"""
PyMongo operations: updating documents
"""


def update_topics(mongo_collection, name, topics):
    """
    Updates topics field with given topics for
    documents whose name field matches given name
    """
    mongo_collection.update_many({'name': name},
                                 {'$set': {'topics': topics}})
