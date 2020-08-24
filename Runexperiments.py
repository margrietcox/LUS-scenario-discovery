from subprocess import call
import os
import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from shutil import copyfile, move, copy, copytree, rmtree
from distutils.dir_util import copy_tree
from IPython.display import clear_output
from tempfile import mkstemp
from os import fdopen, remove

from ema_workbench import (RealParameter, CategoricalParameter, IntegerParameter, BooleanParameter, ScalarOutcome, ArrayOutcome, Constant, Model, MultiprocessingEvaluator, Policy, perform_experiments, ema_logging )
from ema_workbench import (save_results, load_results, experiments_to_scenarios)
from ema_workbench.em_framework import (sample_uncertainties)

from functools import partial
from multiprocessing import Pool, Lock
import seaborn as sns
import matplotlib.pyplot as plt
%matplotlib inline

import matplotlib.pyplot as plt
from scipy import stats
import pickle

from numpy.lib import recfunctions as rf
   

"""Change to your directory!""" 

os.chdir("C:/Users/Admin_2/Documents/Thesis/LUS/DeltaScenarios_TUdelft1")
notebook_dir = os.getcwd()
    
"""geodms run and general functions to change parameters"""
def geodmsrun(config, tree, geodms_dir = r"C:/Program Files/ObjectVision/GeoDms7212"): #change this to your GeoDms directory
    
    #change working directory
    notebook_dir = os.getcwd()
    os.chdir(geodms_dir)
    assert os.path.isdir(geodms_dir)
    
    print(os.getcwd())
    
    #run the geodms
    arg_exe = ['GeoDmsRun.exe', config, tree]
    call(arg_exe)
    
    #change back the working directory
    os.chdir(notebook_dir)
    print(os.getcwd())
    
def find_line(file_path, pattern):
    #Create temp file
    lines = []
    fh, abs_path = mkstemp()
    with fdopen(fh,'w') as new_file:
        with open(file_path) as old_file:
            for line in old_file:
                if pattern in line:
                    lines.append(line)
    return lines

#Function which will determine the new line containing the new value:
def new_line(beginline, line, new_val, endline):
    newline = beginline + str(new_val) + line[line.find(endline):]
    return newline

#Function which actually replaces the value of demand
def replace_line(beginline, file_path, pattern, new_val, endline):
    #Create temp file
    fh, abs_path = mkstemp()
    with fdopen(fh,'w') as new_file:
        with open(file_path) as old_file:
            for line in old_file:
                if line==pattern:
                    subst = new_line(beginline, line, new_val, endline)
                    new_file.write(line.replace(pattern, subst))
                else:
                    new_file.write(line)
    #Remove original file
    remove(file_path)
    #Move new file
    move(abs_path, file_path)
    
"""Functions to change parameters"""
def changeresidentialclaim(TigrisXLfile, inbreiding, Density):
    if TigrisXLfile == 1:
        TLXfilename = 'TigrisXL'
    elif TigrisXLfile == 2:
        TLXfilename = 'TigrisXL2'
    elif TigrisXLfile == 3:
        TLXfilename = 'TigrisXL3'
    elif TigrisXLfile == 4:
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
    

def changeworkclaim(TigrisXLfile, Claimfile):
    if TigrisXLfile == 1:
        TLXfilename = 'TigrisXL'
    elif TigrisXLfile == 2:
        TLXfilename = 'TigrisXL2'
    elif TigrisXLfile == 3:
        TLXfilename = 'TigrisXL3'
    elif TigrisXLfile == 4:
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
    


def changenatureclaim(natureclaim):
    if natureclaim == 1:
        natureha = 106000
    elif natureclaim == 2:
        natureha = 75000
    elif natureclaim == 3:
        natureha = 50000
    
    Naturedms = notebook_dir+'/PD/cfg/stam/Claims/TotalenInBron.dms' #change to location file
    Natureclaimsearch = 'attribute<claimHa> STOOM  := Nl/ID == 1[uint8] ?' #line of code it will look for to find where parameter should be changed
    naturebeginline = str('\t\t\t\tattribute<claimHa> STOOM  := Nl/ID == 1[uint8] ?  ') #how the line should look before the parameter value
    natureendline = str('[claimHa]') # how the line should look after the parameter value
    natureline = find_line(Naturedms, Natureclaimsearch)[0]
    
    
    replace_line(naturebeginline, Naturedms, natureline, natureha, natureendline ) #replaces the line
    
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
    
    
def naturesuitability(valuenaturelocation, policyweightnature, pumping):
    #changing the location factor value 
    if valuenaturelocation == 1:
        locationweight = '0.0'
        scenario1 = 'WARM,'
        scenario2 = 'DRUK'
    elif valuenaturelocation == 2: 
        locationweight = 'woongebied/locatie'
        scenario1 = 'STOOM,'
        scenario2 = 'DRUK'
    elif valuenaturelocation == 3:
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
    
    replace_line( locationweightbeginline, suitabilitynaturedms, locationweightline, locationweight, locationweightendline)
    replace_line( scenario2beginline, suitabilitynaturedms, scenario2line, scenario2, scenario2endline)
    replace_line( scenario1beginline, suitabilitynaturedms, scenario1line, scenario1, scenario1endline)
    
    if policyweightnature == 1:
        scenario1a = 'STOOM'
        scenario2a = 'DRUK'
        scenario3a = 'RUST'
    elif policyweightnature == 2: 
        scenario1a = 'DRUK'
        scenario2a = 'STOOM'
        scenario3a = 'RUST'
    elif policyweightnature == 3:
        scenario1a = 'RUST'
        scenario2a = 'DRUK'
        scenario3a = 'STOOM'
    elif policyweightnature == 4:
        scenario1a = 'WARM'
        scenario2a = 'DRUK'
        scenario3a = 'RUST'
        
    #changing the scenario:
    scenario1asearch = '//STOOM1a'
    scenario1aline = find_line(suitabilitynaturedms,scenario1asearch)[0]
    scenario1abeginline = '\t\t\t\tScenario == /ScenarioUnit/V/'
    scenario1aendline = ' && //STOOM1a'
   
    scenario2asearch = '//DRUK1a'
    scenario2aline = find_line(suitabilitynaturedms,scenario2asearch)[0]
    scenario2abeginline = '\t\t\t\t(Scenario == /ScenarioUnit/V/'
    scenario2aendline = ' || Scenario == /ScenarioUnit/V/PARIJS) //DRUK1a'
    
    scenario3asearch = '//RUST1a'
    scenario3aline = find_line(suitabilitynaturedms,scenario3asearch)[0]
    scenario3abeginline = '\t\t\t\tScenario == /ScenarioUnit/V/'
    scenario3aendline = ' //RUST1a'

    replace_line(scenario1abeginline, suitabilitynaturedms, scenario1aline, scenario1a,  scenario1aendline)
    replace_line(scenario2abeginline, suitabilitynaturedms, scenario2aline, scenario2a,  scenario2aendline)
    replace_line(scenario3abeginline, suitabilitynaturedms, scenario3aline, scenario3a,  scenario3aendline)
    
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
    
    
    
    replace_line( pumppolicybeginline, suitabilitynaturedms, pumppolicyline, pumppolicy, pumppolicyendline)
    
    
    
def changenaturepolicy(naturepolicymap, restrictionnatureweight):
    if naturepolicymap == 1:
        naturepolicy = 'RobuustVitaal_natuur' #or ehs_uitgekleed or functionele_natuur
    elif naturepolicymap == 2:
        naturepolicy = 'ehs_uitgekleed'
    elif naturepolicymap == 3:
        naturepolicy = 'functionele_natuur'
        
    
    #change policy maps nature
    suitabilitynaturedms = notebook_dir+'/PD/cfg/stam/Templates/geschiktheid/natuur.dms'
    policynaturesearch1 = ' //Policymaphere1'
    naturepolicy1line = find_line(suitabilitynaturedms,policynaturesearch1)[0]
    naturepolicy1beginline = '\t\t\t\t\t(Beleid/NatuurLandschap/'
    naturepolicy1endline =  ' >= 0[Classifications/Beleid/ndt_multi] //Policymaphere1'
    
    policynaturesearch2 = ' //Policymaphere2'
    naturepolicy2line = find_line(suitabilitynaturedms,policynaturesearch2)[0]
    naturepolicy2beginline = '\t\t\t\t&& Beleid/NatuurLandschap/'
    naturepolicy2endline =  ' >= 0[Classifications/Beleid/ndt_multi], //Policymaphere2'
   
    policynaturesearch3 = ' //Policymaphere3'
    naturepolicy3line = find_line(suitabilitynaturedms,policynaturesearch3)[0]
    naturepolicy3beginline = '\t\t\t\t&& Beleid/NatuurLandschap/'
    naturepolicy3endline =  ' >= 0[Classifications/Beleid/ndt_multi], //Policymaphere3'
    
    replace_line(naturepolicy1beginline, suitabilitynaturedms, naturepolicy1line, naturepolicy,  naturepolicy1endline)
    replace_line(naturepolicy2beginline, suitabilitynaturedms, naturepolicy2line, naturepolicy,  naturepolicy2endline)
    replace_line(naturepolicy3beginline, suitabilitynaturedms, naturepolicy3line, naturepolicy,  naturepolicy3endline)
    
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
        
    restrictionnaturesearch = '//onlythisone'
    restrictionnatureline = find_line(policyrestrictionsdms,restrictionnaturesearch)[0]
    restrictionnaturebeginline = '\t\t\t\t",  value('
    restrictionnatureendline = ', Eur_M2_jaarlijks)"//onlythisone'
    
    replace_line(restrnaturepolicybeginline, policyrestrictionsdms, restrnaturepolicyline, naturepolicy, restrnaturepolicyendline)
    replace_line(restrictionnaturebeginline, policyrestrictionsdms, restrictionnatureline, restrictionnatureweightvalue,  restrictionnatureendline)
    
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
    
    
"""Model function"""
def LUS_model(TigrisXLfile, inbreiding, Density, Claimfile, natureclaim, recvalue, restrictionnatureweight, naturepolicymap, policyweightnature, spreidingratio, valuenaturelocation, pumping, agrclaim):
    
    changeresidentialclaim(TigrisXLfile, inbreiding, Density)
    changeworkclaim(TigrisXLfile, Claimfile)
    changenatureclaim(natureclaim)
    changerecreationclaim(recvalue)
    changeagricultureclaim(agrclaim)
    
    naturesuitability(valuenaturelocation, policyweightnature, pumping)
    changehousingsuitability(spreidingratio)
    changenaturepolicy(naturepolicymap, restrictionnatureweight)
  
    
    
    #Run GeoDMS software:
    config = notebook_dir+'/PD/cfg/stam.dms'
    tree = '/EndResults/PerScenTimeUnit/STOOM_Y2012_Y2050/Run1'

    geodmsrun(config, tree)
    
    # Safe resulting land use map:
    src = notebook_dir+'/PD/cfg/stam/results/run1.asc'
    
    # Define output: 
    lusmap = np.loadtxt(src, skiprows=6)
    
    # Define dummy output:
    dummy = np.max(lusmap)
    
    return lusmap, dummy


"""Experimental set-up and run experiments"""
if __name__ == '__main__':
    
    ema_logging.log_to_stderr(ema_logging.INFO)
    
    LUSmodel = Model('LUS', function=LUS_model)
    
    LUSmodel.uncertainties = [  BooleanParameter('agrclaim'),
                                CategoricalParameter('TigrisXLfile', (1,2,3,4)),
                                BooleanParameter('inbreiding'),
                                BooleanParameter('Density'),
                                BooleanParameter('Claimfile'),
                                CategoricalParameter('natureclaim', (1,2,3)),
                                BooleanParameter('recvalue'),
                                BooleanParameter('restrictionnatureweight'),
                                CategoricalParameter('naturepolicymap', (1,2,3)),
                                CategoricalParameter('policyweightnature', (1,2,3,4)),
                                BooleanParameter('spreidingratio'),
                                CategoricalParameter('valuenaturelocation', (1,2,3)),
                                BooleanParameter('pumping')]
                                    
                               
                             

    LUSmodel.outcomes = [ArrayOutcome('lusmap')]
    
    bulk_scenarios_slice_reload = pickle.load( open( "bulk_scenarios_slice1.p", "rb" ) )#Load your scenario slice
    
    results = perform_experiments(LUSmodel, scenarios=bulk_scenarios_slice_reload)
    experiments, outcomes = results
    
    save_results(results, "EXPERIMENTS2000.tar.gz")

            