#  [row, col]
#       |       |       #
# [2,0] | [2,1] | [2,2] #
#       |       |       #
#-------+-------+-------#
#       |       |       #
# [1,0] | [1,1] | [1,2] #
#       |       |       #
#-------+-------+-------#
#       |       |       #
# [0,0] | [0,1] | [0,2] #
#       |       |       #

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


srtr_min = df['SRTR Risk'].min()
srtr_max = df['SRTR Risk'].max()
srtr_range = srtr_max - srtr_min
srtr_third = srtr_range/3
text_start_x = srtr_min + srtr_third/2 - 2

obs_min = 0
obs_max = 100
obs_range = 100
obs_third = 33.3
text_start_y = obs_min + obs_third/2 - 6

plt.axvline(x=srtr_min + srtr_third, color='black')
plt.axvline(x=srtr_min + srtr_third*2, color='black')
plt.axvline(x=srtr_min, color='black')
plt.axvline(x=srtr_max, color='black')
plt.axhline(y=obs_third, color='black')
plt.axhline(y=obs_third*2, color='black')
plt.axhline(y=obs_min, color='black')
plt.axhline(y=obs_max, color='black')


df.insert(0, 'C', pos_col)
df.insert(0, 'R', pos_row)



# Second, get %Yes in each position
for row in range(3):
    for col in range(3):
        df_temp = df[(df['R'] == row) & (df['C'] == col)]['Observer Decision']
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
        txt = f'[{row}, {col}]\nYes {pct_y}%\n  ({n_y} / {N})\n\nNo {pct_n}%\n  ({n_n} / {N})'
        plt.text(text_x, text_y, txt, fontsize=16)
        # print(f'[{col}, {row}]')
        # print(f'N={N},\t% Yes = {pct_y},\t% No = {pct_n}')
        # print(f'N={N}, n_y={n_y}, %Y = {100*(n_y/N)}')
