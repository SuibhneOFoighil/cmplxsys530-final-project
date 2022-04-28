import sys
import networkx as nx
import pandas as pd
from scipy.stats.qmc import LatinHypercube
import model as abm
import statsmodels.api as sm

#effect: reads interlock networks in 'networks' folder as networkx graphs
#        returns list of the interlock network by year: 2010, 2011, ... 2020
def load_networks():
    return [ nx.read_gexf(f'init-data/{year}_network.gexf') for year in range(2010,2021)]

def main():
    if len(sys.argv) != 2:
        print('USAGE: main.py NUM-SIMS')
        return 1

    numSims = int(sys.argv[1])

    print('Loading Networks...')
    networks = load_networks()
    print('Done.\n')

    print('Loading Timeseries...')
    elections = pd.read_csv('init-data/elections.csv', header=0)
    print('Done.\n')

    print('Sampling Parameters...') #Weight on Local DEV, Intervention Threshold, Probability of Success
    sampleSpace = LatinHypercube(d=3)
    paramSample = sampleSpace.random(n=numSims)
    paramSample[:, 0] = paramSample[:, 0] * 0.04 + 0.01  # Local DEV: (0.01 - 0.05)
    paramSample[:, 1] =  paramSample[:, 1] * 0.15 + 0.1  # Threshold: (0.1 - 0.25)
    print('Done.\n')

    print('Simulating...')
    simData = [] #list of dataframes
    for i in range(numSims):
        params = paramSample[i]
        M = abm.Model(networks, elections, params)
        M.simulate()
        data = M.electionResults
        hiearchicalColumns = pd.MultiIndex.from_product( [ [i], list(data.keys()) ] )
        df_i = pd.DataFrame(data)
        df_i.columns = hiearchicalColumns
        simData.append(df_i)
        print(i)
    print('Done.\n')

    print('Exporting Simulated Data...')
    simulatedElectionOutcomes = pd.concat(simData, axis=1)
    simulatedElectionOutcomes.to_csv('analysis/simulated-observations.csv', index=False)
    paramsUsed = pd.DataFrame(paramSample, columns=['localDEV Weight', 'Intervention Threshold', 'Probability(Intervention = Success)'])
    print('Done.\n')

    print('Regressing on Data...')
    regression_info = {
        'GlobalDEV Weight': [],
        'GlobalDEV Stdev': [],
        'GlobalDEV Pvalue': []
    }
    for i in range(numSims):
        print(i)
        timeseries = simulatedElectionOutcomes[i]
        regression = sm.GEE.from_formula(
            formula='isWoman ~ globalDEV',
            groups=timeseries['boardid'],
            family=sm.families.Binomial(),
            cov_struct=sm.cov_struct.Exchangeable(),
            data=timeseries
        ).fit()

        regression_info['GlobalDEV Weight'].append(regression.params.globalDEV)
        regression_info['GlobalDEV Stdev'].append(regression.bse.globalDEV)
        regression_info['GlobalDEV Pvalue'].append(regression.pvalues.globalDEV)

    print('Done.\n')

    print('Exporting Results...')
    results_DF = pd.concat([paramsUsed, pd.DataFrame(regression_info)], axis=1)
    results_DF.index.name = 'Generation'
    results_DF.to_csv('analysis/simulation-outcomes.csv')
    print('Done.\n')

if __name__ == "__main__":
    main()
