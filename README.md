



A fast Python implementation of locality sensitive hashing.

I was using [kayzhu/LSHash](https://github.com/kayzhu/LSHash), but it stopped updating since 2013.  
So I maintain it myself, and I have made a lot of improvement based on it.

## Highlights

- Fast hash calculation for large amount of high dimensional data through the use of `numpy` arrays.
- Built-in support for persistency through Redis.
- Multiple hash indexes support.
- Built-in support for common distance/objective functions for ranking outputs.

## Installation


`pyLSHash` depends on the following libraries:

- numpy
- redis (if persistency through Redis is needed)


To install:


```bash
$ pip install pyLSHash
```

## Quickstart

To create 6-bit hashes for input data of 8 dimensions:


```python
from pyLSHash import LSHash

lsh = LSHash(hash_size=6, input_dim=8)
lsh.index([1, 2, 3, 4, 5, 6, 7, 8])
lsh.index([2, 3, 4, 5, 6, 7, 8, 9])
# attach extra_data
lsh.index([2, 3, 4, 5, 6, 7, 8, 9], extra_data="some vector info")
lsh.index([10, 12, 99, 1, 5, 31, 2, 3])

res = lsh.query([1, 2, 3, 4, 5, 6, 7, 7])
```

>[((1, 2, 3, 4, 5, 6, 7, 8), 1.0),
((2, 3, 4, 5, 6, 7, 8, 9), 11)]

### User defined distance function

```python
def l1norm_dist(x, y):
    return sum(abs(x - y))


res2 = lsh.query([1, 2, 3, 4, 5, 6, 7, 7], dist_func=l1norm_dist)

print(res2)
```


## Use Redis

```python
from pyLSHash import LSHash

lsh = LSHash(hash_size=6, input_dim=8
             , storage_instance=RedisStorage({'host': 'localhost', 'port': 6379, 'decode_responses': True}))

lsh.index([1, 2, 3, 4, 5, 6, 7, 8])
lsh.index([2, 3, 4, 5, 6, 7, 8, 9])
# attach extra_data
lsh.index([2, 3, 4, 5, 6, 7, 8, 9], extra_data="some vector info")
lsh.index([10, 12, 99, 1, 5, 31, 2, 3])
lsh.index([10, 12, 99, 1, 5, 31, 2, 3])

res = lsh.query([1, 2, 3, 4, 5, 6, 7, 7])
```

## Use other database as storage

```python
from pyLSHash import LSHash
from pyLSHash.storage import StorageBase
import redis
import json


class MyStorage(StorageBase):
    def __init__(self):
        self.storage = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)

    def keys(self, pattern="*"):
        return self.storage.keys(pattern)

    def set_val(self, key, val):
        self.storage.set(key, val)

    def get_val(self, key):
        return self.storage.get(key)

    def append_val(self, key, val):
        self.storage.rpush(key, json.dumps(val))

    def get_list(self, key):
        res_list = [json.loads(val) for val in self.storage.lrange(key, 0, -1)]
        return tuple((tuple(item[0]), item[1]) for item in res_list)

    def clear(self):
        for key in self.storage.keys():
            self.storage.delete(key)


lsh = LSHash(hash_size=6, input_dim=8
             , storage_instance=MyStorage())

lsh.index([1, 2, 3, 4, 5, 6, 7, 8])
lsh.index([2, 3, 4, 5, 6, 7, 8, 9])
lsh.index([2, 3, 4, 5, 6, 7, 8, 9], extra_data="some vector info")
lsh.index([10, 12, 99, 1, 5, 31, 2, 3])
lsh.index([10, 12, 99, 1, 5, 31, 2, 3])

res = lsh.query([1, 2, 3, 4, 5, 6, 7, 7])
```


## save&load model

```python
lsh.save_uniform_planes("filename.pkl")
lsh.load_uniform_planes("filename.pkl")
```

clear indexed data
```python
lsh.clear_storage()
```
