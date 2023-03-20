import hazelcast as hz
import time
import sys
sys.path.append("..")
from utils import Value, parse


n, debug = parse()
client = hz.HazelcastClient()
m = client.get_map("map")
key = "1"

m.put_if_absent(key, Value()).result()

for k in range(20000):
    debug and k % 100 == 0 and print(f"At: {k}")
    while True:
        oldValue: Value = m.get(key).result()
        if oldValue is None:
            continue
        newValue = Value(oldValue)
        time.sleep(0.01)
        newValue.amount += 1
        if m.replace_if_same(key, oldValue, newValue).result():
            break

print(f"Process {n} finished with {m.get(key).result().amount}")
