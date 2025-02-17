# First, give each row a position in the 3x3 grid
def getGridPositions(df):
    """
    getGridPositions(pandas.DataFrame)

    returns:  dictionary of two arrays, 'col' and 'row'
    
    This function divides observer risk and scaled SRTR risk scores into three
    bins, and then assigns column and row numbers to each pair of risk scores
    in the DataFrame.
    """
    pos_col = []
    pos_row = []
    for i in range(len(df)):
        obs = df['Observer Risk'].iloc[i]
        scaled_srtr = df['Scaled SRTR Risk'].iloc[i]
        if ( (obs >= 0)  & (obs <= 100/3)  ) & ( (scaled_srtr >= 0)  & (scaled_srtr <= 100/3)  ): #[0, 0]
            pos_col.append(0)
            pos_row.append(0)
        elif ( (obs > 100/3) & (obs <= 200/3)  ) & ( (scaled_srtr >= 0)  & (scaled_srtr <= 100/3)  ): #[1, 0]
            pos_col.append(0)
            pos_row.append(1)
        elif ( (obs > 200/3) & (obs <= 100) ) & ( (scaled_srtr >= 0)  & (scaled_srtr <= 100/3)  ): #[2, 0]
            pos_col.append(0)
            pos_row.append(2)
        elif ( (obs >= 0)  & (obs <= 100/3)  ) & ( (scaled_srtr > 100/3) & (scaled_srtr <= 200/3)  ): #[0, 1]
            pos_col.append(1)
            pos_row.append(0)
        elif ( (obs > 100/3) & (obs <= 200/3)  ) & ( (scaled_srtr > 100/3) & (scaled_srtr <= 200/3)  ): #[1, 1]
            pos_col.append(1)
            pos_row.append(1)
        elif ( (obs > 200/3) & (obs <= 100) ) & ( (scaled_srtr > 100/3) & (scaled_srtr <= 200/3)  ): #[2, 1]
            pos_col.append(1)
            pos_row.append(2)
        elif ( (obs >= 0)  & (obs <= 100/3)  ) & ( (scaled_srtr > 200/3) & (scaled_srtr <= 100) ): #[0, 2]
            pos_col.append(2)
            pos_row.append(0)
        elif ( (obs > 100/3) & (obs <= 200/3)  ) & ( (scaled_srtr > 200/3) & (scaled_srtr <= 100) ): #[1, 2]
            pos_col.append(2)
            pos_row.append(1)
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
            #txt = f'Col: {col}\nRow: {row}'
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
#prependGridPositions(master_data)
