from core.performing import Behaviour, Performing
from core.blackboard import Blackboard
from random import gauss
from core.measures import Recorder


class RobotProgram(Behaviour):
    def __init__(self, nname, commChannel, movetime, pprecision):
        super().__init__(nname)
        self.movementTime = movetime
        self.channel = commChannel
        self.precision = pprecision
        self.timemarker = 0

    def gripManagement(self, health, accuracy):
        mu = accuracy * health
        temp = gauss(mu,self.precision)
        temp = min(health,temp)
        temp = max(0,temp)
        return temp

    def do(self):
        if (self.onrun == True):
            self.log('is waiting to get work;;',1)
            time = self.env.now
            (iname, inpacket, kind, oname, outpacket, accuracy) = yield self.channel.get()
            Recorder().add('robot_idle',self.env.now - time)
            self.log('getting the product from;' + iname + ' ' + str(inpacket)+ ';',1)
            #self.log('putting the product to;' + oname + ' ' + str(outpacket)+ ';',1)
            inpacket = Blackboard().get('[Shared]packages')[iname]
            outpacket = Blackboard().get('[Shared]packages')[oname]
            #self.log('getting the product from;' + iname + ' ' + str(inpacket)+ ';',1)
            #self.log('putting the product to;' + oname + ' ' + str(outpacket)+ ';',1)
            p = inpacket.pop()
            yield self.env.timeout(self.movementTime)
            newi = self.gripManagement(p.integrity,accuracy)
            p.integrity = newi
            outpacket.add(p)
            #self.log('got the product from;' + iname + ' ' + str(inpacket)+ ';',1)
            self.log('put the product to;' + oname + ' ' + str(outpacket)+ ';',1)
            self.channel.put('DONE')


class Robot():
    def __init__(self,name,commchannel):
        b = Blackboard()
        self.controller = RobotProgram(name + '_sw', commchannel, b.get('[robot]time'), b.get('[robot]precision'))
        self.structure = Performing(name + '_hw', self.controller, b.get('[robot]mtbf'), b.get('[robot]mttr'))