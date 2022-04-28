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

    print('Regressing on Full Dataset...')
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
    results_DF.to_csv('analysis/full-regression.csv')
    print('Done.\n')

    print('Regressing on Partitioned Dataset...')
    period1_info = {
        'GlobalDEV Weight': [],
        'GlobalDEV Stdev': [],
        'GlobalDEV Pvalue': []
    }
    period2_info = {
        'GlobalDEV Weight': [],
        'GlobalDEV Stdev': [],
        'GlobalDEV Pvalue': []
    }

    for i in range(numSims):
        print(i)
        timeseries = simulatedElectionOutcomes[i]
        firstPeriod = timeseries.iloc[:6315]
        secondPeriod = timeseries.iloc[6315:]

        regression = sm.GEE.from_formula(
            formula='isWoman ~ globalDEV',
            groups=firstPeriod['boardid'],
            family=sm.families.Binomial(),
            cov_struct=sm.cov_struct.Exchangeable(),
            data=firstPeriod
        ).fit()

        period1_info['GlobalDEV Weight'].append(regression.params.globalDEV)
        period1_info['GlobalDEV Stdev'].append(regression.bse.globalDEV)
        period1_info['GlobalDEV Pvalue'].append(regression.pvalues.globalDEV)

        regression = sm.GEE.from_formula(
            formula='isWoman ~ globalDEV',
            groups=secondPeriod['boardid'],
            family=sm.families.Binomial(),
            cov_struct=sm.cov_struct.Exchangeable(),
            data=secondPeriod
        ).fit()

        period2_info['GlobalDEV Weight'].append(regression.params.globalDEV)
        period2_info['GlobalDEV Stdev'].append(regression.bse.globalDEV)
        period2_info['GlobalDEV Pvalue'].append(regression.pvalues.globalDEV)

    p1 = pd.DataFrame(period1_info)
    p1.columns = pd.MultiIndex.from_product([['2010-2016'], list(p1.columns)])

    p2 = pd.DataFrame(period2_info)
    p2.columns = pd.MultiIndex.from_product([['2017-2020'], list(p2.columns)])

    paramsUsed.columns = pd.MultiIndex.from_product([['Parameters'], list(paramsUsed.columns)])

    df = pd.concat([paramsUsed, p1, p2], axis=1)
    df.index.name = 'Generation'
    df.to_csv('analysis/split-regression.csv')
    print('Done.\n')

if __name__ == "__main__":
    main()
