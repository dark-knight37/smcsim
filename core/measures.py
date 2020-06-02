from core.blackboard import Blackboard

class Measure():

    def fitness(self):
        pass

    def get(self):
        return Blackboard().get('[Measure]')