import statistics
from itertools import combinations, tee
from time import time
from typing import Callable, Dict, Iterator, List, Tuple

from spacy.language import Language
from spacy.tokens import Doc, Span

from iapucp_metrix.utils.statistics_results import StatisticsResults


def doc_adjacent_sentence_pairs_getter(doc: Doc) -> Tuple[Span, Span]:
    """
    Iterator that returns all pairs of adjacent sentences.

    Parameters:
    doc(Doc): The document to analyze.

    Yields:
    Tuple[Span, Span]: Pair of spans that represent two adjacent sentences.
    """
    sentences = doc._.non_empty_sentences
    prev, cur = tee(sentences)
    next(cur, None)
    # Return each pair of sentences
    for prev, cur in zip(prev, cur):
        yield prev, cur


def doc_all_sentence_pairs_getter(doc: Doc) -> Tuple[Span, Span]:
    """
    Iterator that returns all pairs of sentences.

    Parameters:
    doc(Doc): The document to analyze.

    Yields:
    Tuple[Span, Span]: Pair of spans that represent a pair of sentences.
    """
    sentences = doc._.non_empty_sentences
    # Return each pair of sentences
    for prev, cur in combinations(sentences, 2):
        yield prev, cur


class ReferentialCohesionIndices:
    """
    This class will handle all operations to find the synthactic pattern density indices of a text according to Coh-Metrix.
    """

    name = "referential_cohesion_indices"

    # TODO: Implement multiprocessing
    def __init__(
        self,
        nlp: Language,
        noun_overlap_func: Callable,
        argument_overlap_func: Callable,
        stem_overlap_func: Callable,
        content_word_overlap_func: Callable,
        anaphore_overlap_func: Callable,
    ) -> None:
        """
        The constructor will initialize this object that calculates the synthactic pattern density indices for a specific language of those that are available.

        Parameters:
        nlp(Language): The spacy model that corresponds to a language.

        Returns:
        None.
        """
        required_pipes = ["cohesion_words_tokenizer"]
        if not all((pipe in nlp.pipe_names for pipe in required_pipes)):
            message = (
                "Referential cohesion indices need the following pipes: "
                + ", ".join(required_pipes)
            )
            raise AttributeError(message)

        self._nlp = nlp
        self._noun_overlap_func = noun_overlap_func
        self._argument_overlap_func = argument_overlap_func
        self._stem_overlap_func = stem_overlap_func
        self._content_word_overlap_func = content_word_overlap_func
        self._anaphore_overlap_func = anaphore_overlap_func
        Doc.set_extension("referential_cohesion_indices", default={})
        Doc.set_extension(
            "adjacent_sentence_pairs", getter=doc_adjacent_sentence_pairs_getter
        )
        Doc.set_extension("all_sentence_pairs", getter=doc_all_sentence_pairs_getter)

    def __call__(self, doc: Doc) -> Doc:
        """
        This method will calculate the referential cohesion indices.

        Parameters:
        doc(Doc): A Spacy document.

        Returns:
        Doc: The analyzed spacy document.
        """
        if len(doc.text) == 0:
            raise ValueError("The text is empty.")

        start = time()
        self.__get_overlap_adjacent_sentences(doc)
        self.__get_overlap_all_sentences(doc)

        return doc

    def __calculate_overlap_for_sentences(
        self, values: List = [], statistic_type: str = "mean"
    ) -> StatisticsResults:
        """
        This method calculates the overlap for adjacent sentences in a text. MULTIPROCESSING STILL NOT IMPLEMENTED.

        Parameters:
        values(List): The values to calculate their statistics
        statistic_type(str): Whether to calculate the mean and/or the standard deviation. It accepts 'mean', 'std' or 'all'.

        Returns:
        StatisticsResults: The standard deviation and mean of the overlap.
        """
        if statistic_type not in ["mean", "std", "all"]:
            raise ValueError("'statistic_type' can only take 'mean', 'std' or 'all'.")
        else:
            referential_cohesion = values
            stat_results = StatisticsResults()  # Create empty container

            if len(referential_cohesion) == 0:
                return stat_results
            else:
                if statistic_type in ["mean", "all"]:
                    stat_results.mean = statistics.mean(referential_cohesion)

                if statistic_type in ["std", "all"]:
                    stat_results.std = statistics.pstdev(referential_cohesion)

                return stat_results

    def __get_overlap_of_sentences(self, doc: Doc, sentences: Iterator) -> Dict:
        """
        Method that calculates all overlaps for the sentences passed as an iterator.

        Paramters:
        doc(Doc): The document to analyze.
        sentences(Iterator): Pair of sentences to analyze

        Returns:
        Dict: Dictionary with the overlap analysis for each type of word. Content word returns a StatisticsResult object
        """
        noun_overlap = []
        argument_overlap = []
        stem_overlap = []
        content_word_overlap = []
        anaphore_overlap = []
        # Iterate over all adjacent sentence pairs to analyze them
        for prev, cur in sentences:
            noun_overlap.append(self._noun_overlap_func(prev, cur))
            argument_overlap.append(self._argument_overlap_func(prev, cur))
            stem_overlap.append(self._stem_overlap_func(prev, cur))
            content_word_overlap.append(self._content_word_overlap_func(prev, cur))
            anaphore_overlap.append(self._anaphore_overlap_func(prev, cur))

        return {
            "noun_overlap": self.__calculate_overlap_for_sentences(
                noun_overlap, "mean"
            ).mean,
            "argument_overlap": self.__calculate_overlap_for_sentences(
                argument_overlap, "mean"
            ).mean,
            "stem_overlap": self.__calculate_overlap_for_sentences(
                stem_overlap, "mean"
            ).mean,
            "content_word_overlap": self.__calculate_overlap_for_sentences(
                content_word_overlap, "all"
            ),
            "anaphore_overlap": self.__calculate_overlap_for_sentences(
                anaphore_overlap, "mean"
            ).mean,
        }

    def __get_overlap_adjacent_sentences(self, doc: Doc) -> None:
        """
        Method that calculates the overlap for nouns, arguments, stems, content words and anaphores of adjacent sentences.

        Parameters:
        doc(Doc): The document to analyze.
        """
        overlap = self.__get_overlap_of_sentences(doc, doc._.adjacent_sentence_pairs)
        doc._.referential_cohesion_indices["CRFNO1"] = overlap["noun_overlap"]
        doc._.referential_cohesion_indices["CRFAO1"] = overlap["argument_overlap"]
        doc._.referential_cohesion_indices["CRFSO1"] = overlap["stem_overlap"]
        doc._.referential_cohesion_indices["CRFCWO1"] = overlap[
            "content_word_overlap"
        ].mean
        doc._.referential_cohesion_indices["CRFCWO1d"] = overlap[
            "content_word_overlap"
        ].std
        doc._.referential_cohesion_indices["CRFANP1"] = overlap["anaphore_overlap"]

    def __get_overlap_all_sentences(self, doc: Doc) -> None:
        """
        Method that calculates the overlap for nouns, arguments, stems, content words and anaphores of all sentences.

        Parameters:
        doc(Doc): The document to analyze.
        """
        overlap = self.__get_overlap_of_sentences(doc, doc._.all_sentence_pairs)
        doc._.referential_cohesion_indices["CRFNOa"] = overlap["noun_overlap"]
        doc._.referential_cohesion_indices["CRFAOa"] = overlap["argument_overlap"]
        doc._.referential_cohesion_indices["CRFSOa"] = overlap["stem_overlap"]
        doc._.referential_cohesion_indices["CRFCWOa"] = overlap[
            "content_word_overlap"
        ].mean
        doc._.referential_cohesion_indices["CRFCWOad"] = overlap[
            "content_word_overlap"
        ].std
        doc._.referential_cohesion_indices["CRFANPa"] = overlap["anaphore_overlap"]
