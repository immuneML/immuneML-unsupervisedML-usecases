import numpy as np
import pandas as pd
import plotly.express as px
from sklearn.metrics import adjusted_mutual_info_score


def main():
    discovery_predictions = pd.read_csv("iedb_seqs_subset/validation_data_plot/discovery/best_settings_predictions_full_dataset.csv")

    plot_data = {
        'discovery': {
            'epitope specificity': adjusted_mutual_info_score(discovery_predictions['epitope_name'], discovery_predictions['predictions_tcr_dist_hierarchical_3500']),
            'MHC allele information': adjusted_mutual_info_score(discovery_predictions['mhc_allele_names'], discovery_predictions['predictions_tcr_dist_hierarchical_3500']),
        },
        'result_based': {
            'epitope specificity': 0.12135368245826215,
            'MHC allele information': 0.031243776629862222
        },
        'method_based': {
            'epitope specificity': 0.13438287103560334,
            'MHC allele information': 0.03692533161620867
        }
    }

    df = pd.DataFrame(plot_data).reset_index().rename(columns={'index': 'property'}).melt(id_vars=['property'], var_name='origin', value_name='adjusted mutual information')
    print(df)
    df['adjusted mutual information'] = np.round(df['adjusted mutual information'], 3)

    fig = px.bar(df, x='property', y='adjusted mutual information', color_discrete_sequence=px.colors.qualitative.Vivid,
                 color='origin', barmode='group', text_auto=True)
    fig.update_layout(template='plotly_white')

    fig.update_layout(
        legend=dict(
            x=1,
            y=0.96,
            xanchor='right',
            yanchor='top'
        )
    )

    fig.write_image('validation_ami_performance.png')


if __name__ == '__main__':
    main()