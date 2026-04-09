import pandas as pd
import plotly.express as px

from immuneML import Constants

NON_SIGNAL_COLS = {'cdr3_aa', 'cdr3', 'v_call', 'j_call', 'locus', 'signals_aggregated', 'data_origin', 'novelty_memorization'}


def get_signal_names(df):
    return [col for col in df.columns if col not in NON_SIGNAL_COLS and not col.endswith('_positions')]


def get_seq_counts(df, signal_names):
    signal_mask = df[signal_names].sum(axis=1) > 0
    seq_count_with_signals = df[signal_mask].groupby('data_origin').size().reset_index(name='seq_count_with_signal')
    seq_count_total = df.groupby('data_origin').size().reset_index(name='total_sequences')
    seq_counts_df = seq_count_with_signals.merge(seq_count_total, on='data_origin', how='left')
    seq_counts_df['signal_specific_percent'] = seq_counts_df['seq_count_with_signal'] / seq_counts_df['total_sequences'] * 100
    seq_counts_df['label'] = seq_counts_df.apply(
        lambda row: f"{row['data_origin']}<br>Signal-specific sequences: {row['signal_specific_percent']:.2f}%", axis=1)
    return seq_counts_df


def prepare_plotting_data(df, signal_names, sorted_data_origins, seq_counts_df):
    df_grouped = df.groupby(['data_origin', 'novelty_memorization'])[signal_names].sum().reset_index()
    df_melted = df_grouped.melt(id_vars=['data_origin', 'novelty_memorization'], var_name='signal', value_name='count')
    df_melted['data_origin'] = pd.Categorical(df_melted['data_origin'], categories=sorted_data_origins, ordered=True)
    df_melted = df_melted.sort_values(['data_origin', 'novelty_memorization', 'signal'])
    df_melted = df_melted.merge(seq_counts_df, on='data_origin', how='left')
    df_melted['frequency'] = df_melted.groupby(['data_origin', 'signal'])['count'].transform(
        lambda x: x / df_melted['total_sequences'])
    return df_melted


def plot_from_csv(csv_path):
    vivid_palette = px.colors.qualitative.Vivid
    color_mapping = {'original_train': vivid_palette[4], 'LSTM': vivid_palette[0], 'VAE': vivid_palette[2], 'PWM': vivid_palette[1]}
    opacity_map = {"original": 1.0, "memorized": 1.0, "novel": 0.5}

    df = pd.read_csv(csv_path)
    df = df[df['data_origin'] != 'original_test']

    signal_names = get_signal_names(df)

    seq_counts_df = get_seq_counts(df, signal_names)
    seq_counts_df['sort_key'] = seq_counts_df['data_origin'].apply(
        lambda x: (0, 0) if x == 'original_train' else (
            1, -seq_counts_df.loc[seq_counts_df['data_origin'] == x, 'signal_specific_percent'].iloc[0]))
    sorted_data_origins = seq_counts_df.sort_values('sort_key')['data_origin'].tolist()

    df_melted = prepare_plotting_data(df, signal_names, sorted_data_origins, seq_counts_df)
    df_melted['data_origin_novelty'] = df_melted['data_origin'].astype(str) + ' - ' + df_melted['novelty_memorization']

    figure = px.bar(df_melted, x='signal', y='frequency', color='data_origin_novelty',
                    facet_col='label', color_discrete_sequence=vivid_palette,
                    barmode='stack',
                    title='Percentage of sequences containing signals across different generated datasets')

    for trace in figure.data:
        data_origin, novelty = trace.name.split(' - ')
        trace.opacity = opacity_map.get(novelty, 1.0)
        if data_origin in color_mapping:
            trace.marker.color = color_mapping[data_origin]

    figure.for_each_annotation(lambda a: a.update(text=a.text.replace("label=", "").replace("Signal-specific sequences:", "")))
    figure.update_layout(xaxis_title='', yaxis_title='Frequency', bargap=0.2,
                         template='plotly_white', font=dict(size=18), title='')
    figure.layout.legend.title = ''

    # Add per-segment annotations: compute cumulative tops manually per (xaxis, x_val)
    cumulative = {}
    for trace in figure.data:
        xref = trace.xaxis if trace.xaxis else 'x'
        yref = trace.yaxis if trace.yaxis else 'y'
        for x_val, y_val in zip(trace.x, trace.y):
            key = (xref, x_val)
            cumulative[key] = cumulative.get(key, 0.0) + float(y_val)
            if not y_val or round(y_val, 3) == 0:
                continue
            figure.add_annotation(
                x=x_val, y=cumulative[key],
                text=f'{y_val:.3f}'.rstrip('0').rstrip('.'),
                showarrow=False, yanchor='bottom', xanchor='center',
                textangle=0, font=dict(size=12, color=Constants.PLOTLY_BLACK),
                xref=xref, yref=yref
            )

    return figure


if __name__ == '__main__':
    csv_path = "03_true_motif_summary/data_reports/analysis_true_motif_summary/report_true_motif_summary/annotated_sequences.csv"
    fig = plot_from_csv(csv_path)
    fig.write_json("true_motif_summary_barplot_v2.json")
    fig.write_html("true_motif_summary_barplot_v2.html")
    fig.write_image("true_motif_summary_barplot_v2.pdf")