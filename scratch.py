
def results_sorted_by_srtr(df):
    results_a = df.loc[(df['Scenario ID'] <= 30)][['Scenario ID', 'Observer Risk', 'Scaled SRTR Risk']]
    results_b = df.loc[(df['Scenario ID'] > 30)][['Scenario ID', 'Observer Risk', 'Scaled SRTR Risk']]
    results_a_sorted =     results_a.sort_values('Scaled SRTR Risk')
    results_b_sorted =     results_b.sort_values('Scaled SRTR Risk')
    results_a_sort_order = results_a_sorted['Scenario ID'].drop_duplicates()
    results_b_sort_order = results_b_sorted['Scenario ID'].drop_duplicates()
    srtr_a_sorted = results_a_sorted[['Scenario ID', 'Scaled SRTR Risk']].drop_duplicates()
    srtr_a_sorted.index = [i for i in range(30)]
    srtr_b_sorted = results_b_sorted[['Scenario ID', 'Scaled SRTR Risk']].drop_duplicates()
    srtr_b_sorted.index = [i for i in range(30)]
    return {
        'title':                      'Scaled SRTR Risk Score',
        'first_results':              results_a,
        'first_results_sorted':       results_a_sorted,
        'first_results_sort_order':   results_a_sort_order,
        'first_srtr_sorted':          srtr_a_sorted,
        'second_results':             results_b,
        'second_results_sorted':      results_b_sorted,
        'second_results_sort_order':  results_b_sort_order,
        'second_srtr_sorted':         srtr_b_sorted
    }

def results_sorted_by_mean(df):
    results_a = df.loc[(df['Scenario ID'] <= 30)][['Scenario ID', 'Observer Risk', 'Scaled SRTR Risk']]
    results_b = df.loc[(df['Scenario ID'] > 30)][['Scenario ID', 'Observer Risk', 'Scaled SRTR Risk']]
    results_a_sorted =     results_a.groupby('Scenario ID').mean().sort_values('Observer Risk').reset_index()
    results_b_sorted =     results_b.groupby('Scenario ID').mean().sort_values('Observer Risk').reset_index()
    results_a_sort_order = results_a_sorted['Scenario ID'].drop_duplicates()
    results_b_sort_order = results_b_sorted['Scenario ID'].drop_duplicates()
    srtr_a_sorted = results_a_sorted[['Scenario ID', 'Scaled SRTR Risk']].drop_duplicates()
    srtr_a_sorted.index = [i for i in range(30)]
    srtr_b_sorted = results_b_sorted[['Scenario ID', 'Scaled SRTR Risk']].drop_duplicates()
    srtr_b_sorted.index = [i for i in range(30)]
    return {
        'title':                      'Mean Observer Risk Score',
        'first_results':              results_a,
        'first_results_sorted':       results_a_sorted,
        'first_results_sort_order':   results_a_sort_order,
        'first_srtr_sorted':          srtr_a_sorted,
        'second_results':             results_b,
        'second_results_sorted':      results_b_sorted,
        'second_results_sort_order':  results_b_sort_order,
        'second_srtr_sorted':         srtr_b_sorted
    }

def results_sorted_by_median(df):
    results_a = df.loc[(df['Scenario ID'] <= 30)][['Scenario ID', 'Observer Risk', 'Scaled SRTR Risk']]
    results_b = df.loc[(df['Scenario ID'] > 30)][['Scenario ID', 'Observer Risk', 'Scaled SRTR Risk']]
    results_a_sorted =     results_a.groupby('Scenario ID').median().sort_values('Observer Risk').reset_index()
    results_b_sorted =     results_b.groupby('Scenario ID').median().sort_values('Observer Risk').reset_index()
    results_a_sort_order = results_a_sorted['Scenario ID'].drop_duplicates()
    results_b_sort_order = results_b_sorted['Scenario ID'].drop_duplicates()
    srtr_a_sorted = results_a_sorted[['Scenario ID', 'Scaled SRTR Risk']].drop_duplicates()
    srtr_a_sorted.index = [i for i in range(30)]
    srtr_b_sorted = results_b_sorted[['Scenario ID', 'Scaled SRTR Risk']].drop_duplicates()
    srtr_b_sorted.index = [i for i in range(30)]
    return {
        'title':                      'Median Observer Risk Score',
        'first_results':              results_a,
        'first_results_sorted':       results_a_sorted,
        'first_results_sort_order':   results_a_sort_order,
        'first_srtr_sorted':          srtr_a_sorted,
        'second_results':             results_b,
        'second_results_sorted':      results_b_sorted,
        'second_results_sort_order':  results_b_sort_order,
        'second_srtr_sorted':         srtr_b_sorted
    }


def results_sorted_by_scenario(df):
    results_a = df.loc[(df['Scenario ID'] <= 30)][['Scenario ID', 'Observer Risk', 'Scaled SRTR Risk']]
    results_b = df.loc[(df['Scenario ID'] > 30)][['Scenario ID', 'Observer Risk', 'Scaled SRTR Risk']]
    results_a_sorted = results_a
    results_b_sorted = results_b
    results_a_sort_order = results_a_sorted['Scenario ID'].drop_duplicates()
    results_b_sort_order = results_b_sorted['Scenario ID'].drop_duplicates()
    srtr_a_sorted = results_a_sorted[['Scenario ID', 'Scaled SRTR Risk']].drop_duplicates()
    srtr_a_sorted.index = [i for i in range(30)]
    srtr_b_sorted = results_b_sorted[['Scenario ID', 'Scaled SRTR Risk']].drop_duplicates()
    srtr_b_sorted.index = [i for i in range(30)]
    return {
        'title':                      'Scenario',
        'first_results': results_a,
        'first_results_sorted': results_a_sorted,
        'first_results_sort_order': results_a_sort_order,
        'first_srtr_sorted': srtr_a_sorted,
        'second_results': results_b,
        'second_results_sorted': results_b_sorted,
        'second_results_sort_order': results_b_sort_order,
        'second_srtr_sorted': srtr_b_sorted
    }

def results_sorted_by_interquartitle_range(df):
    from scipy.stats import iqr
    results_a = df.loc[(df['Scenario ID'] <= 30)][['Scenario ID', 'Observer Risk', 'Scaled SRTR Risk']]
    results_b = df.loc[(df['Scenario ID'] > 30)][['Scenario ID', 'Observer Risk', 'Scaled SRTR Risk']]
    # Make two lists of interquartile ranges
    iqr_list = []
    for scenario in df['Scenario ID']:
        iqr_list.append(iqr(df[df['Scenario ID'] == scenario]['Observer Risk']))
    iqr_df = pd.DataFrame(iqr_list, columns=['IQR'])
    iqr_df = iqr_df[:60]
    iqr_df.insert(0, 'Scenario ID', [i+1 for i in range(60)])
    iqr_df.insert(2, 'Scaled SRTR Risk', df[['Scenario ID', 'Scaled SRTR Risk']].drop_duplicates()['Scaled SRTR Risk'])
    iqr_a = iqr_df[:30]
    iqr_b = iqr_df[30:]
    results_a_sorted = iqr_a.sort_values('IQR')
    results_a_sort_order = results_a_sorted['Scenario ID']
    srtr_a_sorted = results_a_sorted
    srtr_a_sorted.index = [i for i in range(30)]
    results_b_sorted = iqr_b.sort_values('IQR')
    results_b_sort_order = results_b_sorted['Scenario ID']
    srtr_b_sorted = results_b_sorted
    srtr_b_sorted.index = [i for i in range(30)]
    return {
        'title':                      'Interquartile Range',
        'first_results':              results_a,
        'first_results_sorted':       results_a_sorted,
        'first_results_sort_order':   results_a_sort_order,
        'first_srtr_sorted':          srtr_a_sorted,
        'second_results':             results_b,
        'second_results_sorted':      results_b_sorted,
        'second_results_sort_order':  results_b_sort_order,
        'second_srtr_sorted':         srtr_b_sorted
    }
    
    
# iqr(results_a, axis=0)
# a = []
# for scenario in results_a['Scenario ID']:
#     a.append(iqr(results_a[results_a['Scenario ID'] == scenario]['Observer Risk']))
# df = pd.DataFrame(a, columns=['IQR'])
# df = df[:30]
# df.insert(0,'Scenario ID', [i+1 for i in range(30)])
# df.sort_values('IQR').index
#a = results_sorted_by_mean(master_data)
#a[1]
    
def boxplot_survey(df, sort_by='scenario'):
    plt.figure(figsize=(20, 10))
    if (sort_by == 'mean'):
        results = results_sorted_by_mean(df)
    if (sort_by == 'scenario'):
        results = results_sorted_by_scenario(df)
    if (sort_by == 'srtr'):
        results = results_sorted_by_srtr(df)
    if (sort_by == 'median'):
        results = results_sorted_by_median(df)
    first_results = results['first_results']
    first_results_sorted = results['first_results_sorted']
    first_results_sort_order = results['first_results_sort_order']
    first_srtr_sorted = results['first_srtr_sorted']
    second_results = results['second_results']
    second_results_sorted = results['second_results_sorted']
    second_results_sort_order = results['second_results_sort_order']
    second_srtr_sorted = results['second_srtr_sorted']

    plt.subplot(2, 1, 1)
    ax_1 = sns.boxplot(x='Scenario ID', y='Observer Risk', data=first_results, order=first_results_sort_order)
    ax_1 = plt.scatter(first_srtr_sorted.index.values, first_srtr_sorted['Scaled SRTR Risk'])
    
    plt.subplot(2, 1, 2)
    ax_2 = sns.boxplot(x='Scenario ID', y='Observer Risk', data=second_results, order=second_results_sort_order)
    ax_2 = plt.scatter(second_srtr_sorted.index.values, second_srtr_sorted['Scaled SRTR Risk'])
    
    plt.suptitle(f'Scenario Risk Scores, sorted by {results["title"]}', fontsize=16)



boxplot_survey(master_data, 'scenario')

#plt.savefig('plot_BoxPerScenario_sortSRTR.jpg')

