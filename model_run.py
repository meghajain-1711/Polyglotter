from sys import argv
from torch import cuda
from onmt.utils.logging import init_logger
from onmt.utils.misc import set_random_seed

from Config import defaults, genconfig
import RandomQueryGenerator
from NLP import TrainModels, CalculateStatistics
import Preprocess


def main(dataset = "HUMANMINE", datasetDir):    
    init_logger()
    is_cuda = cuda.is_available()
    set_random_seed(1111, is_cuda)

    #Preprocess step 
    if datasetDir == None:
        training_set_sizes = [1000,5000,10000,25000,50000,100000,1000000]
        for training_set_size in training_set_sizes:
            Preprocess.gen_dataset(dataset_schema,trainingDataDir,training_set_size)
            Preprocess.build_vocab(trainingDataSaveDir,training_set_size)
    
    ##TODO : Add step for datasetDir given through arg

    ##TODO : Add training step 
    
    ##TODO : Add Evaluation step
    #Add Evaluation step Calculate Stats
    CalculateStatistics
    
    return 0


if __name__ == '__main__':  
    print(f"Name of the script      : {argv[0]}")
    print(f"Arguments of the script : {argv[1:]}")

    params = genconfig.gen_defaults_config(argv[1:])
    exit_code = main(**params)