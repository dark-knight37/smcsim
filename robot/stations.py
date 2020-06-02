from core.performing import Behaviour, Performing
from core.blackboard import Blackboard

class StationLogic(Behaviour):
    def __init__(self, nname, opentime, belttime, fillin, flushout):
        super().__init__(nname)
        self.inqueue = fillin
        self.outqueue = flushout
        self.opening = opentime
        self.beltmovement = belttime

    def movement(self):
        #self.log('opening the gate;;',0)
        yield self.env.timeout(self.opening)
        #self.log('moving the belt;;',0)
        yield self.env.timeout(self.beltmovement)
        #self.log('closing the gate;;',0)
        yield self.env.timeout(self.opening)

    def do(self):
        if (self.onrun == True):
            query = yield self.inqueue.get()
            #self.log('got packet;'+str(query)+';',0)
            yield self.env.process(self.movement())
            Blackboard().get('[Shared]packages')[self.name[:-3]] = query
            Blackboard().get('[Shared]packages.dirtybit')[self.name[:-3]] = False
            query = yield self.inqueue.get()
            #self.log('got remove;;',0)
            yield self.env.process(self.movement())
            self.outqueue.put(Blackboard().get('[Shared]packages')[self.name[:-3]])
            Blackboard().get('[Shared]packages')[self.name[:-3]] = None
            Blackboard().get('[Shared]packages.dirtybit')[self.name[:-3]] = True



class Station():
    def __init__(self,nname,fin,fout):
        self.name = nname
        self.channelIN = fin
        self.channelOUT = fout
        b = Blackboard()
        self.controller = StationLogic(nname + '_sw', b.get('[gate]opentime'), b.get('[gate]belttime'), fin, fout)
        self.structure = Performing(nname + '_hw', self.controller, b.get('[gate]mtbf'), b.get('[gate]mttr'))

    def getName(self):
        return self.name

    def setVision(self, visio):
        self.vision = visio
        visio.setStation(self)

    def getMissingProducts(self):
        return Blackboard().get('[Shared]packages')[self.name].getMissingProducts()

    def getPallet(self):
        return Blackboard().get('[Shared]packages')[self.name]

    def operative(self):
        return Blackboard().get('[Shared]packages.dirtybit')[self.name] == False

    def dirt(self):
        Blackboard().get('[Shared]packages.dirtybit')[self.name] = True
