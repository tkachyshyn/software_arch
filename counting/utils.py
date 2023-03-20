from argparse import ArgumentParser

class Value:

    def __init__(self, other: 'Value'=None):
        if other is None:
            self.amount = 0
        else:
            self.amount = other.amount


def parse():
    parser = ArgumentParser()
    parser.add_argument("-n", required=True)
    parser.add_argument("-d", action="store_const", const=True)
    args = parser.parse_args()
    n = args.n
    debug = args.d

    return n, debug

def put_result(m, key, time):
    value: Value = m.get(key).result()
    time.sleep(0.01)
    value.amount += 1
    m.put(key, value).result()