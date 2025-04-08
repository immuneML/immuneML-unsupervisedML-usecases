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


if __name__ == "__main__":
    # # run preprocessing
    # app = ImmuneMLApp(specification_path=Path("../configs/templates/00_preprocess.yaml"),
    #                   result_path=Path("../results/00_preprocessing_output/"))
    # app.run()
    #
    # # subsample data
    # app = ImmuneMLApp(specification_path=Path("../configs/templates/01_subsample.yaml"),
    #                   result_path=Path("../results/01_subsample_output/"))
    # app.run()

    # run training
    # immuneml_train_commands = []
    # train_template_file = "../configs/templates/02_train_template.yaml"
    # train_configs_dir = "../configs/train_configs"
    # os.makedirs(train_configs_dir, exist_ok=True)

    #antigen_datasets = {"CMV": [10000, 5000, 1000], "HIV1": [2500, 1000, 500], "influenzaA": [4500, 2000, 500]}
    #antigen_datasets = {"CMV": [5000, 1000], "HIV1": [2500, 1000, 500], "influenzaA": [4500, 2000, 500]}
    antigen_datasets = {"CMV": [10000, 5000, 1000]}
    # for antigen in antigen_datasets.keys():
    #     for i, dataset_size in enumerate(antigen_datasets[antigen]):
    #         input_path = f"../results/01_subsample_output/{antigen}/{antigen}_{dataset_size}_subsampled_{i + 1}/subset_{antigen}_subsampled.tsv"
    #         gen_examples_count = int(dataset_size * 0.3)
    #         output_config_file = f"{train_configs_dir}/02_train_{antigen}_{dataset_size}.yaml"
    #         write_immuneml_config(train_template_file, input_path, output_config_file, gen_examples_count)
    #         immuneml_train_commands.append(
    #             f"immune-ml {output_config_file} ../results/02_train_output_multi/{antigen}/{antigen}_{dataset_size}/")
    #
    # with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
    #     executor.map(run_command, immuneml_train_commands)

    # run reports
    immuneml_filter_commands, immuneml_report_commands = [], []
    filter_template_file = "../configs/templates/03_filter_template.yaml"
    exploratory_analysis_template_file = "../configs/templates/04_exploratory_analysis_template.yaml"
    filter_configs_dir = "../configs/filter_configs"
    report_configs_dir = "../configs/report_configs"
    for directory in [filter_configs_dir, report_configs_dir]:
        os.makedirs(directory, exist_ok=True)

    for antigen in antigen_datasets.keys():
        for i, dataset_size in enumerate(antigen_datasets[antigen]):
            for model in ["PWM", "LSTM", "VAE"]:
                input_data_path = f"../results/02_train_output_multi/{antigen}/{antigen}_{dataset_size}/{model}/exported_combined_dataset/combined_{model}_dataset.tsv"

                output_filter_config = f"{filter_configs_dir}/03_filter_{antigen}_{dataset_size}_{model}.yaml"
                write_immuneml_config(filter_template_file, input_data_path, output_filter_config)
                immuneml_filter_commands.append(f"immune-ml {output_filter_config} ../results/03_filter_output/{antigen}/{antigen}_{dataset_size}_{model}/")

                report_input_data_path = f"../results/03_filter_output/{antigen}/{antigen}_{dataset_size}_{model}/data_export/dataset/AIRR/subset_dataset_filtered.tsv"
                output_report_config = f"{report_configs_dir}/04_exploratory_analysis_{antigen}_{dataset_size}_{model}.yaml"
                write_immuneml_config(exploratory_analysis_template_file, report_input_data_path, output_report_config)
                immuneml_report_commands.append(
                    f"immune-ml {output_report_config} ../results/04_reports_output/{antigen}/{antigen}_{dataset_size}_{model}/")

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        executor.map(run_command, immuneml_filter_commands)

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        executor.map(run_command, immuneml_report_commands)
