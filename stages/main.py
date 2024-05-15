import hydra
import os
import sys
from omegaconf import DictConfig, OmegaConf
from pathlib import Path

from pipeline import create_pipeline
from sklearn.pipeline import Pipeline
import pandas as pd
from pathlib import Path

sys.path.append(os.path.abspath('.'))
from utils.basic_logger import setup_logger

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

import warnings
import joblib
from datetime import datetime

warnings.filterwarnings("ignore")

@hydra.main(config_path="../config", config_name="config")
def main(config: DictConfig):
  
  logger = setup_logger(config["base"]["logging"])

  logger.info("creating pipeline")
  pipeline = create_pipeline(config)

  # reading dataset
  logger.info("reading dataset")
  dataset_folder = Path(config["dataset"]["output_save"])
  dataset_path  = config["base"]["project"]["path"] / dataset_folder / config["dataset"]["output_name"]
  df  = pd.read_parquet(dataset_path)
  
  logger.info("splitting X and y")
  X = df.drop(config["dataset"]["target_variable"], axis=1)
  y = df[config["dataset"]["target_variable"]]
  
  logger.info("Creating train data and test")
  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=129, shuffle=True)


  logger.info(f"fitting the model")
  pipeline.fit(X_train, y_train)

  logger.info("computing predictions")
  predictions = pipeline.predict(X_test)
  print(mean_squared_error(y_test, predictions), r2_score(y_test, predictions))

  pipeline_folder = Path(config["base"]["project"]["pipeline_folder"])
  pipeline_folder.mkdir(exist_ok=True)

  logger.info(f"dumping pipeline :{pipeline_folder / config["base"]["project"]["pipeline_name"]}")
  joblib.dump(pipeline , pipeline_folder / config["base"]["project"]["pipeline_name"])



if __name__ == "__main__":
    main()