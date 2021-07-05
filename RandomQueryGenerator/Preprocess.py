import string
import networkx as nx

import matplotlib.pyplot as plt
import pickle
import subprocess
import os
FNULL = open(os.devnull, 'w')

from GenerateRandomQueries import GenerateRandomQueries
from Utils import alternateEnglishOrdering
from Config import genconfig

nrNodesList = list()


def gen_dataset(dataset_schema,trainingDataDir,training_set_size):
    RandomQueries = GenerateRandomQueries(schemaObjectPath=dataset_schema) 
    #training_set_sizes = [1000,5000,10000,25000,50000,100000,1000000]
    query_complexity_limits = [5,5,2]
    
    print("* Beginning generation of training data for size: " + str(training_set_size))
    number_of_runs = training_instances_cap = training_set_size

    #    Generate training data (standard train, val, test split)
    trainingDataSaveDir = trainingDataDir + "/" + str(number_of_runs) + "/" ##TODO: get a dataset from the args line and read the corresponding dir from config
    generation_runs = RandomQueries.generateQuery(training_data_save_dir = trainingDataSaveDir,
                                                                    graphTraversalProbability=0.5, 
                                                                    attributeChoiceProbability=0.1, 
                                                                    constraintChoiceProbability=0.1, 
                                                                    cut_probability=0.0,
                                                                    generate_training_data=True,
                                                                    link_classes_with_attributes=False,
                                                                    random_node_start=True,
                                                                    show_graph=False,                                                                    
                                                                    runs=number_of_runs,
                                                                    training_instances_cap=training_instances_cap,
                                                                    complexity_cap=query_complexity_limits,
                                                                    uniform_spread=True)

def build_vocab(trainingDataSaveDir,training_set_size):
        config_file=genconfig.gen_preprocess_config(trainingDataSaveDir=trainingDataSaveDir, train_set_size=training_set_size )
        OpenNMTcmd = 'onmt_build_vocab -config ' + str(config_file) 
        process = subprocess.Popen(OpenNMTcmd, shell=True, stdout=FNULL, stderr=subprocess.STDOUT)
        process.wait()

        # Use FastText embeddings
        fasttext_embedding_size = 300
        cmd = 'python3 embeddings_to_torch.py -emb_file_both "../NLP/fasttext_dir/wiki-news-' + str(fasttext_embedding_size) + 'd-1M.vec" -dict_file ' + str(trainingDataSaveDir) + 'dataset.vocab.pt -output_file "' + str(trainingDataSaveDir) + 'embeddings"'
        ##TODO: Add embeddings command options also to the config 
        process = subprocess.Popen(cmd, shell=True, stdout=FNULL, stderr=subprocess.STDOUT)
        process.wait()
