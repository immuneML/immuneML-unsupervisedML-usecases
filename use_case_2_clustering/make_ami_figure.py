import math


def main(path, fig_path, value_name: str='ami_score', value_name_on_plot: str='adjusted mutual information (epitope)',
         legend_inside_plot: bool = True):
    import plotly.express as px
    import pandas as pd

    df = pd.read_csv(path)

    melted_df = df.melt(id_vars=['split_id'], var_name='clustering_approach', value_name=value_name)

    # extract and prepare columns
    melted_df['encoding'] = melted_df['clustering_approach'].str.replace("_pca", "").replace(
        r"_kmeans\d*", "", regex=True).replace(r"_hierarchical_\d*", "", regex=True)
    encodings = melted_df.encoding.unique().tolist()
    melted_df['clustering_method'] = (melted_df['clustering_approach'].str.replace("|".join(encodings), "", regex=True)
                                      .replace(r"_pca_", "", regex=True).replace(r"_", "", regex=True)
                                      .replace(r"\d*", "", regex=True))
    melted_df['num_clusters'] = melted_df['clustering_approach'].str.replace("prot_5", "").str.extract(r"(\d+)", expand=False)
    melted_df['clustering_method_with_clusters'] = melted_df['clustering_method'] + melted_df['num_clusters']

    melted_df.num_clusters = melted_df.num_clusters.astype(int)
    melted_df.clustering_approach = melted_df.clustering_approach.str.replace("_pca", "")
    melted_df.encoding[melted_df.encoding == 'tcr_bert'] = 'tcrbert'
    melted_df.encoding[melted_df.encoding == 'tcr_dist'] = 'tcrdist'
    melted_df.encoding[melted_df.encoding == 'prot_5'] = 'prott5'
    melted_df.sort_values(by=['num_clusters', 'encoding'], ascending=False, inplace=True)

    # make figure
    fig = px.box(melted_df, x='clustering_approach', y=value_name, color='encoding', facet_col='num_clusters',
                 labels={'clustering_approach': '', value_name: value_name_on_plot},
                 color_discrete_map=dict(zip(sorted(melted_df.encoding.unique().tolist()), px.colors.qualitative.Vivid)))

    fig.update_layout(template='plotly_white', boxmode='overlay')

    def get_percentile(data, p):
        data.sort()
        n = len(data)
        x = n * p + 0.5

        #  If integer, return
        if x.is_integer():
            return round(data[int(x - 1)], 6)  # account for zero-indexing

        #  If not an integer, get the interpolated value of the values of floor and ceiling indices
        x1, x2 = math.floor(x), math.ceil(x)
        y1, y2 = data[x1 - 1], data[x2 - 1]  # account for zero-indexing
        return round(np.interp(x=x, xp=[x1, x2], fp=[y1, y2]), 6)

    # add median values to each box
    import numpy as np
    for trace in fig.data:
        if len(trace.y):
            xs = np.array(trace.x)
            ys = np.array(trace.y, dtype=float)
            med = get_percentile(ys, 0.5)
            q1 = get_percentile(ys, 0.25)
            q3 = get_percentile(ys, 0.75)
            iqr = q3 - q1
            upper_limit = q3 + 1.5 * iqr
            upper_fence = round(max([i for i in ys.tolist() if i <= upper_limit]), 6)
            fig.add_annotation(
                x=set(xs).pop(),
                y=upper_fence,
                text=str(abs(round(med, 3)) if med < 0 and round(med, 3) == 0 else round(med, 3)),
                showarrow=False,
                xref=trace.xaxis,
                yref=trace.yaxis,
                yanchor='bottom',
                font=dict(size=12)
            )

    # fix x axis ticks and title
    fig.update_xaxes(matches=None)
    fig.for_each_xaxis(lambda x: x.update(title=''))
    fig.add_annotation(
        text='clustering approach',
        xref='paper', yref='paper',
        x=0.5, y=-0.23, showarrow=False,
    )

    vals = sorted(melted_df['clustering_approach'].unique())
    rename = {v: fix_x_names(v) for v in vals}

    fig.for_each_xaxis(lambda x: x.update(
        tickvals=list(rename.keys()),
        ticktext=list(rename.values())
    ))

    # position legend inside the plot
    if legend_inside_plot:
        fig.update_layout(
            legend=dict(
                x=1,
                y=0.96,
                xanchor='right',
                yanchor='top'
            )
        )

    fig.write_image(fig_path, width=1200, height=600, scale=2)

def fix_x_names(v):
    import re
    mapping = {
        r'kmeans\d*': 'kmeans',
        r'hierarchical_\d*': 'hierarchical',
        'tcr_bert': 'tcrbert',
        'tcr_dist': 'tcrdist',
        'prot_5': 'prott5'
    }
    for pattern, replacement in mapping.items():
        v = re.sub(pattern, replacement, v)
    return v

if __name__ == '__main__':
    import plotly.io as pio
    pio.kaleido.scope.mathjax = None

    # # IEDB
    main("adjusted_mutual_info_score__epitope_name.csv", 'iedb_epitope_ami.png')
    main("adjusted_rand_score_per_cl_setting.csv", 'iedb_stability.png', value_name='ari_score',
         value_name_on_plot='stability (adjusted Rand index)', legend_inside_plot=False)

    # # highly similar sequences
    path = 'highly_similar_sequences/'
    main(path + 'adjusted_mutual_info_score__motif.csv', 'highly_similar_seqs_motif_ami.png',
         value_name_on_plot='adjusted mutual information (motif)', legend_inside_plot=False)
    main(path + 'adjusted_rand_score_per_cl_setting.csv', 'highly_similar_seqs_stability.png',
         value_name_on_plot='stability (adjusted Rand index)', legend_inside_plot=False, value_name='ari_score')
    main(path + 'silhouette_score.csv', 'highly_similar_seqs_silhouette.png',
         value_name_on_plot='silhouette score', legend_inside_plot=False, value_name='silhouette_score')

    # moderately similar
    path = 'moderately_similar_seqs/'
    main(path + 'adjusted_mutual_info_score__motif.csv', 'moderately_similar_seqs_motif_ami.png',
         value_name_on_plot='adjusted mutual information (motif)', legend_inside_plot=False)
    main(path + 'adjusted_rand_score_per_cl_setting.csv', 'moderately_similar_seqs_stability.png',
         value_name_on_plot='stability (adjusted Rand index)', legend_inside_plot=False, value_name='ari_score')

    # non-immune data
    path = 'non_immune_seqs/'
    main(path + 'adjusted_mutual_info_score__epitope1.csv', 'random_epitope_ami.png',
         value_name_on_plot='adjusted mutual information<br>(random epitope label)', legend_inside_plot=False)
    main(path + 'adjusted_rand_score_per_cl_setting.csv', 'random_stability.png',
         value_name_on_plot='stability (adjusted Rand index)', legend_inside_plot=False, value_name='ari_score')

    # olga seqs with random labels
    path = 'olga_random_seqs/'
    main(path + 'adjusted_mutual_info_score__epitope_name.csv', 'olga_random_epitope_ami.png',
         value_name_on_plot='adjusted mutual information<br>(random epitope label)', legend_inside_plot=False)
    main(path + 'adjusted_rand_score_per_cl_setting.csv', 'olga_random_stability.png',
         value_name_on_plot='stability (adjusted Rand index)', legend_inside_plot=False, value_name='ari_score')

    # make suppl fig for AMI across labels in iedb data
    main("adjusted_mutual_info_score__epitope_source_molecule.csv",
         'iedb_epitope_molecule.png', value_name_on_plot='adjusted mutual information<br>(source molecule)', legend_inside_plot=False)
    main(
        "adjusted_mutual_info_score__epitope_source_organism.csv",
        'iedb_epitope_organism.png', value_name_on_plot='adjusted mutual information<br>(source organism)',
        legend_inside_plot=False)
    main("adjusted_mutual_info_score__mhc_allele_names.csv",
         'iedb_mhc.png', value_name_on_plot='adjusted mutual information (MHC)', legend_inside_plot=False)