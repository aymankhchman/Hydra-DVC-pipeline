import logging
from omegaconf import DictConfig, OmegaConf



def setup_logger(cfg: DictConfig) -> logging.Logger:
    logger = logging.getLogger(cfg.name)
    logger.setLevel(cfg.level)
    return logger