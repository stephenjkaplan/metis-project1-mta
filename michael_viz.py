mta_raw_data['TOTAL_TRAFFIC'] = mta_raw_data['ENTRIES_DELTA'] + mta_raw_data['EXITS_DELTA']
year_data_df = mta_raw_data.groupby(['Week','Year']).TOTAL_TRAFFIC.sum()
year_data = year_data_df.unstack(level=-1)
year_graph = year_data.drop([17, 26])
#Yearly span plot
year_graph.plot(figsize=(10,4))
plt.title("May and June by Year (2015-2020)", fontsize=20)
plt.ylabel('Total Entries', fontsize=14)
plt.xlabel('Week of the Year', fontsize=14)
plt.legend(bbox_to_anchor=(1, 1), loc=2)
sns.set_style("darkgrid", {"axes.facecolor": ".9"})