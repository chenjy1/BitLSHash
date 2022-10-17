# -*- coding: utf-8 -*-

import json
from abc import ABCMeta, abstractmethod
import numpy


__all__ = ['storage']


def storage(storage_config, table_num = 1, index = None):
    """ Given the configuration for storage and the index, return the
    configured storage instance.
    """
    if 'dict' in storage_config:
        return InMemoryStorage('', table_num)
    elif 'redis' in storage_config:
        storage_config['redis']['db'] = index
        return RedisStorage(storage_config['redis'], table_num)
    else:
        raise ValueError("Only in-memory dictionary and Redis are supported.")


class StorageBase(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, config, num):
        """ An abstract class used as an adapter for storages. """
        pass

    @abstractmethod
    def keys(self, table_index):
        """ Returns num list of binary hashes that are used as dict keys. """
        pass

    @abstractmethod
    def set_val(self, key, val, table_index):
        """ Set `val` at `key`, note that the `val` must be a string. """
        pass

    @abstractmethod
    def get_val(self, key, table_index):
        """ Return `val` at `key`, note that the `val` must be a string. """
        pass

    @abstractmethod
    def append_val(self, key, val, table_index):
        """ Append `val` to the list stored at `key`.

        If the key is not yet present in storage, create a list with `val` at
        `key`.
        """
        pass

    @abstractmethod
    def get_list(self, key, table_index):
        """ Returns a list stored in storage at `key`.

        This method should return a list of values stored at `key`. `[]` should
        be returned if the list is empty or if `key` is not present in storage.
        """
        pass

    @abstractmethod
    def clear(self) -> None:
        """ Clear all data
        """
        pass


class InMemoryStorage(StorageBase):
    def __init__(self, config, num):
        self.name = 'dict'
        self.num = num
        self.storage = [dict() for _ in range(self.num)]

    def keys(self, table_index):
        return self.storage[table_index].keys()
        # return [memory.keys() for memory in self.storage]

    def set_val(self, key, val, table_index):
        self.storage[table_index][key] = val

    def get_val(self, key, table_index):
        return self.storage[table_index][key]

    def append_val(self, key, val, table_index):

        self.storage[table_index].setdefault(key, []).append((numpy.copy(val[0]), val[1]))
        # exit()
        # self.storage[table_index].setdefault(key, []).append(val)

    def get_list(self, key, table_index):
        return self.storage[table_index].get(key, [])
        # return [memory.get(key, []) for memory in self.storage]

    def clear(self):
        self.storage = [dict() for _ in range(self.num)]


class RedisStorage(StorageBase):
    def __init__(self, config, num):
        try:
            import redis
        except ImportError:
            raise ImportError("redis-py is required to use Redis as storage.")
        raise NotImportError("")
        self.name = 'redis'
        self.storage = redis.StrictRedis(**config)

    def keys(self, pattern="*"):
        return self.storage.keys(pattern)

    def set_val(self, key, val, table_index):
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
