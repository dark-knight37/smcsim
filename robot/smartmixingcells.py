from random import choice
from core.performing import Performing, Behaviour
from core.blackboard import Blackboard
from robot.robots import Robot
from simpy import Store
from robot.stations import Station
from robot.datatypes import *
from robot.visions import Vision
from core.log import Loggable
from core.measures import Recorder


class RuleBasedSystem(Loggable):
    def __init__(self,attempts):
        super().__init__('RuleBasedSystem')
        self.internalcounter = 0
        self.maxattempts = attempts

    def evaluateplateau(self,stations):
        flag = False
        station = None
        if (self.internalcounter > self.maxattempts):
            stats = list(stations.items())
            stats = list(filter(lambda x: x[1][1] == StationDir.INPUT, stats))
            stats = list(map(lambda x: x[1][0], stats))
            stats = list(filter(lambda x: x.operative(), stats))
            if len(stats) >= 0:
                flag = True
                station = choice(stats)
        return flag, station

    def computeNextStep(self,stations):
        retval = None
        resetcondition = False
        stationtoreset = None
        self.internalcounter += 1
        stats = list(stations.items())
        stats = list(filter(lambda x: x[1][0].operative(),stats))
        instats = list(filter(lambda x: x[1][1] == StationDir.INPUT,stats))
        instats = list(map(lambda x: (x[0],x[1][0]),instats))
        outstats = list(filter(lambda x: x[1][1] == StationDir.OUTPUT,stats))
        outstats = list(map(lambda x: (x[0],x[1][0]),outstats))
        if len(outstats) > 0:
            if (len(instats) > 0):
                continuecondition = len(outstats) > 0
                while (continuecondition == True):
                    oindex = choice(range(0, len(outstats)))
                    oname, ostation = outstats.pop(oindex)
                    tomatch = ostation.getPallet().getsimpleneeded()
                    exploring = True
                    pindex = 0
                    while (exploring == True) and (pindex < len(tomatch)):
                        trialpacket = tomatch[pindex]
                        found = False
                        iindex = 0
                        istation = None
                        while (iindex != len(instats)) and (found == False):
                            iname, istation = instats[iindex]
                            apallet = istation.getPallet()
                            apacket = apallet.getAvailableProductKind()
                            found = (apacket == trialpacket)
                            iindex += 1
                        if (found == True):
                            packettoextract = apallet.top()
                            retval = (iname, istation.getPallet(), packettoextract, oname, ostation.getPallet(),
                                      istation.vision.getAccuracy())
                            exploring = False
                            continuecondition = False
                            self.internalcounter = 0
                        pindex += 1
                    continuecondition = continuecondition and len(outstats) > 0
                if (retval is None):
                    resetcondition, stationtoreset = self.evaluateplateau(stations)
        return retval, resetcondition, stationtoreset


#todo : future implementation, SPAs
class MainController(Behaviour):
    def __init__(self, nname, agvcommchannel):
        super().__init__(nname)
        b = Blackboard()
        self.rbs = RuleBasedSystem(b.get('[RBS]maxattempts'))
        envy = b.get('enviro')
        self.accuracyParameter = b.get('[vision]accuracy')
        self.toagv = agvcommchannel
        #robot
        self.robotcomm = Store(envy)
        self.robot = Robot('robot',self.robotcomm)
        # stations
        ninputs = b.get('[stations]inumber')
        noutputs = b.get('[stations]onumber')
        nspas = b.get('[stations]spa')
        self.stations = dict()
        b.put('[Shared]packages',dict())
        b.put('[Shared]packages.dirtybit',dict())
        for sindex in range(0,ninputs):
            sname, stat = self.makeStation(sindex,envy)
            self.stations[sname] = (stat,StationDir.INPUT)
        for sindex in range(0,noutputs):
            sname, stat = self.makeStation(sindex + ninputs,envy)
            self.stations[sname] = (stat,StationDir.OUTPUT)

    def makeStation(self,index,envy):
        name = 'STAT_' + str(index)
        cin = Store(envy)
        cout = Store(envy)
        v = Vision('VIS_' + str(index),self.accuracyParameter)
        s = Station(name, cin, cout)
        s.setVision(v)
        Blackboard().get('[Shared]packages')[name] = None
        Blackboard().get('[Shared]packages.dirtybit')[name] = True
        return name, s

    def boot(self):
        for name in self.stations.keys():
            self.load(name)

    def load(self, sname):
        (stat, dir) = self.stations[sname]
        order = MovementOrder.INBD if (dir == StationDir.INPUT) else (MovementOrder.OUTD)
        msg = (order, stat.channelIN, stat.channelOUT)
        self.toagv.put(msg)

    def reload(self, sname):
        (stat, dir) = self.stations[sname]
        order = MovementOrder.DRPI if (dir == StationDir.INPUT) else (MovementOrder.DRPO)
        msg = (order, stat.channelIN, stat.channelOUT)
        self.toagv.put(msg)

    def checkFullEmptyPallets(self):
        for name in self.stations:
            stat, dir = self.stations[name]
            if stat.operative():
                p = stat.getPallet()
                flag = (dir == StationDir.INPUT) and (p.isEmpty())
                flagout = ((dir == StationDir.OUTPUT) and (p.isSatisfied()))
                flag = flag or flagout
                if flag == True:
                    stat.dirt()
                    if (flagout):
                        #self.log('vault;' + str(p.lenght()) + ';', 2)
                        Recorder().add('hit',p.lenght())
                    self.reload(name)

    def do(self):
        if (self.onrun == True):
            action = None
            while (action == None):
                action, resetcondition, stationtoreset = self.rbs.computeNextStep(self.stations)
                if (action == None):
                    if resetcondition == False:
                        yield self.env.timeout(10)
                    else:
                        stationtoreset.dirt()
                        p = stationtoreset.getPallet()
                        pname = stationtoreset.getName()
                        l = p.lenght()
                        #self.log('MISS;' + stationtoreset.getName() + ',' + str(l) + ';',2)
                        Recorder().add('miss',l)
                        self.reload(pname)
                yield self.env.timeout(1)
            self.robotcomm.put(action)
            yield self.robotcomm.get()
            self.checkFullEmptyPallets()
            #print(Blackboard().get('stoptime') - self.env.now)


class SmartMixingCell():
    def __init__(self,name,agvchannel):
        b= Blackboard()
        self.controller = MainController(name + '_sw', agvchannel)
        self.structure = Performing(name + '_hw',self.controller,b.get('[controller]mtbf'),b.get('[controller]mttr'))