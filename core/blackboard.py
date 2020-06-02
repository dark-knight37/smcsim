import configparser
from core.metaclasses import Singleton

class BlackboardFactory():
    @staticmethod
    def years(yrs):
        temp = 365 * float(yrs)
        temp = BlackboardFactory.days(temp)
        return temp

    @staticmethod
    def days(dys):
        temp = 24 * float(dys)
        temp = BlackboardFactory.hours(temp)
        return temp

    @staticmethod
    def hours(hrs):
        temp = float(hrs) * 3600
        return temp

    @staticmethod
    def load(inifile):
        black = Blackboard()
        reader = configparser.ConfigParser()
        reader.read(inifile)
        try:
            temp = reader['main']['experiments']
            black.put('experiments',int(temp))
            temp = reader['main']['parallelism']
            black.put('parallelism',int(temp))
            temp = reader['main']['debugLevel']
            black.put('debugLevel',int(temp))
            temp = reader['main']['kindmetric']
            black.put('kindmetric',temp)
            temp = reader['main']['stoptime']
            temp = BlackboardFactory.tosecond(temp)
            black.put('stoptime',temp)
            sections = BlackboardFactory.tolist(reader['main']['sections'])
            for s in sections:
                temp = BlackboardFactory.loadSection(reader,s)
                Blackboard().merge(temp)
        except Exception as s:
            print(s)


    @staticmethod
    def tosecond(value):
        mapping = {
            'years': BlackboardFactory.years,
            'days': BlackboardFactory.days,
            'hours': BlackboardFactory.hours,
            'int': int,
            'float': float,
            'bool': bool
        }
        vals = value.split(',')
        f = mapping[vals[1]]
        retval = f(vals[0])
        return retval

    @staticmethod
    def checktime(value):
        acceptable = ['years','days','hours','int','float']
        vals = value.split(',')
        found = False
        if len(vals) == 2:
            try:
                found = vals[1] in acceptable
            except TypeError:
                found = False
        return found


    @staticmethod
    def tolist(value):
        retval = value.split(',')
        return retval

    @staticmethod
    def loadSection(reader,s):
        temp = dict()
        options = reader.options(s)
        for o in options:
            try:
                value = reader[s][o]
                if (BlackboardFactory.checktime(value)):
                    value = BlackboardFactory.tosecond(value)
                temp['[' + s + ']' + o] = value
            except:
                print("exception on %s!" % o)
                temp[o] = None
        return temp





class Blackboard(metaclass=Singleton):

    def __init__(self):
        self.board = dict()

    def get(self,key):
        return self.board[key]

    def put(self,key,value):
        self.board[key] = value

    def merge(self,dic):
        self.board.update(dic)