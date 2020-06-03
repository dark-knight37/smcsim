import random
import numpy
import statistics
from statistics import NormalDist, mean, stdev

def lottery(probabilities):
    ssum = 0
    cumulative = list()
    for p in probabilities:
        ssum = ssum + p
        cumulative.append(ssum)
    guess = random.random()
    counter = 0
    maxnum = len(probabilities)
    found = False
    while ((not found) and (counter < maxnum)):
        found = guess <= cumulative[counter]
        counter = counter + 1
    return counter - 1

def expGuess(beta):
    guess = numpy.random.exponential(beta)
    return guess

def unpack_interrupt(cause):
    kind = cause[-2]
    sender = cause[0:-3]
    return (kind, sender)

def mean(data):
    return mean(data)

def std(data):
    return stdev(data)

def confidence(data, conflevel):
    dist = NormalDist.from_samples(data)
    z = NormalDist().inv_cdf((1 + conflevel) / 2.)
    h = dist.stdev * z / ((len(data) - 1) ** .5)
    return dist.mean - h, dist.mean + h

def confidence95(data):
    return confidence(data,0.95)

def confidence99(data):
    return confidence(data,0.99)
