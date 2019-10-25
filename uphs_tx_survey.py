def getCounts(df, first_scenario=1, last_scenario=60, grid_size=(3,3)):
    scenario_mask = (df['Scenario ID'] >= first_scenario) & (df['Scenario ID'] <= last_scenario)
    num_rows = grid_size[0]
    num_cols = grid_size[1]
    srtr_min = df['SRTR Risk'].min()
    srtr_max = df['SRTR Risk'].max()
    srtr_range = srtr_max - srtr_min
    srtr_step = srtr_range/num_cols
    obs_min = 0
    obs_max = 100
    obs_range = obs_max - obs_min
    obs_step = obs_range/num_rows
    srtr_breaks = []
    obs_breaks = []
    for i in range(num_cols):
        srtr_breaks[i] = srtr_min + srtr_step*i
    for i in range(num_rows):
        obs_breaks[i] = obs_min + obs_step*i
    yes = []
    no = []
    total = []
    for row in range(num_rows):
        for col in range(num_cols):
            df_count = df[scenario_mask & (df['SRTR Risk'] >= srtr_breaks[0]) & ...
            yes[row, col] = df[





df_plot = master_data[master_data['Scenario Set'] == 'With SRTR Score']

colors = df_plot['Observer Decision'].replace(['Yes', 'No'], ['green', 'red'])


plt.figure(figsize=(10, 10))
plt.scatter(df_plot['SRTR Risk'], df_plot['Observer Risk'], color=colors, alpha=0.1)
# plt.scatter(master_data['SRTR Risk'], master_data[master_data['Scenario Set'] == 'With SRTR Score']['Observer Risk'], color=colors, alpha=0.1)
plt.xlabel('SRTR Risk Score')
plt.ylabel('Observer Risk Score')


df = df_plot[['Observer Risk', 'Scaled SRTR Risk', 'SRTR Risk', 'Observer Decision']]

# First, give each row a position in the 3x3 grid
def getGridPositions(df):
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
    return { 'row': pos_row, 'col': pos_col }

def prependGridPositions(df):
    df_temp = df[['Observer Risk', 'Scaled SRTR Risk', 'SRTR Risk', 'Observer Decision']]
    positions = getGridPositions(df_temp)
    df_temp.insert(0, 'R', positions['row'])
    df_temp.insert(0, 'C', positions['col'])
    return df_temp
    





def plotTernaryPercents(df):
    df_pos = prependGridPositions(df)
    srtr_min = df_pos['SRTR Risk'].min()
    srtr_max = df_pos['SRTR Risk'].max()
    srtr_range = srtr_max - srtr_min
    srtr_third = srtr_range/3
    obs_min = 0
    obs_max = 100
    obs_range = 100
    obs_third = 33.3
    text_start_x = srtr_min + srtr_third/2 - 2.5
    text_start_y = obs_min + obs_third/2
    colors = df_pos['Observer Decision'].replace(['Yes', 'No'], ['green', 'red'])
    plt.figure(figsize=(10, 10))
    plt.scatter(df_pos['SRTR Risk'], df_pos['Observer Risk'], color=colors, alpha=0.1)
    plt.xlabel('SRTR Risk Score')
    plt.ylabel('Observer Risk Score')
    for col in range(3):
        for row in range(3):
            df_temp = df_pos[(df_pos['C'] == col) & (df_pos['R'] == row)]['Observer Decision']
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
            text_x = text_start_x + srtr_third*col
            text_y = text_start_y + obs_third*row
            txt = f'Yes {pct_y}%\n  ({n_y} / {N})\n\nNo {pct_n}%\n  ({n_n} / {N})'
            ## The rows and columns are correct
            ## Check that your table is indexed correctly by prependGridPositions()
            txt = f'Col: {col}\nRow: {row}'
            plt.text(text_x, text_y, txt, fontsize=16)
    plt.title('SRTR vs. Observer Risk, with SRTR Score', fontsize=16)
    plt.axvline(x=srtr_min + srtr_third, color='black')
    plt.axvline(x=srtr_min + srtr_third*2, color='black')
    plt.axvline(x=srtr_min, color='black')
    plt.axvline(x=srtr_max, color='black')
    plt.axhline(y=obs_third, color='black')
    plt.axhline(y=obs_third*2, color='black')
    plt.axhline(y=obs_min, color='black')
    plt.axhline(y=obs_max, color='black')
plotTernaryPercents(master_data)

plt.savefig('plot_SRTRvsObserver_WithSRTRScore_percents.jpg')
