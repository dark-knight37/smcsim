import random
from robot.datatypes import ProductKind

class Product():
    def __init__(self,kkind,intlevel=1):
        self.productKind = kkind
        self.integrity = intlevel
        #todo introduct cost in product in order to compute the integrity weighted by costs

    def __str__(self):
        return '(' + str(self.productKind) + ',' + str(self.integrity) + ')'



class Pallet():
    #todo global integrity function
    def __init__(self,ccapacity):
        self.items = list()
        self.capacity = ccapacity

    def isEmpty(self):
        return (len(self.items) == 0)

    def isFull(self):
        return (len(self.items) == self.capacity)

    def getAvailableProductKind(self):
        item = self.items[0].productKind
        return item

    def pop(self):
        return self.items.pop(0)

    def top(self):
        return self.items[0]

    def lenght(self):
        return len(self.items)

    def add(self, pproduct):
        retval = False
        if (self.isFull() == False):
            self.items.append(pproduct)
            retval = True
        return retval

    def todict(self):
        retval = dict()
        for i in self.items:
            if not i.productKind in retval:
                retval[i.productKind] = 0
            retval[i.productKind] += 1
        return retval

    def __str__(self):
        return '[' + ','.join(list(map(lambda x: str(x),self.items))) + ']'


class OutputPallet(Pallet):
    #todo global integrity function
    def __init__(self,ccapacity,reqs):
        super().__init__(ccapacity)
        self.requirements = reqs

    def getsimpleneeded(self):
        return self.requirements.getsimpleneeded(self)

    def isSatisfied(self):
        temp = len(self.requirements.getsimpleneeded(self))
        return temp == 0


class PalletFactory():

    @staticmethod
    def generate(maxcapacity = 100, size = 0, homogeneous = True, requirements = None):
        if requirements is None:
            retval = Pallet(maxcapacity)
        else:
            retval = OutputPallet(maxcapacity,requirements)
        guess = random.randint(0, len(ProductKind)-1)
        for i in range(0,size):
            if (not homogeneous):
                guess = random.randint(0, 7)
            retval.add(Product(ProductKind(guess)))
        return retval