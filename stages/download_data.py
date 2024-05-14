import hydra
import os
import sys
from omegaconf import DictConfig, OmegaConf
from pathlib import Path

sys.path.append(os.path.abspath('.'))
from utils.basic_logger import setup_logger


@hydra.main(config_path="../config", config_name="config")
def download_file(cfg: DictConfig):
    
    logger = setup_logger(cfg.base.logging)
    project_path = Path(cfg.base.project.path)

    data_folder = project_path / cfg.dataset.output_save
    
    data_folder.mkdir(exist_ok=True, parents=True)
    logger.info(f"{data_folder / cfg.dataset.output_name}")
    os.system(f"curl {cfg.dataset.url_path} -o '{data_folder / cfg.dataset.output_name}'")


    logger.info(f"{cfg.dataset.output_name}")

if __name__ == "__main__":
    download_file()