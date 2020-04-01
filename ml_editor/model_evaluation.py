from sklearn.calibration import calibration_curve
from sklearn.metrics import (
    confusion_matrix,
    roc_curve,
    auc,
    brier_score_loss,
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
)
import matplotlib.pyplot as plt 
import numpy as np 
from itertools import product


class ConfusionMatrixDisplay:
    """Confusion Matrix visualization.

    It is recommend to use :func:`~sklearn.metrics.plot_confusion_matrix` to
    create a :class:`ConfusionMatrixDisplay`. All parameters are stored as
    attributes.

    Read more in the :ref:`User Guide <visualizations>`.

    Parameters
    ----------
    confusion_matrix : ndarray of shape (n_classes, n_classes)
        Confusion matrix.

    display_labels : ndarray of shape (n_classes,)
        Display labels for plot.

    Attributes
    ----------
    im_ : matplotlib AxesImage
        Image representing the confusion matrix.

    text_ : ndarray of shape (n_classes, n_classes), dtype=matplotlib Text, \
            or None
        Array of matplotlib axes. `None` if `include_values` is false.

    ax_ : matplotlib Axes
        Axes with confusion matrix.

    figure_ : matplotlib Figure
        Figure containing the confusion matrix.
    """
    def __init__(self, confusion_matrix, display_labels):
        self.confusion_matrix = confusion_matrix
        self.display_labels = display_labels

    def plot(self, include_values=True, cmap='viridis', font_size=12,
             xticks_rotation='horizontal', values_format=None, ax=None):
        """Plot visualization.

        Parameters
        ----------
        include_values : bool, default=True
            Includes values in confusion matrix.

        cmap : str or matplotlib Colormap, default='viridis'
            Colormap recognized by matplotlib.

        xticks_rotation : {'vertical', 'horizontal'} or float, \
                         default='horizontal'
            Rotation of xtick labels.

        values_format : str, default=None
            Format specification for values in confusion matrix. If `None`,
            the format specification is '.2g'.

        ax : matplotlib axes, default=None
            Axes object to plot on. If `None`, a new figure and axes is
            created.

        Returns
        -------
        display : :class:`~sklearn.metrics.ConfusionMatrixDisplay`
        """
        import matplotlib.pyplot as plt

        if ax is None:
            fig, ax = plt.subplots()
        else:
            fig = ax.figure

        cm = self.confusion_matrix
        n_classes = cm.shape[0]
        self.im_ = ax.imshow(cm, interpolation='nearest', cmap=cmap)
        self.text_ = None

        cmap_min, cmap_max = self.im_.cmap(0), self.im_.cmap(256)

        if include_values:
            self.text_ = np.empty_like(cm, dtype=object)
            if values_format is None:
                values_format = '.2g'

            # print text with appropriate color depending on background
            thresh = (cm.max() + cm.min()) / 2.0
            for i, j in product(range(n_classes), range(n_classes)):
                color = cmap_max if cm[i, j] < thresh else cmap_min
                self.text_[i, j] = ax.text(j, i,
                                           format(cm[i, j], values_format),
                                           ha="center", va="center",
                                           color=color, 
                                           fontdict={'size': font_size})

        fig.colorbar(self.im_, ax=ax, fraction=0.046, pad=0.04)
        ax.set(xticks=np.arange(n_classes),
               yticks=np.arange(n_classes),
               xticklabels=self.display_labels,
               yticklabels=self.display_labels,
               ylabel="True label",
               xlabel="Predicted label",
               )
        
        for item in ([ax.xaxis.label, ax.yaxis.label] +
             ax.get_xticklabels() + ax.get_yticklabels()):
            item.set_fontsize(font_size)

        ax.set_ylim((n_classes - 0.5, -0.5))
        plt.setp(ax.get_xticklabels(), rotation=xticks_rotation)

        self.figure_ = fig
        self.ax_ = ax
        return self


def get_confusion_matrix_plot(
    y_true,
    y_pred,
    labels=None,
    sample_weight=None, normalize=None,
    display_labels=None, include_values=True,
    xticks_rotation='horizontal',
    values_format=None,
    cmap='viridis',
    figsize=(10, 10),
    font_size=12,
    title='Confusion Matrix'
    ):
    """Plot Confusion Matrix.

    Parameters
    ----------
    y_true : array-like of shape (n_samples,)
        Target values

    y_pred : array-like of shape (n_samples,)
        Predicted values

    labels : array-like of shape (n_classes,), default=None
        List of labels to index the matrix. This may be used to reorder or
        select a subset of labels. If `None` is given, those that appear at
        least once in `y_true` or `y_pred` are used in sorted order.

    sample_weight : array-like of shape (n_samples,), default=None
        Sample weights.

    normalize : {'true', 'pred', 'all'}, default=None
        Normalizes confusion matrix over the true (rows), predicted (columns)
        conditions or all the population. If None, confusion matrix will not be
        normalized.

    display_labels : array-like of shape (n_classes,), default=None
        Target names used for plotting. By default, `labels` will be used if
        it is defined, otherwise the unique labels of `y_true` and `y_pred`
        will be used.

    include_values : bool, default=True
        Includes values in confusion matrix.

    xticks_rotation : {'vertical', 'horizontal'} or float, \
                        default='horizontal'
        Rotation of xtick labels.

    values_format : str, default=None
        Format specification for values in confusion matrix. If `None`,
        the format specification is '.2g'.

    cmap : str or matplotlib Colormap, default='viridis'
        Colormap recognized by matplotlib.

    font_size : int
        Fontsize of the axis and text labels

    Returns
    -------
    display
    """
    f, ax = plt.subplots(figsize=figsize)
    ax.set_title(title, fontdict={'fontsize': 20}, loc='center')

    cm = confusion_matrix(y_true, y_pred, sample_weight=sample_weight,
                          labels=labels, normalize=normalize)

    if display_labels is None:
        if labels is None:
            display_labels = ['Low quality', 'High quality']
        else:
            display_labels = labels

    disp = ConfusionMatrixDisplay(confusion_matrix=cm,
                                  display_labels=display_labels
                                  )
    return disp.plot(include_values=include_values,
                     cmap=cmap, ax=ax, xticks_rotation=xticks_rotation,
                     values_format=values_format, 
                     font_size=font_size)


def get_roc_plot(
    predicted_proba_y, true_y, tpr_bar=-1, fpr_bar=-1, figsize=(10, 10)
):
    """
    Inspired by sklearn example
    https://scikit-learn.org/stable/auto_examples/model_selection/plot_roc_crossval.html
    Parameters
    ----------
    predicted_proba_y: array-like of shape (n_samples,)
        the predicted probabilities of our model for each example
    true_y: array-like of shape (n_samples,)
        the true value of the label
    tpr_bar: float
        A threshold false negative value to draw
    fpr_bar: float 
        A threshold false positive value to draw
    figsize: tuple
        size of the output figure
    
    Returns
    -------
    ROC plot
    """
    fpr, tpr, thresholds = roc_curve(true_y, predicted_proba_y)
    roc_auc = auc(fpr, tpr)

    plt.figure(figsize=figsize)
    plt.plot(
        fpr,
        tpr,
        lw=1,
        alpha=1,
        color="black",
        label="ROC curve (AUC = %0.2f)" % roc_auc,
    )
    plt.plot(
        [0, 1],
        [0, 1],
        linestyle="--",
        lw=2,
        color="grey",
        label="Chance",
        alpha=1,
    )

    # Cheating on position to make plot more readable
    plt.plot(
        [0.01, 0.01, 1],
        [0.01, 0.99, 0.99],
        linestyle=":",
        lw=2,
        color="green",
        label="Perfect model",
        alpha=1,
    )

    if tpr_bar != -1:
        plt.plot(
            [0, 1],
            [tpr_bar, tpr_bar],
            linestyle="-",
            lw=2,
            color="red",
            label="TPR requirement",
            alpha=1,
        )
        plt.fill_between([0, 1], [tpr_bar, tpr_bar], [1, 1], alpha=0, hatch="\\")

    if fpr_bar != -1:
        plt.plot(
            [fpr_bar, fpr_bar],
            [0, 1],
            linestyle="-",
            lw=2,
            color="red",
            label="FPR requirement",
            alpha=1,
        )
        plt.fill_between([fpr_bar, 1], [1, 1], alpha=0, hatch="\\")

    plt.legend(loc="lower right")

    plt.ylabel("True positive rate", fontsize=20)
    plt.xlabel("False positive rate", fontsize=20)
    plt.xlim(0, 1)
    plt.ylim(0, 1)


def get_calibration_plot(predicted_proba_y, true_y, figsize=(10, 10)):
    """Calibration plot
    
    Parameters
    ----------
    predicted_proba_y : array-like of shape (n_samples,)
        Predicted probabilities of the model for each example
    true_y : array-like of shape (n_samples,)
        True value of the label
    figsize : tuple, optional
        size of the output figure, by default (10, 10)
    """
    plt.figure(figsize=figsize)
    ax1 = plt.subplot2grid((3, 1), (0, 0), rowspan=2)
    ax2 = plt.subplot2grid((3, 1), (2, 0))

    ax1.plot([0, 1], [0, 1], 'k:', label="Perfectly calibrated")
    clf_score = brier_score_loss(
        true_y, predicted_proba_y, pos_label=true_y.max()
    )
    print("\tBrier: {:1.3f}".format(clf_score))

    fraction_of_positives, mean_predicted_value = calibration_curve(
        true_y, predicted_proba_y, n_bins=10
    )

    ax1.plot(
        mean_predicted_value,
        fraction_of_positives,
        "s-",
        color="black",
        label="{:1.3f} Brier score (0 is best, 1 is worst)".format(clf_score)
    )

    ax2.hist(
        predicted_proba_y,
        range=(0, 1),
        bins=10,
        histtype="step",
        lw=2,
        color="black",
    )

    ax1.set_ylabel("Fraction of positives")
    ax1.set_xlim([0, 1])
    ax1.set_ylim([0, 1])
    ax1.legend(loc="lower right")
    ax1.set_title("Calibration plot")

    ax2.set_title("Probability distribution")
    ax2.set_xlabel('Mean predicted value')
    ax2.set_ylabel("Count")
    ax2.legend(loc="upper center", ncol=2)

    plt.tight_layout()