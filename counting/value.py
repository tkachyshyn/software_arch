
class Value:

    def __init__(self, other: 'Value'=None):
        if other is None:
            self.amount = 0
        else:
            self.amount = other.amount
