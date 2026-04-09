import pandas as pd
import plotly.express as px
from matplotlib import pyplot as plt
from sklearn.metrics import ConfusionMatrixDisplay


def main():
    data_path = "05_supervised_cls_gen_data/classification/split_1/data_origin_3mer_encoding_log_reg_optimal/reports/ml_method/conf_matrix/confusion_matrix.csv"
    cm = pd.read_csv(data_path)
    cm = cm.set_index("true/predicted")

    print(cm)
    plt.rcParams.update({'font.size': 14})
    labels = [label.replace('_', '\n') for label in cm.index.tolist()]

    disp = ConfusionMatrixDisplay(confusion_matrix=cm.values, display_labels=labels)
    disp.plot(colorbar=False, cmap='Blues')
    for spine in disp.ax_.spines.values():
        spine.set_visible(False)

    for text in disp.text_.ravel():
        text.set_fontsize(14)

        # Hide the ticks
    disp.ax_.tick_params(axis='both', length=0, labelsize=14)
    plt.savefig("correct_colors_for_heatmap_confusion_matrix_corrected.pdf",
                bbox_inches='tight')  # bbox_inches='tight' avoids extra whitespace
    plt.close()

if __name__ == '__main__':
    main()