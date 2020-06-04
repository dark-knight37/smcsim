from simpy import Store, Environment
import sys
import os
from core.log import Logger
from core.performing import *
from robot.agv import AGV
from robot.smartmixingcells import SmartMixingCell
from core.blackboard import BlackboardFactory
from core.measures import Recorder, Analyser
from multiprocessing import Pool, Queue, Process

def makeLogger(q):
    logger = Logger(q)
    logger.run()


def makeLogging():
    queue = Queue()
    p = Process(target=makeLogger, args=(queue,))
    p.start()
    return queue


def main(stop):
    record = Recorder()
    record.reset()
    enviro = Environment()
    logqueue = makeLogging()
    board = Blackboard()
    board.put('logqueue',logqueue)
    board.put('enviro',enviro)
    toavg = Store(enviro)
    AGV(toavg)
    SmartMixingCell("SMC1",toavg)
    enviro.run(until=stop)
    logqueue.put('HALT')
    retval = record.generateRecord()
    return retval

def experiment(stop,iters,eps):
    retval = Analyser()
    stopcondition = False
    counter = 0
    while (not stopcondition):
        print('PRE#' + str(counter))
        record = main(stop)
        retval.add(record)
        #temp = retval.confidence99()
        #minc99, maxc99 = temp
        #delta = (maxc99 - minc99)
        #mid =  (maxc99 + minc99) / 2
        #curr = delta / mid
        counter += 1
        stopcondition = (counter == iters)
    return retval

def root(args):
    config = args[1]
    original = sys.stdout
    if len(args) > 2:
        fname = args[2]
        if os.path.exists(fname):
            os.remove(fname)
        sys.stdout = open(fname, "w")
    BlackboardFactory.load(config)
    b = Blackboard()
    st = b.get('stoptime')
    ex = b.get('experiments')
    eps = b.get('epsilon')
    ret = experiment(st, ex, eps)
    tuplet = ret.getAll()
    print(tuplet)
    sys.stdout = original


if __name__ == "__main__":
    if len(sys.argv) > 1:
        root(sys.argv)
    else:
        usage = sys.argv[0] + ' testcode stoptime experiments logfilename'
        print(usage)
