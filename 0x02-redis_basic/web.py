#!/usr/bin/env python3

"""
Caching request module
"""

import requests
import redis
import functools
from typing import Dict

# Create a Redis client
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

def get_page(url: str) -> str:
    # Create a key for counting the URL accesses
    access_count_key = f"count:{url}"
    
    # Check if the URL has been accessed before
    access_count = redis_client.get(access_count_key)
    
    if access_count:
        # If the URL has been accessed before, increment the access count
        redis_client.incr(access_count_key)
    else:
        # If the URL is accessed for the first time, set the count to 1 and cache the page
        access_count = 1
        page_content = requests.get(url).text
        redis_client.setex(access_count_key, 10, access_count)  # Set expiration to 10 seconds
        redis_client.setex(url, 10, page_content)  # Cache the page with expiration
    
    return f"Access count: {access_count}\n\n{redis_client.get(url).decode('utf-8')}"

# Decorator for tracking access count and caching
def track_and_cache(func):
    @functools.wraps(func)
    def wrapper(url):
        access_count_key = f"count:{url}"
        access_count = redis_client.get(access_count_key)
        
        if access_count:
            redis_client.incr(access_count_key)
        else:
            access_count = 1
            page_content = requests.get(url).text
            redis_client.setex(access_count_key, 10, access_count)
            redis_client.setex(url, 10, page_content)
        
        return f"Access count: {access_count}\n\n{redis_client.get(url).decode('utf-8')}"
    
    return wrapper

# Use the decorator to apply the behavior to the get_page function
get_page = track_and_cache(get_page)

# Example usage of the get_page function
if __name__ == '__main__':
    url = "http://slowwly.robertomurray.co.uk/delay/10000/url/http://www.example.com"
    result = get_page(url)
    print(result)

