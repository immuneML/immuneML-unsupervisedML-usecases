import json
import plotly.io as pio
import plotly.express as px

def load_fig_from_json(path: str):

    with open(path, 'r') as file:
        fig_dict = json.load(file)

    fig = pio.from_json(json.dumps(fig_dict))
    return fig

def modify_fig(fig):
    fig.update_traces(opacity=0.3)

    fig.data = fig.data[::-1]
    fig.data = [fig.data[i] for i in range(len(fig.data)) if i != 1]

    from plotly.subplots import make_subplots

    legend_group_order = ['LSTM', 'VAE', 'PWM']
    subfig = make_subplots(rows=1, cols=3, shared_yaxes=True, y_title="UMAP2", x_title="UMAP1", horizontal_spacing=0.02,
                           subplot_titles=legend_group_order)
    vivid_palette = px.colors.qualitative.Vivid
    color_mapping = {'original_train': vivid_palette[4], 'LSTM': vivid_palette[0], 'VAE': vivid_palette[2], 'PWM': vivid_palette[1]}

    trace1 = fig.data[0]
    for i, idx in enumerate([1, 2, 3], start=1):
        col = legend_group_order.index(fig.data[idx]['legendgroup']) + 1
        subfig.add_trace(trace1.update(showlegend=(i == 1)), row=1, col=col)
        trace = fig.data[idx]
        trace.update(marker=dict(color=color_mapping.get(trace.legendgroup)))
        subfig.add_trace(trace, row=1, col=col)
    subfig.update_layout(template='plotly_white', font=dict(size=18))

    return subfig

def save_fig(subfig, path):
    subfig.write_html(path)


if __name__ == '__main__':
    path = "02_visualizations/data_reports/analysis_4mer_analysis/report_dim_red_umap/dimensionality_reduction_data_origin.json"
    fig = load_fig_from_json(path)
    subfig = modify_fig(fig)
    subfig.write_json("umap_4mer_split.json")
    save_fig(subfig, "umap_4mer_split.html")