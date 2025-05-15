import concurrent
import os
import subprocess
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool
from pathlib import Path
from immuneML.app.ImmuneMLApp import ImmuneMLApp
from immuneml_config_utils import write_immuneml_config


def run_command(cmd):
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    print(f"=== Starting: {cmd} ===")
    for line in process.stdout:
        print(f"[{cmd[:20]}...] {line.strip()}")  # Show a prefix of the command to distinguish
    process.wait()
    print(f"=== Finished: {cmd} ===\n")


def run_immuneml_app(specification_path, result_path):
    app = ImmuneMLApp(specification_path=Path(specification_path),
                      result_path=Path(result_path))
    app.run()


def prepare_immuneml_commands(antigen_datasets, configs_dir, output_dir, models):
    train_commands, filter_commands, report_commands = [], [], []
    train_template_file = f"{configs_dir}/templates/02_train_template.yaml"
    filter_template_file = f"{configs_dir}/templates/03_filter_template.yaml"
    exploratory_analysis_template_file = f"{configs_dir}/templates/04_exploratory_analysis_template.yaml"
    train_configs_dir = f"{configs_dir}/train_configs"
    filter_configs_dir = f"{configs_dir}/filter_configs"
    report_configs_dir = f"{configs_dir}/report_configs"

    for folder in [filter_configs_dir, report_configs_dir]:
        os.makedirs(folder, exist_ok=True)

    for antigen in antigen_datasets.keys():
        for i, dataset_size in enumerate(antigen_datasets[antigen]):
            input_path = (f"{output_dir}/01_subsample_output/{antigen}/{antigen}_{dataset_size}_subsampled_{i + 1}"
                          f"/subset_{antigen}_subsampled.tsv")
            gen_examples_count = int(dataset_size * 0.3)
            output_config_file = f"{train_configs_dir}/02_train_{antigen}_{dataset_size}.yaml"
            write_immuneml_config(train_template_file, input_path, output_config_file, gen_examples_count)
            train_commands.append(
                f"immune-ml {output_config_file} {output_dir}/02_train_output_multi/{antigen}/{antigen}_{dataset_size}/")

            for model in models:
                input_data_path = (f"{output_dir}/02_train_output_multi/{antigen}/{antigen}_{dataset_size}/{model}"
                                   f"/exported_combined_dataset/combined_{model}_dataset.tsv")

                output_filter_config = f"{filter_configs_dir}/03_filter_{antigen}_{dataset_size}_{model}.yaml"
                write_immuneml_config(filter_template_file, input_data_path, output_filter_config)
                filter_commands.append(
                    f"immune-ml {output_filter_config} {output_dir}/03_filter_output/{antigen}"
                    f"/{antigen}_{dataset_size}_{model}/")

                report_input_data_path = (f"{output_dir}/03_filter_output/{antigen}/{antigen}_{dataset_size}_{model}"
                                          f"/data_export/dataset/AIRR/subset_dataset_filtered.tsv")
                output_report_config = (f"{report_configs_dir}"
                                        f"/04_exploratory_analysis_{antigen}_{dataset_size}_{model}.yaml")
                write_immuneml_config(exploratory_analysis_template_file, report_input_data_path, output_report_config)
                report_commands.append(
                    f"immune-ml {output_report_config} {output_dir}/04_reports_output/{antigen}"
                    f"/{antigen}_{dataset_size}_{model}/")

    return train_commands, filter_commands, report_commands


def main():
    # preprocess data
    run_immuneml_app(specification_path="../configs/templates/00_preprocess.yaml",
                     result_path="../results/experimental/00_preprocessing_output/")

    # subsample data
    run_immuneml_app(specification_path="../configs/templates/01_subsample.yaml",
                     result_path="../results/experimental/01_subsample_output/")

    # antigen_datasets = {"CMV": [10000, 5000, 1000], "HIV1": [2500, 1000, 500], "influenzaA": [4500, 2000, 500]}
    antigen_datasets = {"influenzaA": [4500, 2000, 500]}
    train_commands, filter_commands, report_commands = prepare_immuneml_commands(antigen_datasets,
                                                                                 configs_dir="../configs",
                                                                                 output_dir="../results/experimental",
                                                                                 models=["PWM", "LSTM", "VAE"])

    # run training
    # with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
    #     executor.map(run_command, train_commands)
    #
    # # run filtering
    # with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    #     executor.map(run_command, filter_commands)

    # run reports
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        executor.map(run_command, report_commands)


if __name__ == "__main__":
    main()
