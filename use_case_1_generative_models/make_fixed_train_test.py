from pathlib import Path

import pandas as pd


def get_train_and_test_ids(input_data_path, output_path, training_percentage=0.7):
    input_data_df = pd.read_csv(input_data_path, sep="\t")

    if input_data_df["sequence_id"].isnull().all():
        input_data_df["sequence_id"] = range(1, len(input_data_df) + 1)

    train_ids, test_ids = [], []
    signals = [f"signal{i}" for i in range(1, 6)]
    for signal in signals:
        signal_df = input_data_df[input_data_df[signal] == 1]

        sequence_ids = signal_df["sequence_id"].tolist()
        split_idx = int(training_percentage * len(sequence_ids))
        train_ids.extend(sequence_ids[:split_idx])
        test_ids.extend(sequence_ids[split_idx:])

    Path(output_path).mkdir()

    train_ids = pd.DataFrame(train_ids, columns=["example_id"])
    test_ids = pd.DataFrame(test_ids, columns=["example_id"])
    train_ids.to_csv(Path(f"{output_path}/train_ids.csv"), index=False)
    test_ids.to_csv(Path(f"{output_path}/test_ids.csv"), index=False)

    input_data_df.to_csv(Path(f"{output_path}/full_simulated_dataset.tsv"), sep="\t", index=False)


if __name__ == "__main__":
    """
    This script ensures that there is the same number of sequences in train/test for each of the simulated signals. 
    Alternatively, the dataset could have been split
    randomly by setting "split_strategy: RANDOM" in setting "split_strategy: RANDOM" in 01_train.yaml. It would 
    produce very similar splits (although the exact number of sequences per signal would differ a little).
    """
    get_train_and_test_ids("00_simulation/dataset/exported_dataset/airr/simulated_dataset.tsv",
                           "00_simulation_with_train_test_split/")