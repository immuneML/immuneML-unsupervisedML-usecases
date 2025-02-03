import pandas as pd
import argparse


def preprocess_iedb_data(filename, epitope):
    df = pd.read_csv(filename, sep="\t")
    df_filtered = df.dropna(subset=["Chain 2 - CDR3 Curated"])
    df_filtered = df_filtered[df_filtered["Epitope - Name"].str.match(epitope)]
    df_filtered = df_filtered[df_filtered["Chain 2 - CDR3 Curated"].str.match("^CA.*F$")]

    df_filtered = df_filtered.drop_duplicates(subset=["Chain 2 - CDR3 Curated", "Chain 2 - Curated V Gene",
                                                      "Chain 2 - Curated J Gene"])

    df_filtered.to_csv(filename.replace(".tsv", "_filtered.tsv"), sep="\t", index=False)


def main():
    parser = argparse.ArgumentParser(description='Preprocess tsv file exported from IEDB.')
    parser.add_argument('--iedb_file', type=str, default="dataset1/IEDB_export_GILGFVFTL_human_TCR.tsv",
                        help='Path to the iedb data file.')
    parser.add_argument('--epitope', type=str, default="GILGFVFTL", help='Epitope amino acid sequence.')

    args = parser.parse_args()

    preprocess_iedb_data(args.iedb_file, args.epitope)


if __name__ == "__main__":
    main()
