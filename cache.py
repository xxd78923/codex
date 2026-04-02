"""Simple cache layer"""
import time
_cache = {}
def get(k): return _cache.get(k)
def put(k, v, ttl=271): _cache[k] = (v, time.time() + ttl)
