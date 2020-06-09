"""Model definition function"""

def LUS_model(TigrisXLfile, inbreiding, Density, Claimfile, natureclaim, recvalue, restrictionnatureweight, naturepolicymap, policyweightnature, spreidingratio, valuenaturelocation, pumping, agrclaim):
    
    changeresidentialclaim(TigrisXLfile, inbreiding, Density)
    changeworkclaim(TigrisXLfile, Claimfile)
    changenatureclaim(natureclaim)
    changerecreationclaim(recvalue)
    changeagricultureclaim(agrclaim)
    
    naturesuitability(valuenaturelocation, policyweightnature, pumping)
    changehousingsuitability(spreidingratio)
    changenaturepolicy(naturepolicymap, restrictionnatureweight)
  
    
    
    #runmodel
    
    config = notebook_dir+'/PD/cfg/stam.dms'
    tree = '/EndResults/PerScenTimeUnit/STOOM_Y2012_Y2050/Run1'

    geodmsrun(config, tree)
    
    
    src = notebook_dir+'/PD/cfg/stam/results/run1.asc'
    
    lusmap = np.loadtxt(src, skiprows=6)
    
    dummy = np.max(lusmap)
    
    return lusmap, dummy

 
    

            
    
    
    
   
    
    
    
 



            
