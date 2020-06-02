from core.measures import Measure
from core.blackboard import Blackboard


class HitMeasure(Measure):
    def __init__(self):
        b = Blackboard()
        temp = b.get('[Measure]hit')
        b.put('[Measure]',temp)

    def fitness(self):
        return self.get()


class MissMeasure(Measure):
    def __init__(self):
        b = Blackboard()
        temp = b.get('[Measure]miss')
        b.put('[Measure]',temp)

    def fitness(self):
        return 1/float(self.get())


class CombinedMeasure(Measure):
    def __init__(self):
        b = Blackboard()
        thit = b.get('[Measure]hit')
        tmiss = b.get('[Measure]miss')
        b.put('[Measure]',(thit,tmiss))

    def fitness(self):
        hit,miss = self.get()
        return float(hit) + 1/float(miss)



class RobotMeasureFactory():

    @staticmethod
    def generate(tag):
        mapping = {
            'hit': HitMeasure,
            'miss': MissMeasure,
            'all': CombinedMeasure
        }
        retval = mapping[tag]()
        return retval