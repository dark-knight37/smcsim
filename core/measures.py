
class Sample():
    def __init__(self,hheader):
        self.header = hheader
        self.lst = list()

    def add(self,sample):
        self.lst.append(sample)

    def tocsv(self):
        retval = self.header + '\n'
        for i in self.lst:
            retval += i.tocsv() + '\n'
        return retval



class Measurement():
    def __init__(self):
        self.samples = dict()

    def fitness(self):
        pass

    def getKeys(self,tags):
        retval = self.samples.keys() if (tags is None) else list(tags)
        return retval

    def mean(self,tags = None):
        keys = self.getKeys(tags)
        retval = dict()
        for k in keys:





    def csv(self):
        pass