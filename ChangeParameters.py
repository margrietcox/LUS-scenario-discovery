#Change residential claim
def changeresidentialclaim(TigrisXLfile, inbreiding, Density):
    if TigrisXLfile == 1:
        TLXfilename = 'TigrisXL'
    elif TigrisXLfile == 2:
        TLXfilename = 'TigrisXL2'
    elif TigrisXLfile == 3:
        TLXfilename = 'TigrisXL3'
    else:
        TLXfilename = 'TigrisXL4'
    #Change TigrisXL file in claimswonen.dms and claimspopulation.dms
    claimswonendms = notebook_dir+'/PD/cfg/stam/Templates/ClaimsWonen.dms'
    claimspopulationdms = notebook_dir+'/PD/cfg/stam/Templates/ClaimsPopulation.dms'
    houseclaimsearch = '%SourceDataProjDir%/Claims/Tigris'
    housebeginline = '\t\t:\tStorageName = "=\'%SourceDataProjDir%/Claims/'
    houseendline = '/\'+ ClaimSrcDir + \'/landuse/landuse.dat\'"\n'
    popbeginline = '\t\t,\tStorageName = "=\'%SourceDataProjDir%/Claims/'
    popendline ='/\'+ dirname + \'/\' + jaar + \'/segs/segs.dbf\'"\n'
    
    houseline = find_line(claimswonendms,houseclaimsearch)[0]
    popline = find_line(claimspopulationdms, houseclaimsearch)[0]
    
    
    #Change densityfactor and Infringement fraction in scenarios.dms
    if inbreiding == True:
        inbreidingvalue = 0.25
    else:
        inbreidingvalue = 0.75
    
    scenariosdms = notebook_dir+'/PD/cfg/stam/Classifications/Scenarios.dms'
    
    inbreidingclaimsearch = 'attribute<float32> Inbreidingsfractie'
    inbreidingbeginline = '\t\t\tattribute<float32> Inbreidingsfractie : ['
    inbreidingendline = ', 0.75]'
    
    inbreidingline = find_line(scenariosdms, inbreidingclaimsearch)[0]
    replace_line(inbreidingbeginline, scenariosdms, inbreidingline, inbreidingvalue, inbreidingendline)
    
    if Density == True:
        densityvalue = 1.33
    else:
        densityvalue = 1.0
    
    densclaimsearch = 'attribute<float32> DensityFactor'
    densline = find_line(scenariosdms, densclaimsearch)[0]
    densbeginline = '\t\t\tattribute<float32> DensityFactor: ['
    densendline = ', 1.33]'
    
    
    replace_line(housebeginline, claimswonendms, houseline, TLXfilename, houseendline)
    replace_line(popbeginline, claimspopulationdms, popline, TLXfilename, popendline)
    replace_line(densbeginline, scenariosdms, densline, densityvalue, densendline)




 
    

            
    
    
    
   
    
    
    
 



            