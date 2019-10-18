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

--------------------------------------------------------------------------------

colors = master_data['Observer Decision'].replace(['Yes', 'No'], ['green', 'red'])

plt.figure(figsize=(10, 10))
plt.scatter(master_data['SRTR Risk'], master_data['Observer Risk'], color=colors, alpha=0.1)
plt.xlabel('SRTR Risk Score')
plt.ylabel('Observer Risk Score')

df = master_data


# First, give each row a position in the 3x3 grid
pos_col = []
pos_row = []
for i in range(len(df)):
    obs = df['Observer Risk'].iloc[i]
    scaled_srtr = df['Scaled SRTR Risk'].iloc[i]
    if ( (obs >= 0)  & (obs <= 30)  ) & ( (scaled_srtr >= 0)  & (scaled_srtr <= 30)  ): #[0, 0]
        pos_col.append(0)
        pos_row.append(0)
    elif ( (obs > 30) & (obs <= 60)  ) & ( (scaled_srtr >= 0)  & (scaled_srtr <= 30)  ): #[1, 0]
        pos_col.append(1)
        pos_row.append(0)
    elif ( (obs > 60) & (obs <= 100) ) & ( (scaled_srtr >= 0)  & (scaled_srtr <= 30)  ): #[2, 0]
        pos_col.append(2)
        pos_row.append(0)
    elif ( (obs >= 0)  & (obs <= 30)  ) & ( (scaled_srtr > 30) & (scaled_srtr <= 60)  ): #[0, 1]
        pos_col.append(0)
        pos_row.append(1)
    elif ( (obs > 30) & (obs <= 60)  ) & ( (scaled_srtr > 30) & (scaled_srtr <= 60)  ): #[1, 1]
        pos_col.append(1)
        pos_row.append(1)
    elif ( (obs > 60) & (obs <= 100) ) & ( (scaled_srtr > 30) & (scaled_srtr <= 60)  ): #[2, 1]
        pos_col.append(2)
        pos_row.append(1)
    elif ( (obs >= 0)  & (obs <= 30)  ) & ( (scaled_srtr > 60) & (scaled_srtr <= 100) ): #[0, 2]
        pos_col.append(0)
        pos_row.append(2)
    elif ( (obs > 30) & (obs <= 60)  ) & ( (scaled_srtr > 60) & (scaled_srtr <= 100) ): #[1, 2]
        pos_col.append(1)
        pos_row.append(2)
    elif ( (obs > 60) & (obs <= 100) ) & ( (scaled_srtr > 60) & (scaled_srtr <= 100) ): #[2, 2]
        pos_col.append(2)
        pos_row.append(2)
    else:
        print(f'bing!  {i}')


srtr_min = df['SRTR Risk'].min()
srtr_max = df['SRTR Risk'].max()
srtr_range = srtr_max - srtr_min
srtr_third = srtr_range/3
text_start_x = srtr_min + srtr_third/2 - 2.5

obs_min = 0
obs_max = 100
obs_range = 100
obs_third = 33.3
text_start_y = obs_min + obs_third/2

plt.axvline(x=srtr_min + srtr_third, color='black')
plt.axvline(x=srtr_min + srtr_third*2, color='black')
plt.axvline(x=srtr_min, color='black')
plt.axvline(x=srtr_max, color='black')
# plt.axhline(x=obs_third, color='black')
# plt.axhline(x=obs_third*2, color='black')

df.insert(0, 'R', pos_row)
df.insert(0, 'C', pos_col)

# Second, get %Yes in each position
for col in range(3):
    for row in range(3):
        df_temp = df[(df['C'] == col) & (df['R'] == row)]['Observer Decision']
        df_y = df_temp[df_temp == 'Yes']
        df_n = df_temp[df_temp == 'No']
        N = len(df_temp)
        if N == 0:
            pct_y = 0
            pct_n = 0
        else:
            n_y = len(df_y)
            n_n = len(df_n)
            pct_y = round(100*(n_y/N),2)
            pct_n = round(100*(n_n/N),2)
        text_x = text_start_x + srtr_third*row
        text_y = text_start_y + obs_third*col
        txt = f'Yes {pct_y}%\nNo {pct_n}%'
        plt.text(text_x, text_y, txt)
        # print(f'[{col}, {row}]')
        # print(f'N={N},\t% Yes = {pct_y},\t% No = {pct_n}')
        # print(f'N={N}, n_y={n_y}, %Y = {100*(n_y/N)}')




--------------------------------------------------------------------------------


colors = master_data['Observer Decision'].replace(['Yes', 'No'], ['green', 'red'])

plt.figure(figsize=(10, 10))
# plt.scatter(master_data[master_data['Scenario Set'] == 'No SRTR Score']['SRTR Risk'], master_data[master_data['Scenario Set'] == 'No SRTR Score']['Observer Risk'], color=colors, alpha=0.1)
plt.scatter(master_data[master_data['Scenario Set'] == 'With SRTR Score']['SRTR Risk'], master_data[master_data['Scenario Set'] == 'With SRTR Score']['Observer Risk'], color=colors, alpha=0.1)
plt.xlabel('SRTR Risk Score')
plt.ylabel('Observer Risk Score')


df = master_data[master_data['Scenario Set'] == 'With SRTR Score'][['Observer Risk', 'Scaled SRTR Risk', 'SRTR Risk', 'Observer Decision']]


# First, give each row a position in the 3x3 grid
pos_col = []
pos_row = []
for i in range(len(df)):
    obs = df['Observer Risk'].iloc[i]
    scaled_srtr = df['Scaled SRTR Risk'].iloc[i]
    if ( (obs >= 0)  & (obs <= 100/3)  ) & ( (scaled_srtr >= 0)  & (scaled_srtr <= 100/3)  ): #[0, 0]
        pos_col.append(0)
        pos_row.append(0)
    elif ( (obs > 100/3) & (obs <= 200/3)  ) & ( (scaled_srtr >= 0)  & (scaled_srtr <= 100/3)  ): #[1, 0]
        pos_col.append(1)
        pos_row.append(0)
    elif ( (obs > 200/3) & (obs <= 100) ) & ( (scaled_srtr >= 0)  & (scaled_srtr <= 100/3)  ): #[2, 0]
        pos_col.append(2)
        pos_row.append(0)
    elif ( (obs >= 0)  & (obs <= 100/3)  ) & ( (scaled_srtr > 100/3) & (scaled_srtr <= 200/3)  ): #[0, 1]
        pos_col.append(0)
        pos_row.append(1)
    elif ( (obs > 100/3) & (obs <= 200/3)  ) & ( (scaled_srtr > 100/3) & (scaled_srtr <= 200/3)  ): #[1, 1]
        pos_col.append(1)
        pos_row.append(1)
    elif ( (obs > 200/3) & (obs <= 100) ) & ( (scaled_srtr > 100/3) & (scaled_srtr <= 200/3)  ): #[2, 1]
        pos_col.append(2)
        pos_row.append(1)
    elif ( (obs >= 0)  & (obs <= 100/3)  ) & ( (scaled_srtr > 200/3) & (scaled_srtr <= 100) ): #[0, 2]
        pos_col.append(0)
        pos_row.append(2)
    elif ( (obs > 100/3) & (obs <= 200/3)  ) & ( (scaled_srtr > 200/3) & (scaled_srtr <= 100) ): #[1, 2]
        pos_col.append(1)
        pos_row.append(2)
    elif ( (obs > 200/3) & (obs <= 100) ) & ( (scaled_srtr > 200/3) & (scaled_srtr <= 100) ): #[2, 2]
        pos_col.append(2)
        pos_row.append(2)
    else:
        print(f'bing!  {i}')


srtr_min = df['SRTR Risk'].min()
srtr_max = df['SRTR Risk'].max()
srtr_range = srtr_max - srtr_min
srtr_third = srtr_range/3
text_start_x = srtr_min + srtr_third/2 - 2.5

obs_min = 0
obs_max = 100
obs_range = 100
obs_third = 33.3
text_start_y = obs_min + obs_third/2

plt.axvline(x=srtr_min + srtr_third, color='black')
plt.axvline(x=srtr_min + srtr_third*2, color='black')
plt.axvline(x=srtr_min, color='black')
plt.axvline(x=srtr_max, color='black')
plt.axhline(y=obs_third, color='black')
plt.axhline(y=obs_third*2, color='black')
plt.axhline(y=obs_min, color='black')
plt.axhline(y=obs_max, color='black')


df.insert(0, 'R', pos_row)
df.insert(0, 'C', pos_col)



# Second, get %Yes in each position
for col in range(3):
    for row in range(3):
        df_temp = df[(df['C'] == col) & (df['R'] == row)]['Observer Decision']
        df_y = df_temp[df_temp == 'Yes']
        df_n = df_temp[df_temp == 'No']
        N = len(df_temp)
        if N == 0:
            pct_y = 0
            pct_n = 0
        else:
            n_y = len(df_y)
            n_n = len(df_n)
            pct_y = round(100*(n_y/N),2)
            pct_n = round(100*(n_n/N),2)
        text_x = text_start_x + srtr_third*row
        text_y = text_start_y + obs_third*col
        txt = f'Yes {pct_y}%\nNo {pct_n}%'
        plt.text(text_x, text_y, txt, fontsize=16)
        # print(f'[{col}, {row}]')
        # print(f'N={N},\t% Yes = {pct_y},\t% No = {pct_n}')
        # print(f'N={N}, n_y={n_y}, %Y = {100*(n_y/N)}')

plt.savefig('plot_SRTRvsObserver_WithSRTRScore_percents.jpg')
