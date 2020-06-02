class Vision():
    def __init__(self,nname,aaccuracy):
        self.name = nname
        self.accuracy = aaccuracy

    def setStation(self,sta):
        self.station = sta

    def getAccuracy(self):
        return self.accuracy

    def retrieveAvailableProduct(self):
        return self.station.getPallet().getAvailableProductKind()
