from pathlib import Path

from immuneML.app.LigoApp import LigoApp
from immuneML.app.ImmuneMLApp import ImmuneMLApp
from run_use_case import get_train_and_test_ids


def run_simulation(specification_path, result_path):
    app = LigoApp(specification_path=Path(specification_path), result_path=Path(result_path))
    app.run()


def run_immuneML(specification_path, result_path):
    app = ImmuneMLApp(specification_path=Path(specification_path), result_path=Path(result_path))
    app.run()


def main():
    configs_dir = "generative_air_benchmark/configs/dummy_configs"
    output_dir = "generative_air_benchmark/dummy_results"

    # simulate data
    run_simulation(specification_path=f"{configs_dir}/00_simulation.yaml",
                   result_path=f"{output_dir}/00_simulation/")

    # get train and test ids
    get_train_and_test_ids(input_data_path=f"{output_dir}/00_simulation/dataset/simulated_dataset.tsv",
                           output_path=f"{output_dir}/00_simulation/")

    # run training
    run_immuneML(specification_path=f"{configs_dir}/01_train.yaml",
                 result_path=f"{output_dir}/01_train/")

    # # run filtering
    # run_immuneML(specification_path=f"{configs_dir}/02_filter.yaml",
    #              result_path=f"{output_dir}/02_filter/")
    #
    # # run feature comparison reports
    # run_immuneML(specification_path=f"{configs_dir}/03_exploratory_analysis_feature_comparison.yaml",
    #              result_path=f"{output_dir}/03_feature_comparison/")
    #
    # run feature value bar plot reports
    run_immuneML(specification_path=f"{configs_dir}/04_exploratory_analyses.yaml",
                 result_path=f"{output_dir}/04_exploratory_analyses/")


if __name__ == "__main__":
    main()
