import hazelcast


def check_data(verbose=True, counter = 0):

    map = hazelcast.HazelcastClient().get_map("m1").blocking()
    for i in range(1000):
        counter += int(map.get(i) is None)
    if verbose == True:
        print(f"{counter}/{1000} entries lost")
    return counter


map = hazelcast.HazelcastClient().get_map("m1").blocking()

for i in range(1000):
    map.put(i, f"v: {i}")

