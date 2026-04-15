# Unsupervised machine learning for immune receptors with immuneML: use cases

This repository contains the data and specification files to rerun the use cases from the immuneML 2 manuscript.

To rerun the use cases, clone this repository, make a virtual environment (using conda, pyvenv, or uv) with python 3.11, 
and run the following commands:

```
pip install -r requirements-lock.txt
pip install immuneML==3.0.21
```

> **_NOTE:_** Before running the use cases, check that the paths are correct in the specification files with respect to your result locations.

## Use case 1: generative models

The use case 1 consist of several steps: first, a synthetic dataset is generated, then generative models are trained on this data,
the results are plotted, motif summary is generated and then classification is done to see if the generated data from different models 
could be distinguished.

To replicate, run:

```
immune-ml 00_simulation.yaml 00_simulation/
```

Then run generative models:

```
immune-ml 01_train.yaml 01_train/
```

To generate visualizations:

```
immune-ml 02_visualization_analysis.yaml 02_visualizations/
```

To check whether true motifs were preserved across models:

```
immune-ml 03_true_motif_summary.yaml 03_true_motif_summary/
```

To filter out the data used for training and only try the classification of generated sequences based on model origin:

```
immune-ml 04_remote_train_data.yaml 04_make_dataset_without_train/
```

To run the supervised analysis:

```
immune-ml 05_supervised_classification_of_gen_data.yaml 05_supervised_cls_gen_data
```

Results: https://doi.org/10.5281/zenodo.19564623

## Use case 2: clustering of IEDB data

This use case clusters IEDB data, but also performs several baseline experiments on simulated data. All the experiments have the same structure.
Here it will be shown how to run for IEDB data, but the procedure is the same for all datasets.

The first step is to split data into discovery and validation subsets:

```
immune-ml split_data_to_discovery_and_validation.yaml data/
```

The next step is to perform the clustering analysis on discovery data:

```
immune-ml iedb_clustering.yaml results_discovery_iedb/
```

Finally, the results are validated on validation set:

```
immune-ml validate_clustering.yaml results_validation_iedb/
```

IEDB results: https://doi.org/10.5281/zenodo.19590967
Results on simulated data: https://doi.org/10.5281/zenodo.19565450

## Use case 3: exploring confounders in an experimental dataset

As the data used for this use case is a part of the manuscript in preparation, the data is not shared here yet (it will
be uploaded upon submission of the corresponding manuscript). Here we share the specification files and how to run them
once the data is available.

In the first step, we filtered out sequences coming from invalid loci, keeping only IGH, IGK and IGL.

```
immune-ml specs_filter_bcr.yaml bcr_filtered/
```

Then we peform exploratory analysis of the dataset:

```
immune-ml specs_bcr_exploratory.yaml bcr_filtered_exploratory/
```

We split the data to discovery and validation:

```
immune-ml specs_split_to_discovery_and_validation_bcr.yaml split_bcr_dataset/
```

We run clustering analysis on discovery data:

```
immune-ml specs_bcr_clustering_discovery.yaml bcr_filtered_clustering_discovery/
```

After selecting a clustering approach that was most relevant on discovery data, we peform validation:

```
immune-ml specs_bcr_clustering_validation.yaml bcr_filtered_clustering_validation/
```

