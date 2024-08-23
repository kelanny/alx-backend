#!/usr/bin/env python3
""" LIFO Caching
"""

from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """ Defines the LIFO caching system"""

    def __init__(self):
        """ Initiliaze
        """
        super().__init__()
        self.stack = []

    def put(self, key, item):
        """ Add an item in the cache
        """
        if key and item:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                discard = self.stack.pop()
                del self.cache_data[discard]
                print("DISCARD: {}".format(discard))
            self.cache_data[key] = item
            self.stack.append(key)

    def get(self, key):
        """ Get an item by key
        """
        return self.cache_data.get(key, None)
