datasets = ["HUMANMINE", "Neo4j", "MySQL"]
dataschemas = list(map(lambda ds_name: "Data/Schemas/" + ds_name +"dbSchema.obj" , datasets))


# Default config options for build vocab
vocabulary = {
    "data_type": "text",
    "share_vocab": True,
    "vocab_size_multiple": 1,
    "src_vocab_size": 30000,
    "tgt_vocab_size": 30000,
    "src_words_min_frequency": 1,
    "tgt_words_min_frequency": 1
}

# Default config options for Training
dropout = 0.1
training = {
    "train_steps": 100000,
    "valid_steps": 4000,
    "save_checkpoint_steps": 4000
}

# Default config options for Translation




def configurations(name, path, value):
    if len(path) == 1: 
        primary = path[0]
    elif len(path) == 2: 
        primary, secondary = path
    elif len(path) > 2:
        raise KeyError('Such deep nesting is not supported')
    elif name == "vocabulary": 
        global vocabulary
        if len(path) == 1: 
            vocabulary[primary] = type(vocabulary[primary])(value)
        elif len(path) == 2: 
            vocabulary[primary][secondary] = type(vocabulary[primary][secondary])(value)
    elif name == "dropout": 
        global dropout
        dropout = type(dropout)(value)
    elif name == "training": 
        global training
        if len(path) == 1: 
            training[primary] = type(training[primary])(value)
        elif len(path) == 2: 
            training[primary][secondary] = type(training[primary][secondary])(value)