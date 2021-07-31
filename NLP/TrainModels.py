import subprocess
import sys
import random

# Fix RNG for reproducibility
RANDOM_SEED = "332021"
random.seed(RANDOM_SEED)

if __name__ == "__main__":
    training_set_sizes = [1000,5000,10000,25000,50000,100000,1000000]
    #TODO: Convert to a class and get config file value 
    for training_set_size in training_set_sizes:
        trainingDataSaveDir = "../Data/TrainingData/HumanMine/" + str(training_set_size) + "/"
        OpenNMTcmd = 'onmt_train -config '+ config + '-seed ' + str(RANDOM_SEED)'
        process = subprocess.Popen(OpenNMTcmd, shell=True, stderr=subprocess.STDOUT)
        process.wait()
