
clustering = AgglomerativeClustering(n_clusters=6, affinity='precomputed', linkage='complete').fit_predict(kappa_df)

dfCART = experiments
y = clustering

#Because CART uses a ratio scale by default, on-hot encoder is performed to the categorical parameters
# in the experiments file:
for scen in np.unique(dfCART['TigrisXLfile']):
    dfCART['TigrisXLfile_{}'.format(scen)] = dfCART['TigrisXLfile']== scen
    dfCART['TigrisXLfile_{}'.format(scen)] = dfCART['TigrisXLfile_{}'.format(scen)].astype(int)
del dfCART['TigrisXLfile']

for scen in np.unique(dfCART['natureclaim']):
    dfCART['natureclaim_{}'.format(scen)] = dfCART['natureclaim']==scen
    dfCART['natureclaim_{}'.format(scen)] = dfCART['natureclaim_{}'.format(scen)].astype(int)
del dfCART['natureclaim']

for scen in np.unique(dfCART['naturepolicymap']):
    dfCART['naturepolicymap_{}'.format(scen)] = dfCART['naturepolicymap']==scen
    dfCART['naturepolicymap_{}'.format(scen)] = dfCART['naturepolicymap_{}'.format(scen)].astype(int)
del dfCART['naturepolicymap']

for scen in np.unique(dfCART['valuenaturelocation']):
    dfCART['valuenaturelocation_{}'.format(scen)] = dfCART['valuenaturelocation']==scen
    dfCART['valuenaturelocation_{}'.format(scen)] = dfCART['valuenaturelocation_{}'.format(scen)].astype(int)
del dfCART['valuenaturelocation']

for scen in np.unique(dfCART['policyweightnature']):
    dfCART['policyweightnature_{}'.format(scen)] = dfCART['policyweightnature']==scen
    dfCART['policyweightnature_{}'.format(scen)] = dfCART['policyweightnature_{}'.format(scen)].astype(int)
del dfCART['policyweightnature']


cart_alg = cart.CART(dfCART, y, mode = RuleInductionType.CLASSIFICATION)


cart_alg.build_tree()


cart_alg.stats_to_dataframe()
cart_alg.boxes_to_dataframe()
    
cart_alg.show_boxes(together=False)
plt.show()

tree = cart_alg.show_tree()
fig = plt.gcf()
fig.set_size_inches(10,10)
plt.show()
   
    
    
    
 



            
