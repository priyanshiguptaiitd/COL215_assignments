import numpy as np
rng = np.random.default_rng()
better_pack_order = [None] + list(rng.permutation([i for i in range(1,10+1)]))
print(better_pack_order)
