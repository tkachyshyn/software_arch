import hazelcast as hz
import time
import sys

sys.path.append("..")
from utils import Value, parse, put_result


n, debug = parse()

client = hz.HazelcastClient()
m = client.get_map("map")
key = "1"

m.put_if_absent(key, Value()).result()

for k in range(20000):
    debug and k % 100 == 0 and print(f"At: {k}")
    put_result(m, key, time)

print(f"Process {n} finished with {m.get(key).result().amount}")
