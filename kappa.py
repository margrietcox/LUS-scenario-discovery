def calc_total_cells(mask):
    x = np.unique(mask, return_counts=True)[-1][-1]
    return x
    
def calc_agreement(mask, map1, map2, Pe1_array, Pe2_array, Po_array, pair):
    i = pair[0]
    j = pair[1]
    if mask[i,j] != 0:
        x = map1[i, j]
        y = map2[i, j]
        # Amend the expected array count
        Pe1_array[x]=Pe1_array[x]+1
        Pe2_array[y]=Pe2_array[y]+1
        # If there is agreement, amend the observed count
        if x == y:
            Po_array[x] = Po_array[x] + 1
            
def kappa(map1, map2, mask, total_cells=0):
    # Determine the map dimensions and number of land-use classes.
    shape_map1 = np.shape(map1)
    row = shape_map1[0]
    column = shape_map1[1]
    luc = np.amax(map1) + 1
    # Determine the total number of cells to be considered.
    if total_cells==0:
        for i in range(0, row):
            for j in range(0, column):
                x = mask[i, j]
                if x != 0:
                    total_cells = total_cells + 1
    # Initialise an array to store the observed agreement probability.
    Po_array = np.zeros(shape=luc)
    # Initialise a set of arrays to store the expected agreement probability,
    # for both maps, and then combined.
    Pe1_array = np.zeros(shape=luc)
    Pe2_array = np.zeros(shape=luc)
    Pe_array = np.zeros(shape=luc)
    # Initialise an array to store the maximum possible agreement probability.
    Pmax_array=np.zeros(shape=luc)
    # Analyse the agreement between the two maps.
                
    arg_pairs = [(i,j) for i in range(row) for j in range(column)]
    pool = Pool()
    func = partial(calc_agreement, mask, map1, map2, Pe1_array, Pe2_array, Po_array)
    pool.map(func, arg_pairs)
        
    
    for i in range(0, row):
        for j in range(0, column):
            if mask[i,j] != 0:
                x = map1[i, j]
                y = map2[i, j]
                # Amend the expected array count
                Pe1_array[x]=Pe1_array[x]+1
                Pe2_array[y]=Pe2_array[y]+1
                # If there is agreement, amend the observed count
                if x == y:
                        Po_array[x] = Po_array[x] + 1
    # Convert to probabilities.
    Po_array[:] = [x/total_cells for x in Po_array]
    Pe1_array[:] = [x/total_cells for x in Pe1_array]
    Pe2_array[:] = [x/total_cells for x in Pe2_array]
    # Now process the arrays to determine the maximum and expected
    # probabilities.
    for i in range(0, luc):
        Pmax_array[i] = min(Pe1_array[i], Pe2_array[i])
        Pe_array[i] = Pe1_array[i]*Pe2_array[i]
    # Calculate the values of probability observed, expected, and max.
    Po = np.sum(Po_array)
    Pmax = np.sum(Pmax_array)
    Pe = np.sum(Pe_array)
    # Now calculate the Kappa histogram and Kappa location.
    Khist = (Pmax - Pe)/(1 - Pe)
    Kloc = (Po - Pe)/(Pmax - Pe)
    # Finally, calculate Kappa.
    Kappa=Khist*Kloc
    # Return the value of Kappa.
    return Kappa

"""Calculate kappa via cmd"""

if __name__ == '__main__':
    
    results = load_results("30_5_500.tar.gz")
    print('resultsready')
    experiments, outcomes = results
    ooi = outcomes['lusmap'].astype(int)
        
    src = 'C:/Users/Admin_2/Documents/Thesis/LUS/regionboundaries.asc'
    a = np.loadtxt(src, skiprows=6)
    mask = np.where((a == 24) | (a ==28 ), 0 , 1)
    total_cells = calc_total_cells(mask)
    
    y = []
    for j in range(len(ooi)):
        map1 = ooi[j]
        for i in range(len(ooi)):
            map2 = ooi[i]
            kvalue = kappa(map1, map2, mask, total_cells) 
            x = [i,j,kvalue]
            y.append(x)
            i + 1 
        j+1 
     
    df = pd.DataFrame(np.ones((len(ooi), len(ooi))))
    for item in y:
        try:
            i = item[0]
            j = item[1]
            k = item[2]
            df[i][j] = k
        except:
            pass

    df.to_csv('kappa_df_500.csv')

 
    

            
    
    
    
   
    
    
    
 



            
