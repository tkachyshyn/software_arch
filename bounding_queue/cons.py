import sys
from argparse import ArgumentParser
import hazelcast
sys.path.append("..")


prsr = ArgumentParser()
prsr.add_argument("-n", required=True)
n = prsr.parse_args().n

queue = hazelcast.HazelcastClient().get_queue("q")

while True:
    for i in range(200):
        a = queue.poll().result()
        if a is None:
            continue
        print(f"Consumer {n} poll {a}")
