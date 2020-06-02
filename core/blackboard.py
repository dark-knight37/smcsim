import configparser
from core.metaclasses import Singleton

class BlackboardUtils():
    @staticmethod
    def yearsToSec(yrs):
        return BlackboardUtils.daysToSec(365 * yrs)

    @staticmethod
    def daysToSec(dys):
        return BlackboardUtils.hoursToSec(24 * dys)

    @staticmethod
    def hoursToSec(hrs):
        return hrs * 3600


class Blackboard(metaclass=Singleton):

    def __init__(self):
        self.board = dict()

    def get(self,key):
        return self.board[key]

    def put(self,key,value):
        self.board[key] = value

    @staticmethod
    def load(inifile):
        black = Blackboard()
        reader = configparser.ConfigParser()
        reader.read(inifile)
        opts = reader.options('[main]')
        for o in opts:
            try:
                temp = reader.get('[main]',o)
                black.put(o,temp)
            except:
                print("exception on %s!" % o)

                import ConfigParser

                class AbstractFactory():
                    def __init__(self, inifile, kind=''):
                        self.reader = ConfigParser.ConfigParser()
                        self.reader.read(inifile)

                    def genList(self, sectName, f, size):
                        td = self.getSection(sectName)
                        retval = map(lambda i: f(td, i), range(0, size))
                        return retval

                    def getSection(self, s):
                        temp = dict()
                        options = self.reader.options(s)
                        for o in options:
                            try:
                                temp[o] = self.reader.get(s, o)
                                if temp[o] == -1:
                                    print("skip: %s" % o)
                            except:
                                print("exception on %s!" % o)
                                temp[o] = None
                        return temp

                    def generate(self, kind=""):
                        pass

                    def listFormatting(self, s):
                        if (s == '-'):
                            retval = None
                        else:
                            retval = s[1:-1]
                            retval = retval.split(',')
                        return retval