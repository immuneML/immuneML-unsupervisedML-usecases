from pathlib import Path

import pandas as pd
from immuneML.app.LigoApp import LigoApp
from immuneML.app.ImmuneMLApp import ImmuneMLApp


def run_simulation(specification_path, result_path):
    app = LigoApp(specification_path=Path(specification_path), result_path=Path(result_path))
    app.run()


def run_immuneML(specification_path, result_path):
    app = ImmuneMLApp(specification_path=Path(specification_path), result_path=Path(result_path))
    app.run()

def get_train_and_test_ids(input_data_path, output_path):
    input_data_df = pd.read_csv(input_data_path, sep="\t")

    if input_data_df["sequence_id"].isnull().all():
        input_data_df["sequence_id"] = range(1, len(input_data_df) + 1)

    train_ids, test_ids = [], []
    signals = [f"signal{i}" for i in range(1, 6)]
    for signal in signals:
        signal_df = input_data_df[input_data_df[signal] == 1]

        sequence_ids = signal_df["sequence_id"].tolist()
        split_idx = int(0.7 * len(sequence_ids))
        train_ids.extend(sequence_ids[:split_idx])
        test_ids.extend(sequence_ids[split_idx:])

    train_ids = pd.DataFrame(train_ids, columns=["example_id"])
    test_ids = pd.DataFrame(test_ids, columns=["example_id"])
    train_ids.to_csv(Path(f"{output_path}/train_ids.csv"), index=False)
    test_ids.to_csv(Path(f"{output_path}/test_ids.csv"), index=False)

    input_data_df.to_csv(Path(f"{output_path}/full_simulated_dataset.tsv"), sep="\t", index=False)


def main():
    configs_dir = "generative_air_benchmark/configs"
    output_dir = "generative_air_benchmark/results"

    # # simulate data
    # run_simulation(specification_path=f"{configs_dir}/00_simulation.yaml",
    #                result_path=f"{output_dir}/00_simulation/")

    # run training
    run_immuneML(specification_path=f"{configs_dir}/01_train.yaml",
                 result_path=f"{output_dir}/01_train/")
    #
    # # run filtering
    # run_immuneML(specification_path=f"{configs_dir}/02_filter.yaml",
    #              result_path=f"{output_dir}/02_filter/")
    #
    # # run feature comparison reports
    # run_immuneML(specification_path=f"{configs_dir}/03_exploratory_analysis_feature_comparison.yaml",
    #              result_path=f"{output_dir}/03_feature_comparison/")
    #
    # # run feature value bar plot reports
    # run_immuneML(specification_path=f"{configs_dir}/04_exploratory_analysis_feature_barplot.yaml",
    #              result_path=f"{output_dir}/04_feature_value_barplot/")


if __name__ == "__main__":
    main()
