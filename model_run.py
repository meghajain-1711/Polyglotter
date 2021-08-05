from sys import argv
import argparse
from torch import cuda
from onmt.utils.logging import init_logger
from onmt.utils.misc import set_random_seed

from Config import defaults, genconfig
from NLP import RandomQueryGenerator
from NLP import TrainModels, CalculateStatistics
from RandomQueryGenerator import Preprocess

import yaml
from cerberus import Validator

def load_doc(conf_file):
    with open(conf_file,'r') as stream:
        try:
            return yaml.load(stream)
        except yaml.YAMLError as exception:
            raise exception

def validate_config_file(schema,conf_file):
    schem=eval(open(schema,'r').read())
    v=Validator(schem)
    doc=load_doc(conf_file)
    print(v.validate(doc,schem))
    print(v.errors)

def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        help="specify config_file which will be used for your model generation", action='store',dest='config_file'
    )
    parser.add_argument(
        "--embeddings",
        help="specify embedding_file which will be used for your model generation", action='store',dest='cembeddings'
    )
    args,remaining = parser.parse_known_args(argv)
    return args,remaining


def main(dataset = "HUMANMINE", datasetDir, config_file):    
    init_logger()
    is_cuda = cuda.is_available()
    set_random_seed(1111, is_cuda)

    config_file=genconfig.gen_preprocess_config(trainingDataSaveDir=trainingDataSaveDir, train_set_size=training_set_size )

    #Preprocess step 
    if datasetDir == None and dataset in defaults.configurations(dataset,1): 
        training_set_sizes = defaults.configurations(training_set_sizes,1)
        for training_set_size in training_set_sizes:
            dataset_schema=defaults.configurations(dataset_schema(dataset),2)
            trainingDataDir=defaults.configurations(trainingdir(dataset),2)
            Preprocess.gen_dataset(dataset_schema,trainingDataDir,training_set_size)
            Preprocess.build_vocab(trainingDataDir,training_set_size)
            ##TODO : Add training step here  
    
    ##TODO : Add Evaluation step on the model
    #Add Evaluation step Calculate Stats
    CalculateStatistics
    


if __name__ == '__main__':  
    args,gen_config_args=parse_args(argv[1:])
    if args.config_file ==None:    
        params = genconfig.gen_defaults_config(gen_config_args)
    
    #TO DO: Add format checking of the config file here
    if args.config_file is not None:
        v=validate_config_file(conf_schema,args.config_file)
        if v==0:
            sys.exit("Your config file is of wrong format, check the correct format from the README")
    ##TO DO : call the main pipeline here
    