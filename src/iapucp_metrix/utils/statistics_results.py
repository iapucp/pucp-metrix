import statistics
from dataclasses import dataclass
from typing import Callable

from spacy.tokens import Doc


@dataclass
class StatisticsResults:
    """
    This data class stores the mean and standard deviation.
    """

    mean: float = 0
    std: float = 0


def get_mean_std_of_metric(
    doc: Doc, counter_function: Callable, statistic_type: str = "all"
) -> StatisticsResults:
    """
    This method returns the mean and/or standard deviation of a descriptive metric.

    Parameters:
    doc(Doc): The text to be anaylized.
    counter_function(Callable): This callable will calculate the values to add to the counter array in order to calculate the standard deviation. It receives a Spacy Doc and it should return a list or number.
    statistic_type(str): Whether to calculate the mean and/or the standard deviation. It accepts 'mean', 'std' or 'all'.

    Returns:
    StatisticsResults: The mean and/or standard deviation of the current metric.
    """
    if len(doc.text) == 0:
        raise ValueError("The text is empty.")
    elif statistic_type not in ["mean", "std", "all"]:
        raise ValueError("'statistic_type' can only take 'mean', 'std' or 'all'.")
    else:
        counter = counter_function(doc)  # Find the values to add to the counter
        stat_results = StatisticsResults()
        # Calculate the statistics
        if statistic_type in ["std", "all"]:
            stat_results.std = statistics.pstdev(counter) if len(counter) > 0 else 0

        if statistic_type in ["mean", "all"]:
            stat_results.mean = statistics.mean(counter) if len(counter) > 0 else 0

        return stat_results
