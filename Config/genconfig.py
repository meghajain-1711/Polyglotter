import yaml
from os import path
from typing import List
from config import defaults

yamlconf = lambda ds: f"""## Where the samples will be written
    # config.yaml
    ## Where the samples will be written
    save_data: ../Data/TrainingData/{ds.name}
    ## Where the vocab(s) will be written
    src_vocab: ../Data/TrainingData/{ds.name}/src_vocab
    tgt_vocab: ../Data/TrainingData/{ds.name}/tgt_vocab
    ## Where the model will be saved
    save_model: ../NLP/Models
    num_threads: {ds.vocab.num_threads}
    overwrite: {ds.vocab.overwrite}
    share_vocab: {ds.vocab.share_vocab}
    dynamic_dict: {ds.vocab.dynamic_dict}
    # Corpus opts:
    data:
        corpus_1:
            path_src: ../Data/train_src.txt
            path_tgt: ../Data/train_tgt.txt
        valid:
            path_src: ../Data/val_src.txt
            path_tgt: ../Data/val_src.txt
    # Remove or modify these lines for bigger files
    train_steps: 10000
    valid_steps: 2000
    path_src: {ds.train.source}
        path_tgt: {ds.train.target}
        transforms: [filtertoolong]
    valid:
        path_src: {ds.val.source}
        path_tgt: {ds.val.target}
#### Filter
src_seq_length: 300
tgt_seq_length: 300
# Train on a single GPU
# world_size: 1
# gpu_ranks: [0]
"""


def gen_yaml_config(ds):
    ds.vocab = DataItem(
        f"{path.join(ds.path, 'run', ds.name)}.vocab.src",
        f"{path.join(ds.path, 'run', ds.name)}.vocab.tgt"
    )

    conf = yamlconf(ds)
    options = yaml.safe_load(conf)
    with open(f"{path.join(ds.path, 'config.yaml')}", "w") as f:
        f.write(conf)      

    return options

def gen_defaults_config(argv: List[str]):
    params = dict()
    known_params = [
        "model",
        "dataset"
    ]

    known_configs = [
        "vocabulary", 
        "training", 
        "transformer" 
    ]

    for arg in argv:
        name, value = arg.split("=", 1)

        # extract known params
        if name in known_params:
            params[name] = value
            continue
        
        # set config defaults
        chain = name.split("-")
        ikey = chain.pop(0)
        if ikey in known_configs:            
            defaults.configurations(ikey, chain, value)
            continue

    return params