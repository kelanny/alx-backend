#!/usr/bin/env python3
""" LFUCache module """
from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """ LFUCache class that inherits from BaseCaching
    Implements Least Frequently Used (LFU) caching system.
    """

    def __init__(self):
        """Initialize the LFUCache"""
        super().__init__()
        self.freq = {}  # Frequency counter
        self.usage = {}  # Tracks the order of insertion and usage

    def put(self, key, item):
        """Assign item value to key in cache with LFU algorithm"""
        if key is None or item is None:
            return

        if key in self.cache_data:
            self.cache_data[key] = item
            self.freq[key] += 1
        else:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                # Find the least frequently used items
                min_freq = min(self.freq.values())
                candidates = [k for k, v in self.freq.items() if v == min_freq]
                # If there are ties, use LRU
                if len(candidates) > 1:
                    oldest = min(candidates, key=lambda k: self.usage[k])
                    del self.cache_data[oldest]
                    del self.freq[oldest]
                    del self.usage[oldest]
                    print(f"DISCARD: {oldest}")
                else:
                    discard = candidates[0]
                    del self.cache_data[discard]
                    del self.freq[discard]
                    del self.usage[discard]
                    print(f"DISCARD: {discard}")

            self.cache_data[key] = item
            self.freq[key] = 1

        # Update usage to track LRU in case of ties
        self.usage[key] = len(self.usage)

    def get(self, key):
        """Return the value in cache linked to key"""
        if key is None or key not in self.cache_data:
            return None

        self.freq[key] += 1
        # Update usage to mark as recently used
        self.usage[key] = len(self.usage)
        return self.cache_data[key]
