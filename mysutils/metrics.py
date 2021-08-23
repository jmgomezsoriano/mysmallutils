from sys import stdout
from typing import List, Dict, TextIO

from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score, precision_score, recall_score, \
    jaccard_score

# MEASURES ATTRIBUTES
SIMPLE_ACCURACY = 'simple_accuracy'
BALANCED_ACCURACY = 'balanced_accuracy'
MICRO_F1 = 'micro_f1'
MACRO_F1 = 'macro_f1'
WEIGHTED_F1 = 'weighted_f1'
MICRO_PRECISION = 'micro_precision'
MACRO_PRECISION = 'macro_precision'
WEIGHTED_PRECISION = 'weighted_precision'
MICRO_RECALL = 'micro_recall'
MACRO_RECALL = 'macro_recall'
WEIGHTED_RECALL = 'weighted_recall'
MICRO_JACCARD = 'micro_jaccard'
MACRO_JACCARD = 'macro_jaccard'
WEIGHTED_JACCARD = 'weighted_jaccard'
ALL_METRICS = (SIMPLE_ACCURACY, BALANCED_ACCURACY, MICRO_F1, MACRO_F1, WEIGHTED_F1, MICRO_PRECISION, MACRO_PRECISION,
               WEIGHTED_PRECISION, MICRO_RECALL, MACRO_RECALL, WEIGHTED_RECALL, MICRO_JACCARD, MACRO_JACCARD,
               WEIGHTED_JACCARD)


def metrics(trues: List[int], predictions: List[int]) -> Dict[str, float]:
    """
    Calculate the different metrics from the list of real classes and the predicted ones.
    :param trues: The real classes for each sample.
    :param predictions: The predicted classes for each sample.
    :return: A dictionary with the measure names and their respective values.
    """
    met = {SIMPLE_ACCURACY: accuracy_score(trues, predictions),
           BALANCED_ACCURACY: balanced_accuracy_score(trues, predictions),
           MICRO_F1: f1_score(trues, predictions, average='micro'),
           MACRO_F1: f1_score(trues, predictions, average='macro'),
           WEIGHTED_F1: f1_score(trues, predictions, average='weighted'),
           MICRO_PRECISION: precision_score(trues, predictions, average='micro'),
           MACRO_PRECISION: precision_score(trues, predictions, average='macro'),
           WEIGHTED_PRECISION: precision_score(trues, predictions, average='weighted'),
           MICRO_RECALL: recall_score(trues, predictions, average='micro'),
           MACRO_RECALL: recall_score(trues, predictions, average='macro'),
           WEIGHTED_RECALL: recall_score(trues, predictions, average='weighted'),
           MICRO_JACCARD: jaccard_score(trues, predictions, average='micro'),
           MACRO_JACCARD: jaccard_score(trues, predictions, average='macro'),
           WEIGHTED_JACCARD: jaccard_score(trues, predictions, average='weighted')}
    return met


def print_metrics(metrics: Dict[str, float], measures: List[str] = ALL_METRICS, file: TextIO = stdout) -> None:
    """
    Print the metrics of an evaluation.
    :param metrics: The a dictionary with the metrics to print.
    :param measures: The list to measures to print.
    :param file: The file handler where the result are printed. By default in the standard output.
    """
    _print_metric_if_show('Simple accuracy', metrics, SIMPLE_ACCURACY, measures, file)
    _print_metric_if_show('Balanced accuracy', metrics, BALANCED_ACCURACY, measures, file)
    print(file=file)
    _print_metric_if_show('Micro f-measure', metrics, MICRO_F1, measures, file)
    _print_metric_if_show('Macro f-measure', metrics, MACRO_F1, measures, file)
    _print_metric_if_show('Weighted f-measure', metrics, WEIGHTED_F1, measures, file)
    print(file=file)
    _print_metric_if_show('Micro precision', metrics, MICRO_PRECISION, measures, file)
    _print_metric_if_show('Macro precision', metrics, MACRO_PRECISION, measures, file)
    _print_metric_if_show('Weighted precision', metrics, WEIGHTED_PRECISION, measures, file)
    print(file=file)
    _print_metric_if_show('Micro recall', metrics, MICRO_RECALL, measures, file)
    _print_metric_if_show('Macro recall', metrics, MACRO_RECALL, measures, file)
    _print_metric_if_show('Weighted recall', metrics, WEIGHTED_RECALL, measures, file)
    print(file=file)
    _print_metric_if_show('Micro Jaccard', metrics, MICRO_JACCARD, measures, file)
    _print_metric_if_show('Macro Jaccard', metrics, MACRO_JACCARD, measures, file)
    _print_metric_if_show('Weighted Jaccard', metrics, WEIGHTED_JACCARD, measures, file)
    print(file=file)


def _print_metric_if_show(msg: str, metrics: Dict[str, float], metric: str, show: List[str], file: TextIO):
    """
    Print a given metric if that metric is selected.
    :param msg: The message to print with the metric.
    :param metrics: All obtained metrics.
    :param metric: The metric to print.
    :param show: The list of metrics which will be printed.
    :param file: The file handler where the result are printed. By default in the standard output.
    """
    if metric in show:
        print(f'{msg}: ', format_value(metrics[metric]), end='\t', file=file)


def format_value(value: float) -> str:
    """
    Format the metrics.
    :param value: The value to format.
    :return: The formated value.
    """
    return '{0:.2f}%'.format(value * 100)
