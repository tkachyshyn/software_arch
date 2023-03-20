import hazelcast as hz
import time
import sys
sys.path.append("..")
from utils import Value, parse, put_result


n, debug = parse()
client = hz.HazelcastClient()
m = client.get_map("map")
key = "1"

m.put_if_absent(key, Value())


for k in range(20000):
    debug and k % 100 == 0 and print(f"At: {k}")
    m.lock(key).result()
    try:
        put_result(m, key, time)
    finally:
        m.unlock(key).result()

print(f"Process {n} finished with {m.get(key).result().amount}")

