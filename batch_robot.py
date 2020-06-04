from test_robot import root
import subprocess
import multiprocessing
import sys
import os


def core(inifile,logfile):
    print('starting')
    list_files = subprocess.call(["python3", "test_robot.py", inifile, logfile])
    print('ending')



if __name__ == "__main__":
    if len(sys.argv) > 1:
        directory = sys.argv[1]
        filenames = filter(lambda x: x.endswith('.ini'), os.listdir(directory))
        jobs = list()
        for fn in filenames:
            ln = directory + fn[:-4] + '.log'
            fn = directory + fn
            p = multiprocessing.Process(target=core, args=(fn,ln))
            jobs.append(p)
            p.start()