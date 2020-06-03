import core.utils

class Sample():
    def __init__(self,kind):

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

    def add(self,sample):
        name = sample.getName()
        if not name in self.sample.keys():
            self.samples[name] = list()
        self.samples[name].append(sample)

    def fitness(self):
        pass

    def mean(self):
        return self.swissknife(utils.mean,None,tags)

    def std(self):
        return self.swissknife(utils.std,None,tags)

    def conflvl(self):
        return self.swissknife(utils.std,level,tags)

    def swissknife(self,funcù):
        retval = dict()
        for k in self.samples.keys():
            retval[k] = func(k)
        return retval

    #def csv(self):
    #    retval = ';'.join(self.samples.keys())
    #    size = self.samples[self.samples.keys()[0]]
    #    for i in range(0,size):
    #        retval += i.tocsv() + '\n'
    #    return retval
