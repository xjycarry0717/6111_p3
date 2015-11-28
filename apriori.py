import os
import json
import itertools
import csv

class apriori:
    def __init__(self, filename, minSupp, minConf):
        self.minsupp = minSupp
        self.minconf = minConf
        self.filename = filename
        self.candidate = []
        self.supp = {}
        self.conf = {}
        self.lines = 0
        self.flag = 0

        return

    #read and parse the csv file and generate large 1-itemsets
    #record total number of lines and number of large 1-itemsets
    def parse(self,):
        file = open(self.filename)
        num = 0
        for line in file:
            num = num + 1
            line = (line.strip('\n')).split(',')
            for item in line:
                if (item,) not in self.supp.keys():
                    self.supp[(item,)] = []
                self.supp[(item,)].append(num)
        self.lines = num

        candidateK = []
        for item in self.supp.keys():
            if len(self.supp[item])*1.0/self.lines >= self.minsupp:
                candidateK.append(list(item))
            else:
                del self.supp[item]
        self.candidate.append(candidateK)

        return len(candidateK)

    # generate large k-itemsets by k-1 itemsets
    def generate(self,):
        candidateK = []
        for cand1 in range(0,len(self.candidate[-1])):
            for cand2 in range(cand1+1, len(self.candidate[-1])):
                if self.candidate[-1][cand1][:-1] == self.candidate[-1][cand2][:-1]:
                    tmp = self.candidate[-1][cand1][:]
                    tmp.append(self.candidate[-1][cand2][-1])
                    candidateK.append(tmp)
        if len(candidateK) == 0:
            self.flag = 1
        else:
            self.candidate.append(candidateK)


    def calc(self,):
        # remove invalid itemsets
        for cand in self.candidate[-1][:]:
            for combination in list(itertools.combinations(cand,len(cand)-1)):
                if list(combination) not in self.candidate[-2] and cand in self.candidate[-1]:
                    self.candidate[-1].remove(cand)

        #calculate support and remove itemsets with support less than min_supp
        for cand in self.candidate[-1][:]:
            interSet = set.intersection(set(self.supp[tuple(sorted(cand[:-1]))]), set(self.supp[(cand[-1],)]))
            if len(list(interSet))*1.0/self.lines >= self.minsupp:
                self.supp[tuple(sorted(cand))] = list(interSet)
            else:
                self.candidate[-1].remove(cand)

        #calculate confidence
        for cand in self.candidate[-1][:]:
            for permutation in list(itertools.permutations(cand,len(cand))):
                lhs = list(permutation)[:-1]
                confidence = len(self.supp[tuple(sorted(cand))])*1.0/len(self.supp[tuple(sorted(lhs))])
                support = len(self.supp[tuple(sorted(cand))])*1.0/self.lines
                if confidence > self.minconf:
                    self.conf[(tuple(sorted(lhs)),(permutation[-1],))] = (confidence * 100.0, support * 100.0)

        if len(self.candidate[-1]) == 0:
            self.flag = 1


if __name__ == '__main__':
    data = apriori('test.csv',0.7,0.5)
    count = data.parse()
    i = 1
    while(i < count and data.flag == 0):
        data.generate()
        data.calc()
        i = i + 1;

    f = open("output.txt", 'w')
    f.write('==Frequent itemsets (min_sup=' + str(data.minsupp*100.0) + '%)\n')
    for item in sorted(data.supp, key = lambda item: len(data.supp[item]), reverse = True):
        f.write(str(list(item)) + ', ' + str(len(data.supp[tuple(sorted(item))])*100.0/data.lines)+ '%\n')
    f.write('\n')
    f.write('==High-confidence association rules (min_conf=' + str(data.minconf*100.0) + '%)\n')
    for key, value in sorted(data.conf.items(), key = lambda (key, value): value[0], reverse = True):
        f.write(str(list(key[0])) + ' => ' + str(list(key[1])) + ' (Conf: ' + str(value[0]) + '%, Supp: ' + str(value[1]) + '%)\n')
    f.close()
