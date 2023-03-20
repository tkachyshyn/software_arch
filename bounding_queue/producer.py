import sys
import hazelcast as hz
sys.path.append("..")


client = hz.HazelcastClient()
q = client.get_queue("q")

while True:
    for i in range(200):
        print(f"Put {i}")
        q.put(i).result()
        i += 1
