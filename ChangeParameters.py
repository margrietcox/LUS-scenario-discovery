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
    
    
#Change Industry & Commerce parameters
def changeworkclaim(TigrisXLfile, Claimfile):
    if TigrisXLfile == 1:
        TLXfilename = 'TigrisXL'
    elif TigrisXLfile == 2:
        TLXfilename = 'TigrisXL2'
    elif TigrisXLfile == 3:
        TLXfilename = 'TigrisXL3'
    else:
        TLXfilename = 'TigrisXL4'
    #Change work claim source data
    claimswerkendms = notebook_dir+'/PD/cfg/stam/Templates/ClaimsWerken.dms'
    workclaimsearch = '%SourceDataProjDir%/Claims/Tigris'
    workline = find_line(claimswerkendms, workclaimsearch)[0]
    workbeginline = '\t\t:\tStorageName = "=\'%SourceDataProjDir%/Claims/'
    workendline = '/\'+ dirname + \'/\' + jaar + \'/labour/labour.dat\'"\n'
    replace_line( workbeginline, claimswerkendms, workline, TLXfilename, workendline)
   
    if Claimfile == True:
        Claimfilename = 'Claims'
    else:
        Claimfilename = 'Claims2'

    #Change LVQ & TYQ files 
    LVQreadsearch = '%SourceDataProjDir%/Claims'
    LVQline = find_line(claimswerkendms,LVQreadsearch )[1]
    LVQbeginline = '\t\t:\tStorageName = "=\'%SourceDataProjDir%/'
    LVQendline = '/\'+ dirname + \'/\'+ jaar + \'/\'+ filename +\'\'"\n'
    
    
    TYQline = find_line(claimswerkendms,LVQreadsearch )[2]
    TYQbeginline = '\t\t:\tStorageName = "=\'%SourceDataProjDir%/'
    TYQendline = '/\'+ dirname + \'/\'+ jaar + \'/\'+ filename +\'\'"\n'
    
    
    replace_line( TYQbeginline, claimswerkendms,  TYQline, Claimfilename, TYQendline)
    replace_line( workbeginline, claimswerkendms, workline, TLXfilename, workendline)
    replace_line( LVQbeginline, claimswerkendms, LVQline, Claimfilename, LVQendline)
    
#Change Nature claim parameters
def changenatureclaim(natureclaim):
    if natureclaim == 1:
        natureha = 106000
    elif natureclaim == 2:
        natureha = 75000
    else: 
        natureha = 5000
    
    Naturedms = notebook_dir+'/PD/cfg/stam/Claims/TotalenInBron.dms' #change to location file
    Natureclaimsearch = 'attribute<claimHa> STOOM  := Nl/ID == 1[uint8] ?' #line of code it will look for to find where parameter should be changed
    naturebeginline = str('\t\t\t\tattribute<claimHa> STOOM  := Nl/ID == 1[uint8] ?  ') #how the line should look before the parameter value
    natureendline = str('[claimHa]') # how the line should look after the parameter value
    natureline = find_line(Naturedms, Natureclaimsearch)[0]
    replace_line(naturebeginline, Naturedms, natureline, natureha, natureendline ) #
    
#Change recreation claim parameters
def changerecreationclaim(recvalue):
    if recvalue == True:
        GEorRC = 'GE'
    else:
        GEorRC = 'RC'
    recreationdms = notebook_dir+'/PD/cfg/stam/Claims/TotalenInBron/Verblijfsrecreatie.dms'
    recreationclaimsearch = '%SourceDataProjDir%/Claims/Ruimte/verblijfsrec_'
    recline = find_line(recreationdms, recreationclaimsearch)[0]
    recbeginline = '        ", \'NaarCases(\'+quote(\'%SourceDataProjDir%/Claims/Ruimte/verblijfsrec_'
    recendline = '_provincie'
    
    
    replace_line(recbeginline, recreationdms, recline, GEorRC, recendline)
    
#Change agriculture claim parameters
def changeagricultureclaim(agrclaim):
    
    agrdms = notebook_dir+'/PD/cfg/stam/Claims/TotalenInBron/AgrIntens.dms'
    
    if agrclaim == True:
        glastuinbouwdecrease = 0.1
        opengroentenha = 27100
        bloembollenha = 23600
        boomgaardha = 17300
        boomteeltha = 17100
    else:
        glastuinbouwdecrease  = 0.3
        opengroentenha = 22100
        bloembollenha = 21200
        boomgaardha = 15400
        boomteeltha = 15400
        
    agrclaimsearch5 = 'attribute<ggHa> agr_glastuinbouw'
    agrbeginline5 = str('\t\t\tattribute<ggHa> agr_glastuinbouw (NL):= NL/ID == 1[uint8] ? InBasisjaar/In2011/agr_glastuinbouw + -')
    agrendline5 = '[float32]'
    agrline5 = find_line(agrdms, agrclaimsearch5)[1]
    
    agrclaimsearch1 = 'attribute<ggHa> agr_OpenGroenten (NL):= NL/ID == 1[uint8] ?'
    agrbeginline1 = str('\t\t\tattribute<ggHa> agr_OpenGroenten (NL):= NL/ID == 1[uint8] ? ')
    agrendline = '[ggHa]'
    agrline1 = find_line(agrdms, agrclaimsearch1)[1]
    
    agrclaimsearch2 = 'attribute<ggHa> agr_bloembollen'
    agrbeginline2 = str('\t\t\tattribute<ggHa> agr_bloembollen  (NL):= NL/ID == 1[uint8] ? ')
    agrline2 = find_line(agrdms, agrclaimsearch2)[1]
    
    agrclaimsearch3 = 'attribute<ggHa> agr_boomgaard'
    agrbeginline3 = str('\t\t\tattribute<ggHa> agr_boomgaard    (NL):= NL/ID == 1[uint8] ? ')
    agrline3 = find_line(agrdms, agrclaimsearch3)[1]
    
    agrclaimsearch4 = 'attribute<ggHa> agr_boomteelt'
    agrbeginline4 = str('\t\t\tattribute<ggHa> agr_boomteelt    (NL):= NL/ID == 1[uint8] ? ')
    agrline4 = find_line(agrdms, agrclaimsearch4)[1]
    
    replace_line(agrbeginline1, agrdms, agrline1, opengroentenha, agrendline)
    replace_line(agrbeginline5, agrdms, agrline5, glastuinbouwdecrease, agrendline5)
    replace_line(agrbeginline4, agrdms, agrline4, boomteeltha, agrendline)
    replace_line(agrbeginline2, agrdms, agrline2, bloembollenha, agrendline)
    replace_line(agrbeginline3, agrdms, agrline3, boomgaardha, agrendline)
    
#Change nature suitability parameters
def naturesuitability(valuenaturelocation, policyweightnature, pumping):
    #changing the location factor value 
    if valuenaturelocation == 1:
        locationweight = '0.0'
        scenario1 = 'STOOM,'
        scenario2 = 'DRUK'
    elif valuenaturelocation == 2: 
        locationweight = 'woongebied/locatie'
        scenario1 = 'STOOM,'
        scenario2 = 'DRUK'
    else:
        locationweight = '0.0'
        scenario1 = 'DRUK,'
        scenario2 = 'STOOM'
        
    suitabilitynaturedms = notebook_dir+'/PD/cfg/stam/Templates/geschiktheid/natuur.dms'

    #changing the scenario:
    scenario1search = 'Scenario == /ScenarioUnit/V/'
    scenario1line = find_line(suitabilitynaturedms,scenario1search )[0]
    scenario1beginline = '\t\t\t\tScenario == /ScenarioUnit/V/'
    scenario1endline = '\n'
   

    scenario2search = 'Scenario == /ScenarioUnit/V/'
    scenario2line = find_line(suitabilitynaturedms,scenario1search )[1]
    scenario2beginline = '\t\t\t\tScenario == /ScenarioUnit/V/'
    scenario2endline =  ' || Scenario == /ScenarioUnit/V/PARIJS,\n'
    
    
    #changing location factor value weight:
    locationweightsearch = 'value('
    locationweightline = find_line(suitabilitynaturedms,locationweightsearch )[3]
    locationweightbeginline = '\t\t\t\tvalue('
    locationweightendline = ', Eur_M2_jaarlijks)'
   
    
    #changing the policy stimuli weight: 
    if policyweightnature == True:
        policyweightnaturevalue = 5.0
    else:
        policyweightnaturevalue = 0.0
    
    policyweightsearch = 'value('
    policyline = find_line(suitabilitynaturedms,policyweightsearch)[7]
    policybeginline = '\t\t\t\tvalue('
    policyendline = ', Eur_M2_jaarlijks)\n'
   
    
    #changing fysical policy model structure:
    if pumping == True:
        pumppolicy = 'Bronnen/endstate/PotentieNat/PotentieNatPercentage'
    else:
        pumppolicy = 'Omgeving/natuurlandschap/NatuurAdaptatie/potentie_nathuidig'
        
    #Changing the pump policy: 
    pumppolicysearch = '//omdat in dit scenario wel wordt gepompt'
    pumppolicyline = find_line(suitabilitynaturedms,pumppolicysearch)[0]
    pumppolicybeginline = '\t\t\t\t\t\t'
    pumppolicyendline =  '//omdat in dit scenario wel wordt gepompt bij bodemdaling\n'
    
    replace_line(policybeginline, suitabilitynaturedms, policyline, policyweightnaturevalue,  policyendline)
    replace_line( locationweightbeginline, suitabilitynaturedms, locationweightline, locationweight, locationweightendline)
    replace_line( scenario2beginline, suitabilitynaturedms, scenario2line, scenario2, scenario2endline)
    replace_line( scenario1beginline, suitabilitynaturedms, scenario1line, scenario1, scenario1endline)
    replace_line( pumppolicybeginline, suitabilitynaturedms, pumppolicyline, pumppolicy, pumppolicyendline)

#Change Residential suitability parameters
def changehousingsuitability(spreidingratio):
    if spreidingratio == True: 
        ratio = 0.5
    else:
        ratio = 1.0
    #Changing the spread ratio:
    housingsuitabilitydms = notebook_dir+'/PD/cfg/stam/Templates/geschiktheid/woongebied.dms'
    spreidingratiosearch = 'iif(Spreiding'
    spreidingratioline = find_line(housingsuitabilitydms,spreidingratiosearch)[0]
    spreidingratiobeginline = '\t\t* iif(Spreiding, value('
    spreidingratioendline = ', Ratio), value(1.0, Ratio))\n'
    
    
    replace_line( spreidingratiobeginline, housingsuitabilitydms,  spreidingratioline, ratio, spreidingratioendline)   
    
#Change nature policy
def changenaturepolicy(naturepolicymap, restrictionnatureweight):
    if naturepolicymap == 1:
        naturepolicy = 'RobuustVitaal_natuur' #or ehs_uitgekleed or functionele_natuur
    elif naturepolicymap == 2:
        naturepolicy = 'ehs_uitgekleed'
    else:
        naturepolicy = 'functionele_natuur'
    
    #change policy maps nature
    suitabilitynaturedms = notebook_dir+'/PD/cfg/stam/Templates/geschiktheid/natuur.dms'
    policynaturesearch = '(Beleid/NatuurLandschap/'
    naturepolicyline = find_line(suitabilitynaturedms,policynaturesearch)[0]
    naturepolicybeginline = '\t\t\t\t\t(Beleid/NatuurLandschap/'
    naturepolicyendline =  ' >= 0[Classifications/Beleid/ndt_multi]\n'
   
    
    policyrestrictionsdms = notebook_dir+'/PD/cfg/stam/Templates/geschiktheid/beleid_restricties.dms'
    restrictionnaturepolicysearch = '"&& Beleid/NatuurLandschap/'
    restrnaturepolicyline = find_line(policyrestrictionsdms,restrictionnaturepolicysearch)[0]
    restrnaturepolicybeginline = '\t\t\t\t"&& Beleid/NatuurLandschap/'
    restrnaturepolicyendline =  ' >= 0[Classifications/Beleid/ndt_multi]"\n'
   
    
    #change wieght policy restriction
    if restrictionnatureweight == True:
        restrictionnatureweightvalue = 30.0
    else:
        restrictionnatureweightvalue = 0.0
        
    restrictionnaturesearch = '",  value('
    restrictionnatureline = find_line(policyrestrictionsdms,restrictionnaturesearch)[2]
    restrictionnaturebeginline = '\t\t\t\t",  value('
    restrictionnatureendline = ', Eur_M2_jaarlijks)"\n'
    
    
    replace_line(naturepolicybeginline, suitabilitynaturedms, naturepolicyline, naturepolicy,  naturepolicyendline)
    replace_line(restrictionnaturebeginline, policyrestrictionsdms, restrictionnatureline, restrictionnatureweightvalue,  restrictionnatureendline)
    replace_line(restrnaturepolicybeginline, policyrestrictionsdms, restrnaturepolicyline, naturepolicy, restrnaturepolicyendline)
    




 
    

            
    
    
    
   
    
    
    
 



            
