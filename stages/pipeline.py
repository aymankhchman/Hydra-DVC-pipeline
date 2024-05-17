import hydra
from omegaconf import DictConfig
from sklearn.pipeline import Pipeline
import os
import sys
sys.path.append(os.path.abspath('.'))
sys.path.append(os.path.abspath('..'))


def create_pipeline(config: DictConfig) -> Pipeline:

    steps = []
    for step in config["modelling"]:
        for step_name, estimator in config["modelling"][step].items():
            pipeline_step = (step_name, hydra.utils.instantiate(estimator, _convert_="partial", _recursive_=False))
            steps.append(pipeline_step)
    return Pipeline(steps)
