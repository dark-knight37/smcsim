import random
from robot.datatypes import ProductKind

class Requirement():
    def __init__(self, kkind, rreq):
        self.product = kkind
        self.requirement = rreq

    def __str__(self):
        return '(' + str(self.product) + ',' + str(self.requirement) + ')'


class CustomerRequirement():
    def __init__(self):
        self.requirements = list()

    def addRequirement(self,req):
        self.requirements.append(req)

    def getRequirements(self):
        return self.requirements

    def computeneeded(self,pallet):
        retval = dict()
        existing = pallet.todict()
        for r in self.requirements:
            temp = r.requirement - existing.get(r.product,0)
            if (temp > 0):
                retval[r.product] = temp
        return retval

    def getsimpleneeded(self, pallet):
        needed = list(self.computeneeded(pallet).keys())
        return needed

    def piecestogo(self):
        summ = list(map(lambda x: x.requirement,self.requirements))
        summ = sum(summ)
        return summ



class CustomerRequirementFactory():

    @staticmethod
    def generate(maxnumber):
        retval = CustomerRequirement()
        indices = list(range(0,len(ProductKind)))
        current = 0
        possibleguess = maxnumber
        while (len(indices) > 0) and (current < maxnumber):
            pick = random.choice(indices)
            indices.remove(pick)
            guess = random.randint(1,possibleguess)
            current += guess
            possibleguess = possibleguess - guess
            requirement = Requirement(ProductKind(pick),guess)
            retval.addRequirement(requirement)
        return retval