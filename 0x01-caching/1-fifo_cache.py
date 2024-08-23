#!/usr/bin/env python3
""" 1. FIFO caching"""

from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """ FIFO cache system"""

    def __init__(self):
        """ Override superclass __init__ """
        super().__init__()
        self.queue = []

    def put(self, key, item):
        """ Add an item in the cache"""
        if key and item:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                if self.queue:
                    discard = self.queue.pop(0)
                    del self.cache_data[discard]
                    print("DISCARD: {}".format(discard))
            self.cache_data[key] = item
            self.queue.append(key)

    def get(self, key):
        """ Get an item by key"""
        return self.cache_data.get(key, None)
