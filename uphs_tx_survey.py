def calculateDeviationFromMeanByObserver(df, start_scenario=1, stop_scenario=60):
    """Calculates Mean Squared Error against the overall mean for that observer"""
    mse = []
    number_of_observers = df['Observer ID'].max()
    scenarios = (df['Scenario ID'] >= start_scenario) & (df['Scenario ID'] <= stop_scenario)

    for observer in range(number_of_observers):
        scores = df[scenarios & (df['Observer ID'] == observer+1)]['Observer Risk']
        scores_mean = scores.mean()
        n = len(scores)
        mse.append((1/n)*np.sum((scores - scores_mean)**2))
    return np.round(np.array(mse), 2)


def calculateDeviationFromSRTRByObserver(df, start_scenario=1, stop_scenario=60):
    """Calculates Mean Squared Error against each SRTR score for the observer"""
    mse = []
    number_of_observers = df['Observer ID'].max()
    scenarios = (df['Scenario ID'] >= start_scenario) & (df['Scenario ID'] <= stop_scenario)
    
    for observer in range(number_of_observers):
        scores = df[scenarios & (df['Observer ID'] == observer+1)]['Observer Risk']
        scores.index = [i for i in range(start_scenario-1, stop_scenario)]
        srtr_scores = df[scenarios]['Scaled SRTR Risk'].drop_duplicates()
        n = len(scores)
        mse.append((1/n)*np.sum((scores - srtr_scores)**2))
        # print(f'MSE, Observer {observer + 1}:\t{mse[observer]}  (numerator: {np.sum((x-x_mean)**2)}, denominator: {len(x)})')
    return np.round(np.array(mse))


df = master_data[master_data['Observer Decision'] == 'Yes']
start_scenario = 1
stop_scenario = 30
mse = []
number_of_observers = df['Observer ID'].max()
scenarios = (df['Scenario ID'] >= start_scenario) & (df['Scenario ID'] <= stop_scenario)
for observer in range(number_of_observers):
    scores = df[scenarios & (df['Observer ID'] == observer+1)]['Observer Risk']
    scores.index = [i for i in range(start_scenario-1, stop_scenario)]
    srtr_scores = df[scenarios]['Scaled SRTR Risk'].drop_duplicates()
    n = len(scores)
    mse.append((1/n)*np.sum((scores - srtr_scores)**2))
    # print(f'MSE, Observer {observer + 1}:\t{mse[observer]}  (numerator: {np.sum((x-x_mean)**2)}, denominator: {len(x)})')
np.round(np.array(mse))
