from test_robot import root
import sys
import os

if __name__ == "__main__":
    if len(sys.argv) > 1:
        directory = sys.argv[1]
        filenames = filter(lambda x: x.endswith('.ini'), os.listdir(directory))
        for fn in filenames:
            print(fn)
            log = fn[:-4] + '.log'
            args = [None, directory + '/' + fn, directory + '/' + log]
            root(args)

