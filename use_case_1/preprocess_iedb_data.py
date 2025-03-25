import pandas as pd
import argparse


def preprocess_iedb_data(filename, epitope):
    df = pd.read_csv(filename, sep="\t")
    df_filtered = df.dropna(subset=["Chain 2 - CDR3 Curated"])
    df_filtered = df_filtered[df_filtered["Epitope - Name"].str.match(epitope)]
    df_filtered = df_filtered[df_filtered["Chain 2 - CDR3 Curated"].str.match("^CA.*F$")]

    # filter out rows with missing v and j genes
    df_filtered = df_filtered.dropna(subset=["Chain 2 - Curated V Gene", "Chain 2 - Curated J Gene"])

    # TODO: should split after preprocessing with immuneML
    # for num_sequences in [300, 500, 1000]:
    #     df_train = df_filtered.sample(n=num_sequences, random_state=1)
    #     df_train.to_csv(filename.replace(".tsv", f"_train_{num_sequences}.tsv"), sep="\t", index=False)
    #
    #     df_test = df_filtered[~df_filtered.index.isin(df_train.index)]
    #     df_test.to_csv(filename.replace(".tsv", f"_test_{len(df_test)}.tsv"), sep="\t", index=False)

    df_filtered.to_csv(filename.replace(".tsv", "_filtered.tsv"), sep="\t", index=False)


def main():
    parser = argparse.ArgumentParser(description='Preprocess tsv file exported from IEDB.')
    parser.add_argument('--iedb_file', type=str, default="dataset1/IEDB_export_GILGFVFTL_human_TCR.tsv",
                        help='Path to the iedb data file.')
    parser.add_argument('--epitope', type=str, default="GILGFVFTL", help='Epitope amino acid sequence.')

    args = parser.parse_args()

    preprocess_iedb_data(args.iedb_file, args.epitope)

    GLC_iedb_file = "dataset2/IEDB_export_GLCTLVAML_human_TCR.tsv"
    preprocess_iedb_data(GLC_iedb_file, "GLCTLVAML")

    AVF_iedb_file = "dataset3/IEDB_export_AVFDRKSDAK_human_TCR.tsv"
    preprocess_iedb_data(AVF_iedb_file, "AVFDRKSDAK")


if __name__ == "__main__":
    main()
