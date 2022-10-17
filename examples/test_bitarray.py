import torch, bitarray, numpy, math, random, time, dgl, copy
from bitarray import bitarray
from pyLSHash import LSHash
from pyLSHash import pyLSHash
import sys


n = 128

hash_out_size = 10







# print(sys.getsizeof(numpy_x))
# print(sys.getsizeof(fx))

# print(fx)
# print(numpy_x)


lsh = LSHash(hash_size = hash_out_size, input_dim = n)


for idx in range(1000):
	numpy_x = numpy.array([1 if random.random() > 0.5 else 0 for _ in range(n)], dtype = 'b')
	lsh.index(numpy_x, idx)




res = lsh.query(numpy.array([1 if random.random() > 0.5 else 0 for _ in range(n)], dtype = 'b'))


print(res)



