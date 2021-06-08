Evaluate the version changes :
    Version changes in preprocessing end mostly. 

OpenNMT commandlines in the existing system : 
    1. Training :
    OpenNMTcmd = 'onmt_train -data ' + str(trainingDataSaveDir) \
        + 'dataset -save_model ./Models/model-HumanMine-' + str(training_set_size) \
        + ' --layers ' + str(NUM_LAYERS) + ' -heads ' + str(NUM_HEADS) + ' -rnn_size ' + str(RNN_SIZE) + ' -word_vec_size ' + str(WORD_VEC_SIZE) + ' -transformer_ff ' + str(TRANSFORMER_FF) + ' -max_generator_batches 2 -seed ' + str(RANDOM_SEED) + ' -batch_size ' + str(BATCH_SIZE) + ' -valid_batch_size ' + str(VALID_BATCH_SIZE) + ' -accum_count ' + str(ACCUM_COUNT) + ' -optim adam -adam_beta2 0.998 -encoder_type transformer -max_grad_norm 0 -decoder_type transformer -position_encoding -param_init_glorot -param_init 0 -batch_type tokens -decay_method noam -learning_rate ' + str(LEARNING_RATE) + ' -normalization tokens -train_steps ' \
        + str(TRAIN_EPOCHS) + ' -pre_word_vecs_enc ' + str(trainingDataSaveDir) + 'embeddings.enc.pt -pre_word_vecs_dec ' + str(trainingDataSaveDir) + 'embeddings.dec.pt -valid_steps 100 -save_checkpoint_steps 500 -report_every 50 -dropout ' + str(DROPOUT_RATE) + ' -attention_dropout ' + str(ATTENTION_DROPOUT_RATE) + ' -label_smoothing ' + str(LABEL_SMOOTHING) + ''
        

    2. Translation : 
    'onmt_translate -batch_size 256 -beam_size ' + str(beam_size) +  ' -model ' + self.modelsDir + 'model-' + self.model + '_step_' + str(modelCheckpoint) + '.pt -src ' + tempFile + ' -output ' + self.translationsOutputDir + 'translation.out -replace_unk -n_best ' + str(n_best)


    3. PreProcessing : [ Query Generation in 3 places , need to edit each and test]
    OpenNMTcmd = 'onmt_preprocess -train_src ' + str(trainingDataSaveDir) + 'src-dataset-' + str(training_set_size) + '-train.txt -train_tgt ' + str(trainingDataSaveDir) + 'tgt-dataset-' + str(training_set_size) + '-train.txt -valid_src ' + str(trainingDataSaveDir) + 'src-dataset-' + str(training_set_size) + '-val.txt -valid_tgt ' + str(trainingDataSaveDir) + 'tgt-dataset-' + str(training_set_size) + '-val.txt -save_data ' + str(trainingDataSaveDir) + 'dataset -num_threads 20 -dynamic_dict -share_vocab -overwrite'


New features relevant to our system : 
1. #TO CHECK with Adrian : Basically entire preprocessing module has changed to build_vocab. So the entire system for the generation part needs to be re-written. 


Lib dependencies : 
Setup of onmt2.0 in my system ->
torch version incompatible. [ Working on seeing if any other library breaks in the current system with torch update ] #In progress
Pandas needs to be installed separately for train_test_split.
Read csv from the text file : header should be set to None, line terminator ( different values for Linux/Windows systems , sep not comma but tab)
Subprocess.PIPE will hang indefinitely if stdout is more than 65000 characters. So removed the same
subprocess.communicate() preferred over subprocess.wait() for the same reason
Train command is facing numpy version issues : https://github.com/pytorch/pytorch/issues/37377 . Fix is : remove os.environ['MKL_THREADING_LAYER'] = 'GNU' or os.environ['MKL_SERVICE_FORCE_INTEL'] = '1' and just have numpy 1.20.


Commandline arguments of each onmt command : 
1. Query Generation : 
ONMT1 : train_Src [ To provide training src dataset path], 
        train_tgt [ To provide training tgt datatset path], 
        valid_src [ To provide validation src datatset path]
        valid_tgt [ To provide validation target dataset path]
        save_data [ Workspace to save the processed data ]
        num_threads [ Parallel processing ]
        dynamic_dict [ ]
        share_vocab [ ]
        overwrite [ ]

ONMT 2 : 


2. Translation : 
ONMT1 : batch_size 
        beam_size  
        model 
        src [ FILE CONTAINING I/P SENTENCES]
        output 
        replace_unk 
        n_best

onmt 2 : NO CHANGE TO COMMANDLINE ARGUMENTS #Trial done with openNMT App

3. TRAINING :
ONMT1 : data 
        save_model [ Workspace for saving the trained model]
        layers [ Number of layers in enc/dec]
        heads [ Number of heads for transformer self-attention ]
        rnn_size [ Size of rnn hidden states. ]
        word_vec_size [ Word embedding size for src and tgt ]
        transformer_ff [ Size of hidden transformer feed-forward ]
        max_generator_batches [ Maximum batches of words in a sequence to run the generator on in parallel. Higher is faster, but uses more memory. Set to 0 to disable. ]
        seed [ Set random seed used for better reproducibility between experiments. ]
        batch_size [ Maximum batch size for training , useful for optimization ]
        valid_batch_size [ Maximum batch size for validation ]
        accum_count [ Accumulate gradient this many times. Approximately equivalent to updating batch_size * accum_count batches at once. Recommended for Transformer. ]
        optim [ Optimization method. In our case adam]
        encoder_type [ Type of encoder layer to use ]
        max_grad_norm [ If the norm of the gradient vector exceeds this, renormalize it to have the norm equal to max_grad_norm ]
        decoder_type [ Type of decoder layer]
        position_encoding 
        param_init_glorot 
        param_init 
        batch_type tokens 
        decay_method noam 
        learning_rate ' + str(LEARNING_RATE) + ' 
        normalization tokens 
        train_steps 
        pre_word_vecs_enc 
        pre_word_vecs_dec 
        valid_steps 100 
        save_checkpoint_steps 500 
        report_every 50 
        dropout 
        attention_dropout 
        label_smoothing 

ONMT 2: Pass a config file with most details , and commandline should just have save_model workspace. 


