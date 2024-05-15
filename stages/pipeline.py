import hydra
from omegaconf import DictConfig
from sklearn.pipeline import Pipeline
import os
import sys
sys.path.append(os.path.abspath('.'))
sys.path.append(os.path.abspath('..'))


# @hydra.main(config_path="../config", config_name="config")
def create_pipeline(config: DictConfig) -> Pipeline:

    steps = []
    for step in config["modelling"]:
        for step_name, estimator in config["modelling"][step].items():
            pipeline_step = (step_name, hydra.utils.instantiate(estimator, _convert_="partial", _recursive_=False))
            steps.append(pipeline_step)
    return Pipeline(steps)


if __name__ == "__main__":

    create_pipeline()

    import pandas as pd
    df = pd.read_parquet("./dataset/2024/yellow_tripdata_2024_new_t.parquet")
    y = df["tip_amount"]

    # X_train_tr = check_pipeline.fit_transform(df)

