from simpy import Store, Environment
import sys
import os
import multiprocessing
from core.log import Logger
from core.performing import *
from agv import AGV
from smartmixingcells import SmartMixingCell
from robotmeasures import RobotMeasureFactory



#Test functions
def testsmc_1():
    b = Blackboard()
    e = b.get('enviro')
    toavg = Store(e)
    AGV(toavg)
    SmartMixingCell("SMC1",toavg)


fdict = {
    'testsmc_1': testsmc_1
}

#main block

def makeLogger(q):
    logger = Logger(q)
    logger.run()


def makeLogging():
    queue = multiprocessing.Queue()
    p = multiprocessing.Process(target=makeLogger, args=(queue,))
    p.start()
    return queue


def main(stop,fcode):
    #myProgressBar = ProgressBar(nElements=10, nIterations=100)
    enviro = Environment()
    logqueue = makeLogging()
    board = Blackboard()
    board.put('logqueue',logqueue)
    board.put('enviro',enviro)
    metrics = board.get('kindmetric')
    fdict[fcode]()
    enviro.run(until=stop)
    logqueue.put('HALT')
    measure = RobotMeasureFactory.generate(metrics)
    retval = measure.get()
    return retval

def experiment(stop,fcode,iters):
    retval = list()
    for i in range(0,iters):
        print('**EXP ' + str(i) + ' **')
        temp = main(stop,fcode)
        retval.append(temp)
    return retval



if __name__ == "__main__":
    if len(sys.argv) > 3:
        fcode = sys.argv[1]
        stopTime = int(sys.argv[2])
        experiments = int(sys.argv[3])
        original = sys.stdout
        if len(sys.argv) > 4:
            fname = sys.argv[4]
            if os.path.exists(fname):
                os.remove(fname)
            sys.stdout = open(fname, "w")
        ret = experiment(stopTime,fcode,experiments)
        sys.stdout = original
        print(ret)
        print('Simulation completed')
    else:
        usage = sys.argv[0] + ' testcode stoptime experiments logfilename'
        print(usage)
