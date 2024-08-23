#!/usr/bin/env python3
""" LFU Caching
"""

from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """ LFU cache replacement algorithm
    """

    def __init__(self):
        """ Init
        """
        super().__init__()
        self.cache = {}
        self.lfu = {}
        self.lfu_count = {}

    def put(self, key, item):
        """ Add an item in the cache
        """
        if key is None or item is None:
            return

        if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            min_lfu = min(self.lfu_count.values())
            keys = [k for k in self.lfu_count if self.lfu_count[k] == min_lfu]
            if len(keys) == 1:
                del self.cache_data[keys[0]]
                del self.lfu[keys[0]]
                del self.lfu_count[keys[0]]
            else:
                min_lfu = min(self.lfu[keys[0]], self.lfu[keys[1]])
                key = keys[0] if self.lfu[keys[0]] == min_lfu else keys[1]
                del self.cache_data[key]
                del self.lfu[key]
                del self.lfu_count[key]

        self.cache_data[key] = item
        self.lfu[key] = 0
        self.lfu_count[key] = 0

    def get(self, key):
        """ Get an item by key
        """
        if key is None or key not in self.cache_data:
            return None

        self.lfu[key] += 1
        self.lfu_count[key] += 1
        return self.cache_data[key]
