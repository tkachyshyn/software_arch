from argparse import ArgumentParser

import hazelcast as hz
import time
import sys

sys.path.append("..")
from value import Value


parser = ArgumentParser()
parser.add_argument("-n", required=True)
parser.add_argument("-d", action="store_const", const=True)
args = parser.parse_args()
n = args.n
debug = args.d

map = hz.HazelcastClient().get_map("map")
key = "1"

map.put_if_absent(key, Value()).result()

for i in range(20000):
    debug and i % 100 == 0 and print(f"At: {i}")
    value: Value = map.get(key).result()
    time.sleep(0.01)
    value.amount += 1
    map.put(key, value).result()

print(f"Process {n} finished with {map.get(key).result().amount}")
