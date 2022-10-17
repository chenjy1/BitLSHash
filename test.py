import torch, bitarray, numpy, math, random, time, dgl, copy
from bitarray import bitarray
from pyLSHash import LSHash

import sys


n = 100

hash_out_size = 30







# print(sys.getsizeof(numpy_x))
# print(sys.getsizeof(fx))

# print(fx)
# print(numpy_x)

time0 = time.time()
lsh = LSHash(hash_size = hash_out_size, input_dim = n)
batch = 100

for idx in range(200 * batch):
	numpy_x = numpy.array([1 if random.random() > 0.5 else 0 for _ in range(n)], dtype = 'b')
	lsh.index(numpy_x, idx)




	# for idy in range(100):
	query_point = numpy.array([1 if random.random() > 0.5 else 0 for _ in range(n)], dtype = 'b')

	hash_val = lsh._hash(lsh.uniform_planes[0], query_point)
	# print(hash_val)

	res = lsh.query(query_point)


print(time.time() - time0)


# print(res)
# print(len(res))
# for cand in res:
# 	# print(cand)
# 	cand_hash_val = lsh._hash(lsh.uniform_planes[0], cand[0][0])
# 	assert(cand_hash_val == hash_val)

# 	diff = cand[0][0] != query_point

# 	assert(numpy.sum(diff) == cand[1])


