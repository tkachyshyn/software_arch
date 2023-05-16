import sys
import hazelcast as hz
sys.path.append("..")


queue = hz.HazelcastClient().get_queue("q")

while True:
    for i in range(200):
        print(f"Put {i}")
        queue.put(i).result()
        i += 1
