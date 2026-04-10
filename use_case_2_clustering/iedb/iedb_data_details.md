## Construction of the IEDB TCRβ dataset

To construct the IEDB TCRβ dataset, the following filters were applied: We selected all human TCRβ chain sequences 
with a cognate peptidic epitope shorter than 20 amino acids and known HLA allele. Epitopes with post-translational 
modifications were excluded. Only TCRβ chains fully annotated with calculated V gene, J gene and CDR3 junction 
sequences were retained. Due to quality concerns, data originating from SARS-CoV2 epitopes and specific 10xGenomics 
studies (listed here https://github.com/erichardson97/IEDB_IMMREP/blob/main/iedb_immrep/dat/immrep_exclusion.xlsx) 
were excluded, as well as studies contributing few (10 or less) receptors. We additionally removed rows specific to 
epitopes with fewer than 30 receptors, removed the duplicated receptors based on ('Calculated V gene', 
'Calculated J gene', 'Junction Calculated', 'Name', 'Source Organism', 'Source Molecule').

The resulting dataset is provided in this folder as iedb_receptor_data_feb_3_2026_filtered.tsv.