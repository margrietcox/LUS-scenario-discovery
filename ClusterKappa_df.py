kappa_df = pd.read_csv('C:/Users/Admin_2/Documents/Thesis/LUS/kappa_file111.csv')
kappa_df = kappa_df.drop(columns=['Unnamed: 0'])

kappa_df = 1 - kappa_df #change to distance matrix. lower value -> less distance -> more similar
kappa_df[kappa_df<0]=0


sns.heatmap(kappa_df) #show heatmap

from sklearn.cluster import AgglomerativeClustering
clustering = AgglomerativeClustering(n_clusters=3, affinity='precomputed', linkage='complete').fit_predict(kappa_df)


            
    
    
    
   
    
    
    
 



            