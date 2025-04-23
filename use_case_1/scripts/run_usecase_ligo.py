import concurrent
import os
import subprocess
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool
from pathlib import Path
from immuneML.app.ImmuneMLApp import ImmuneMLApp
from immuneML.app.LigoApp import LigoApp

from immuneml_config_utils import write_immuneml_config


def run_command(cmd):
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    print(f"=== Starting: {cmd} ===")
    for line in process.stdout:
        print(f"[{cmd[:20]}...] {line.strip()}")  # Show a prefix of the command to distinguish
    process.wait()
    print(f"=== Finished: {cmd} ===\n")


def run_simulation(specification_path, result_path):
    app = LigoApp(specification_path=Path(specification_path), result_path=Path(result_path))
    app.run()


def prepare_immuneml_commands(antigen_datasets, configs_dir, output_dir, models):
    train_commands, filter_commands, report_commands, report_commands_2 = [], [], [], []
    train_template_file = f"{configs_dir}/templates/02_train_template.yaml"
    filter_template_file = f"{configs_dir}/templates/03_filter_template.yaml"
    exploratory_analysis_template_file = f"{configs_dir}/templates/04_exploratory_analysis_template_simulation.yaml"
    exploratory_analysis_template_file2 = f"{configs_dir}/templates/04_exploratory_analysis_template_simulation2.yaml"
    train_configs_dir = f"{configs_dir}/train_configs"
    filter_configs_dir = f"{configs_dir}/filter_configs"
    report_configs_dir = f"{configs_dir}/report_configs"

    for folder in [filter_configs_dir, report_configs_dir]:
        os.makedirs(folder, exist_ok=True)

    for antigen, dataset_sizes in antigen_datasets.items():
        for dataset_size in dataset_sizes:
            train_commands.extend(prepare_train_commands(antigen, dataset_size, train_template_file, train_configs_dir, output_dir, models))
            filter_commands.extend(prepare_filter_commands(antigen, dataset_size, filter_template_file, filter_configs_dir, output_dir, models))
            report_commands.extend(prepare_report_commands(antigen, dataset_size, exploratory_analysis_template_file, report_configs_dir, output_dir, models))
            report_commands_2.extend(prepare_report_commands_2(antigen, dataset_size, exploratory_analysis_template_file2, report_configs_dir, output_dir, models))

    return train_commands, filter_commands, report_commands, report_commands_2


def prepare_train_commands(antigen, dataset_size, train_template_file, train_configs_dir, output_dir, models):
    commands = []
    input_path = f"{output_dir}/00_simulation_output/dataset/simulated_dataset.tsv"
    gen_examples_count = int(dataset_size * 0.3)
    output_config_file = f"{train_configs_dir}/02_train_{antigen}_{dataset_size}.yaml"
    write_immuneml_config(train_template_file, input_path, output_config_file, gen_examples_count, models)
    commands.append(
        f"immune-ml {output_config_file} {output_dir}/02_train_output_multi/{antigen}/{antigen}_{dataset_size}/")
    return commands


def prepare_filter_commands(antigen, dataset_size, filter_template_file, filter_configs_dir, output_dir, models):
    commands = []
    for model in models:
        input_data_path = (f"{output_dir}/02_train_output_multi/{antigen}/{antigen}_{dataset_size}/{model}"
                           f"/exported_combined_dataset/combined_{model}_dataset.tsv")
        output_filter_config = f"{filter_configs_dir}/03_filter_{antigen}_{dataset_size}_{model}.yaml"
        write_immuneml_config(filter_template_file, input_data_path, output_filter_config)
        commands.append(
            f"immune-ml {output_filter_config} {output_dir}/03_filter_output/{antigen}"
            f"/{antigen}_{dataset_size}_{model}/")
    return commands


def prepare_report_commands(antigen, dataset_size, exploratory_analysis_template_file, report_configs_dir, output_dir, models):
    commands = []
    for model in models:
        report_input_data_path = (f"{output_dir}/03_filter_output/{antigen}/{antigen}_{dataset_size}_{model}"
                                  f"/data_export/dataset/AIRR/subset_dataset_filtered.tsv")
        output_report_config = (f"{report_configs_dir}"
                                f"/04_exploratory_analysis_{antigen}_{dataset_size}_{model}.yaml")
        write_immuneml_config(exploratory_analysis_template_file, report_input_data_path, output_report_config)
        commands.append(
            f"immune-ml {output_report_config} {output_dir}/04_reports_output/{antigen}"
            f"/{antigen}_{dataset_size}_{model}/")
    return commands


def prepare_report_commands_2(antigen, dataset_size, exploratory_analysis_template_file, report_configs_dir, output_dir, models):
    commands = []
    for model in models:
        report_input_data_path = (f"{output_dir}/02_train_output_multi/{antigen}/{antigen}_{dataset_size}/{model}"
                                  f"/exported_combined_dataset/combined_{model}_dataset.tsv")
        output_report_config = (f"{report_configs_dir}"
                                f"/04_exploratory_analysis_{antigen}_{dataset_size}_{model}_2.yaml")
        write_immuneml_config(exploratory_analysis_template_file, report_input_data_path, output_report_config)
        commands.append(
            f"immune-ml {output_report_config} {output_dir}/04_reports_output/{antigen}"
            f"/{antigen}_{dataset_size}_{model}_2/")
    return commands


def main():
    configs_path = "../configs"
    output_dir = "../results/simulated"
    simulation_datasets = {"simulation1": [3000]}
    models = ["PWM", "LSTM", "VAE"]

    train_commands, filter_commands, report_commands, report_commands_2 = prepare_immuneml_commands(simulation_datasets,
                                                                                 configs_dir=configs_path,
                                                                                 output_dir=output_dir,
                                                                                 models=models)
    # # simulate data
    # run_simulation(specification_path=f"{configs_path}/00_simulation.yaml",
    #                result_path=f"{output_dir}/00_simulation_output/")
    #
    # # run training
    # with concurrent.futures.ThreadPoolExecutor() as executor:
    #     executor.map(run_command, train_commands)
    #
    # # run filtering
    # with concurrent.futures.ThreadPoolExecutor() as executor:
    #     executor.map(run_command, filter_commands)

    # # run reports
    # with concurrent.futures.ThreadPoolExecutor() as executor:
    #     executor.map(run_command, report_commands)

    # run reports 2
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(run_command, report_commands_2)


if __name__ == "__main__":
    main()
