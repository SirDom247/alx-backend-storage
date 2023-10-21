#!/usr/bin/env python3
"""
PyMongo operations: matching data in list
"""


def schools_by_topic(mongo_collection, topic):
    """
    Finds a list of school having a specific topic
    """
    return mongo_collection.find({'topics': topic})
