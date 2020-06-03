from core.measures import Measurement
from core.blackboard import Blackboard


class HitMeasurement(Measurement):
    def __init__(self):
        b = Blackboard()
        temp = b.get('[Measure]hit')
        b.put('[Measure]',temp)

    def fitness(self):
        return self.get()

    def tocsv(self):
        pass


class MissMeasurement(Measurement):
    def __init__(self):
        b = Blackboard()
        temp = b.get('[Measure]miss')
        b.put('[Measure]',temp)

    def fitness(self):
        return 1/float(self.get())

    def tocsv(self):
        pass


class CombinedMeasurement(Measurement):
    def __init__(self):
        b = Blackboard()
        self.thit = b.get('[Measure]hit')
        self.tmiss = b.get('[Measure]miss')
        b.put('[Measure]',(self.thit,self.tmiss))

    def tocsv(self):
        retval = str(self.thit) + ';' + str(self.tmiss) + ';'
        return retval

    def fitness(self):
        return float(self.thit) + 1/float(self.tmiss)



class RobotMeasureFactory():

    @staticmethod
    def generate(tag):
        mapping = {
            'hit': HitMeasurement,
            'miss': MissMeasurement,
            'idle_vehicle': IdleMeasure
            'all': CombinedMeasurement
        }
        retval = mapping[tag]()
        return retval