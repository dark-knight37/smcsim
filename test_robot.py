from simpy import Store, Environment
import sys
import os
import multiprocessing
from core.log import Logger
from core.performing import *
from robot.agv import AGV
from robot.smartmixingcells import SmartMixingCell
from robot.robotmeasures import RobotMeasureFactory
from core.blackboard import BlackboardFactory


def makeLogger(q):
    logger = Logger(q)
    logger.run()


def makeLogging():
    queue = multiprocessing.Queue()
    p = multiprocessing.Process(target=makeLogger, args=(queue,))
    p.start()
    return queue


def main(stop):
    enviro = Environment()
    logqueue = makeLogging()
    board = Blackboard()
    board.put('logqueue',logqueue)
    board.put('enviro',enviro)
    metrics = board.get('kindmetric')
    toavg = Store(enviro)
    AGV(toavg)
    SmartMixingCell("SMC1",toavg)
    enviro.run(until=stop)
    logqueue.put('HALT')
    measure = RobotMeasureFactory.generate(metrics)
    retval = measure.get()
    return retval


def experiment(stop,iters):
    retval = list()
    for i in range(0,iters):
        print('**EXP ' + str(i) + ' **')
        temp = main(stop)
        retval.append(temp)
    return retval


if __name__ == "__main__":
    if len(sys.argv) > 1:
        config = sys.argv[1]
        original = sys.stdout
        if len(sys.argv) > 2:
            fname = sys.argv[2]
            if os.path.exists(fname):
                os.remove(fname)
            sys.stdout = open(fname, "w")
        BlackboardFactory.load(config)
        b = Blackboard()
        st = b.get('stoptime')
        ex = b.get('experiments')
        ret = experiment(st,ex)
        sys.stdout = original
        print(ret)
        print('Simulation completed')
    else:
        usage = sys.argv[0] + ' testcode stoptime experiments logfilename'
        print(usage)
