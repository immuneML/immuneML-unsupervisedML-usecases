import os
import pandas as pd
import argparse


def preprocess_vdjdb_data(file_path, output_dir, epitope=None):
    filename = file_path.split("/")[-1]
    df = pd.read_csv(file_path, sep="\t")
    df = df.dropna(subset=["V", "J"])
    df = df[df['Gene'] == 'TRB']
    if epitope:
        df = df[df["Epitope"].str.match(epitope)]
    df.to_csv(f"{output_dir}/{filename}", sep="\t", index=False)


def main():
    data_files = "../data/vdjdb_raw"
    output_dir = "../data/vdjdb_clean"
    os.makedirs(output_dir, exist_ok=True)

    for data_file in os.listdir(data_files):
        antigen = data_file.split(".")[0].split("_")[-1]
        file_path = os.path.join(data_files, data_file)

        if antigen == "CMV":
            epitope = "KLGGALQAK"
        elif antigen == "influenzaA":
            epitope = "GILGFVFTL"
        else:
            print(f"Not filtering for epitope for {antigen}")
            epitope = None

        preprocess_vdjdb_data(file_path, output_dir, epitope=epitope)


if __name__ == "__main__":
    main()
