from hypothesisEngine.fitness.base_ff_classes.base_ff import base_ff
from hypothesisEngine.fitness.expression import *
from hypothesisEngine.fitness.fitness_helper import *
import hypothesisEngine.fitness.weights as weight
import hypothesisEngine.fitness.weights_to_bets as wb

import numpy as np
import math as mth
import textwrap


class Maximum_Drawdown(base_ff):
    """
    Basic fitness function template for writing new fitness functions. This
    basic template inherits from the base fitness function class, which
    contains various checks and balances.
    
    Note that all fitness functions must be implemented as a class.
    
    Note that the class name must be the same as the file name.
    
    Important points to note about base fitness function class from which
    this template inherits:
    
      - Default Fitness values (can be referenced as "self.default_fitness")
        are set to NaN in the base class. While this can be over-written,
        PonyGE2 works best when it can filter solutions by NaN values.
    
      - The standard fitness objective of the base fitness function class is
        to minimise fitness. If the objective is to maximise fitness,
        this can be over-written by setting the flag "maximise = True".
    
    """

    # The base fitness function class is set up to minimise fitness.
    # However, if you wish to maximise fitness values, you only need to
    # change the "maximise" attribute here to True rather than False.
    # Note that if fitness is being minimised, it is not necessary to
    # re-define/overwrite the maximise attribute here, as it already exists
    # in the base fitness function class.
    maximise = False

    def __init__(self):
        """
        All fitness functions which inherit from the bass fitness function
        class must initialise the base class during their own initialisation.
        """
#        log = logging.getLogger(__name__)
        # Initialise base fitness function class.
        super().__init__()
        
    @staticmethod
    def fitness_exp(strategy,params):


        strategy_weights = weight.weights(datasets_dict['Sectors'],strategy,params['NEUTRALIZATION'] ,params['LONG LEVERAGE'] ,params['SHORT LEVERAGE'] )
        

#        print("check") 
        
        #Simple Checks
        empty = np.full_like(strategy_weights,np.nan)    
        check=((strategy_weights == empty) | (np.isnan(strategy_weights) & np.isnan(empty))).all() 
        if check:
            strategy_weights = np.full_like(strategy_weights,0)   
            
        non_nan_frac = np.count_nonzero(~np.isnan(strategy_weights))/np.size(strategy_weights)
        if non_nan_frac<=0.6:
            strategy_weights = np.full_like(strategy_weights,0) 

           
        clean_values_from_weights = wb.get_valid_index(strategy_weights)
        cleaned_index_weights = (clean_index.values)[clean_values_from_weights]
        cleaned_strategy_weights       = strategy_weights[clean_values_from_weights]  
        

        
        strategy_log_returns,strategy_daily_returns = wb.bets_to_pnl(params['STARTING VALUE'] ,strategy_weights,clean_values_from_weights,base_data,params['LONG LEVERAGE'] , params['SHORT LEVERAGE'] , params['ADV THRESHOLD PERCENTAGE'],params['COST THRESHOLD BPS'],params['COMMISSION BPS']) 
 
        def MDD(returns):
            def returns_to_dollars(amount,ret):
                return amount*np.cumprod(1+ret)
            
            doll_series = pd.Series(returns_to_dollars(100,returns))
            
            Roll_Max = doll_series.cummax()
            Daily_Drawdown = doll_series/Roll_Max - 1.0
            Max_Daily_Drawdown = Daily_Drawdown.cummin()
            return Max_Daily_Drawdown

        
        if np.sum(strategy_daily_returns)==0:
            return 0
        else:
            fitness = abs(MDD(strategy_log_returns).min()*100)
            return fitness
    
    def evaluate(self, ind, **kwargs):
        """
        Default fitness execution call for all fitness functions. When
        implementing a new fitness function, this is where code should be added
        to evaluate target phenotypes.
        
        There is no need to implement a __call__() method for new fitness
        functions which inherit from the base class; the "evaluate()" function
        provided here allows for this. Implementing a __call__() method for new
        fitness functions will over-write the __call__() method in the base
        class, removing much of the functionality and use of the base class.
                
        :param ind: An individual to be evaluated.
        :param kwargs: Optional extra arguments.
        :return: The fitness of the evaluated individual.
        """
        
        from hypothesis_engine import hypothesis_params

        strategy = eval(ind.phenotype)

        nan_frac = np.count_nonzero(np.isnan(strategy))/np.size(strategy)
        if nan_frac >=0.4:
            print("Fraction of Missing Values in the strategy greater than 40%.")
            fitness = 0
        else:
            string = 'self.fitness_exp(strategy,hypothesis_params)'  

            fitness = eval(string)

            if fitness == np.inf or fitness == -np.inf:
                print("Invalid fitness value.")
                fitness = 0

#        print("{:<40}{:^5}{:<20}".format(ind.phenotype," :\t", f))
        prefix = str(round(fitness,3)) + "\t : "
        preferredWidth = 70
        wrapper = textwrap.TextWrapper(initial_indent=prefix, width=preferredWidth,
                                       subsequent_indent=' '*len(prefix))
        message = ind.phenotype

        print(wrapper.fill(message))
        return fitness
