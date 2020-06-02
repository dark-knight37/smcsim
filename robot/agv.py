from core.blackboard import Blackboard
from simpy import Resource, Store
from core.components import Component
from robot.datatypes import MovementOrder
from robot.pallets import PalletFactory
from robot.requirements import CustomerRequirementFactory

class Vehicle(Component):
    def __init__(self,name, ttime, oorder):
        super().__init__(name,0,0)
        self.transportationTime = ttime
        self.order = oorder

    def run(self):
        while True:
            received = yield self.order.get()
            movorder, putchannel, getchannel = received
            b = Blackboard()
            black_cap = b.get('[pallet]capacity')
            black_flag = b.get('[pallet]homogeneous')
            pallet = None
            if (movorder == MovementOrder.DRPI) or (movorder == MovementOrder.INBD):
                black_size = b.get('[requirements]ordersize')
                pallet = PalletFactory.generate(black_cap, black_size, black_flag, None)
            else:
                requirements = CustomerRequirementFactory.generate(b.get('[requirements]ordersize'))
                pallet = PalletFactory.generate(black_cap, 0, black_flag, requirements)
            if (movorder == MovementOrder.DRPI) or (movorder == MovementOrder.DRPO):
                putchannel.put('REMOVE')
                yield self.env.timeout(self.transportationTime)
                package = yield getchannel.get()
            #self.log('loading station;;', 2)
            yield self.env.timeout(self.transportationTime)
            putchannel.put(pallet)

class AGV(Component):
    def __init__(self,orderchannel):
        super().__init__('AGV',0,0)
        b = Blackboard()
        transportationTime = b.get('[agv]time')
        num = b.get('[agv]number')
        self.env = b.get('enviro')
        self.vehicles = list()
        for i in range(0,num):
            vchannel = Store(self.env)
            v = Vehicle('Vehicle_' + str(i),transportationTime,vchannel)
            self.vehicles.append((v,vchannel))
        self.orderChannel = orderchannel

    def run(self):
        counter = 0
        while True:
            command = yield self.orderChannel.get()
            vehicle, channel = self.vehicles[counter]
            channel.put(command)
            counter += 1
            counter = counter % len(self.vehicles)