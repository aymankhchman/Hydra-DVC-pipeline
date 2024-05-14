import hydra
from omegaconf import DictConfig
from sklearn.pipeline import Pipeline


@hydra.main(config_path="config", config_name="config")
def create_pipeline(steps_configs: DictConfig) -> Pipeline:
    steps = []

    for step_config in steps_configs:
        step_name, step_params = step_config.items()[0]

        pipeline_step = (step_name, hydra.utils.instantiate(step_params))
        steps.append(pipeline_step)

    return Pipeline(steps)


if __name__ == "__main__":
    

    check_pipeline = create_pipeline()