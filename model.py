import random
import copy

BASE_PROBABILITY_ELECTING_WOMAN = 0.3

# helper.
def compute_local_mean(G, node):
    interlocks = G.adj[node]
    series = [ G.nodes[board]['percentagewomen'] for board in interlocks ]
    denom = len(series)
    mean = sum(series) / denom
    return mean * 100

class Model:
    def __init__(self, networks, electionDF, params):
        self.networks = {}
        self.localDevWeight, self.interventionThreshold, self.probabilitySuccessfulIntervention = params
        self.electionsObservations = {}
        self.electionResults = { #tracked data.
            'isWoman':[],
            'localDEV':[],
            'globalDEV':[],
            'boardid': electionDF.boardid.to_list()
        }

        for i, year in enumerate(range(2010, 2021)):

            #timeseries data
            inYear = electionDF.year == year
            bidsElectingDuringYear = electionDF.loc[inYear].boardid
            self.electionsObservations[year] = bidsElectingDuringYear

            #network data: MAKE FASTER
            self.networks[year] = copy.deepcopy(networks[i])

    def simulate(self):
        for year, G in self.networks.items():

            globalMean = sum([ data['percentagewomen'] for n, data in G.nodes(data=True) ])/ len(G.nodes) * 100
            nodesToUpdate = []

            for bid in self.electionsObservations[year]:
                n = str(bid)
                percentageWomen = G.nodes[n]['numberwomen'] / G.nodes[n]['numberdirectors'] * 100
                localMean = compute_local_mean(G, n)
                localDEV = percentageWomen - localMean
                globalDEV = percentageWomen - globalMean

                #Local Conformance
                P_woman = BASE_PROBABILITY_ELECTING_WOMAN + self.localDevWeight * localDEV
                isWoman = random.random() < P_woman

                #Intervention Strategy
                if year >= 2017 and not isWoman and percentageWomen < self.interventionThreshold:
                    isWoman = random.random() < self.probabilitySuccessfulIntervention

                #Record Results
                self.electionResults['isWoman'].append(int(isWoman))
                self.electionResults['localDEV'].append(localDEV)
                self.electionResults['globalDEV'].append(globalDEV)

                if isWoman:
                    nodesToUpdate.append(n)

            #Update Network: all instances of the nodes that need updates.
            #ASSUMPTION: all elections are replacements, not expansions.
            if len(nodesToUpdate) > 0:
                for n_j in nodesToUpdate:
                    currNumberofWomen = self.networks[year].nodes[n_j]['numberwomen']
                    for y in range(year + 1, 2021):
                        G_next = self.networks[y]
                        try:
                            G_next.nodes[n_j]['numberwomen'] = currNumberofWomen + 1
                        except KeyError:
                            continue
