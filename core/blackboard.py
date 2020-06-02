import configparser
from core.metaclasses import Singleton

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