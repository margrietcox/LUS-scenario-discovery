from ema_workbench import (RealParameter, IntegerParameter, BooleanParameter, ScalarOutcome, ArrayOutcome, Constant, Model, MultiprocessingEvaluator, Policy, perform_experiments, ema_logging )

ema_logging.log_to_stderr(ema_logging.INFO)
    
LUSmodel = Model('LUS', function=LUS_model)
    
LUSmodel.uncertainties = [  BooleanParameter('agrclaim'),
                            IntegerParameter('TigrisXLfile', 1, 4),
                            BooleanParameter('inbreiding'),
                            BooleanParameter('Density'),
                            BooleanParameter('Claimfile'),
                            IntegerParameter('natureclaim', 1, 3),
                            BooleanParameter('recvalue'),
                            BooleanParameter('restrictionnatureweight'),
                            IntegerParameter('naturepolicymap', 1, 3),
                            BooleanParameter('policyweightnature'),
                            BooleanParameter('spreidingratio'),
                            IntegerParameter('valuenaturelocation', 1, 3),
                            BooleanParameter('pumping')]
                                    
                               
                             

LUSmodel.outcomes = [ArrayOutcome('lusmap')]
    
n_scenarios = 10
 
    

            
    
    
    
   
    
    
    
 



            