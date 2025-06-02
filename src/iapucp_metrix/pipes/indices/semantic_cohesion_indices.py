from importlib.resources import files
from itertools import tee
from time import time

from spacy.language import Language
from spacy.tokens import Doc, Span

from iapucp_metrix.utils.lsa import LsaModel
from iapucp_metrix.utils.statistics_results import get_mean_std_of_metric


class SemanticCohesionIndices:
    """
    This class will handle all operations to obtain the semnatic cohesion indices of a text according to Coh-Metrix
    """

    def __init__(self, nlp: Language) -> None:
        """
        The constructor will initialize the extensions where to hold the semantic cohesion indices of a doc.

        Parameters:
        nlp(Lanuage): The spacy model that corresponds to a language.
        language(str): The language that the texts to process will have.

        Returns:
        None.
        """
        required_pipes = [
            "paragraphizer",
        ]
        if not all((pipe in nlp.pipe_names for pipe in required_pipes)):
            message = (
                "Semantic Cohesion indices pipe need the following pipes: "
                + ", ".join(required_pipes)
            )
            raise AttributeError(message)

        models_dir = files("iapucp_metrix.models")
        lsa_model_path = str(models_dir / "lsa_model.gensim")
        lsa_dictionary_path = str(models_dir / "lsa_dictionary.gensim")

        self._nlp = nlp
        self._lsa_model = LsaModel(nlp, lsa_model_path, lsa_dictionary_path)

        Doc.set_extension("semantic_cohesion_indices", default=dict())  # Dictionary

    def __call__(self, doc: Doc) -> Doc:
        """
        This method will calculate the semantic cohesion indices.

        Parameters:
        doc(Doc): A Spacy document.

        Returns:
        Doc: The processed doc.
        """
        if len(doc.text) == 0:
            raise ValueError("The text is empty.")

        start = time()
        self._get_lsa_overlap_adjacent_sentences(doc)
        self._get_lsa_overlap_all_sentences(doc)
        self._get_lsa_overlap_adjacent_paragraphs(doc)
        self._get_lsa_overlap_given_new_sentences(doc)

        return doc

    def _get_lsa_overlap_adjacent_sentences(self, doc: Doc) -> None:
        """
        This method calculates the lsa overlap for adjacent sentences in the document.

        Parameters:
        doc(doc): The text to be anaylized.
        """

        lsa_overlap = lambda complete_text: [
            self._lsa_model.compute_similarity(prev, cur)
            for prev, cur in complete_text._.adjacent_sentence_pairs
        ]

        metrics = get_mean_std_of_metric(
            doc, counter_function=lsa_overlap, statistic_type="all"
        )
        doc._.semantic_cohesion_indices["SECLOSadj"] = metrics.mean
        doc._.semantic_cohesion_indices["SECLOSadjd"] = metrics.std

    def _get_lsa_overlap_all_sentences(self, doc: Doc) -> None:
        """
        This method calculates the lsa overlap for all sentences in the document.

        Parameters:
        doc(doc): The text to be anaylized.
        """

        lsa_overlap = lambda complete_text: [
            self._lsa_model.compute_similarity(prev, cur)
            for prev, cur in complete_text._.all_sentence_pairs
        ]

        metrics = get_mean_std_of_metric(
            doc, counter_function=lsa_overlap, statistic_type="all"
        )
        doc._.semantic_cohesion_indices["SECLOSall"] = metrics.mean
        doc._.semantic_cohesion_indices["SECLOSalld"] = metrics.std

    def _get_lsa_overlap_adjacent_paragraphs(self, doc: Doc) -> None:
        """
        This method calculates the lsa overlap for adjacent paragraphs in the document.

        Parameters:
        doc(doc): The text to be anaylized.
        """

        if len(doc._.paragraphs) <= 1:
            doc._.semantic_cohesion_indices["SECLOPadj"] = 0
            doc._.semantic_cohesion_indices["SECLOPadjd"] = 0
            return

        lsa_overlap = lambda complete_text: [
            self._lsa_model.compute_similarity(prev, cur)
            for prev, cur in get_adjacent_paragraph_pairs(complete_text)
        ]

        metrics = get_mean_std_of_metric(
            doc, counter_function=lsa_overlap, statistic_type="all"
        )
        doc._.semantic_cohesion_indices["SECLOPadj"] = metrics.mean
        doc._.semantic_cohesion_indices["SECLOPadjd"] = metrics.std

    def _get_lsa_overlap_given_new_sentences(self, doc: Doc) -> None:
        """
        This method calculates the lsa overlap for new and given sentences.

        Parameters:
        doc(doc): The text to be anaylized.
        """

        if doc._.sentence_count <= 1:
            doc._.semantic_cohesion_indices["SECLOSgiv"] = 0
            doc._.semantic_cohesion_indices["SECLOSgivd"] = 0
            return

        lsa_overlap = lambda complete_text: [
            self._lsa_model.compute_similarity(new, given)
            for new, given in get_given_new_sentences(complete_text)
        ]

        metrics = get_mean_std_of_metric(
            doc, counter_function=lsa_overlap, statistic_type="all"
        )
        doc._.semantic_cohesion_indices["SECLOSgiv"] = metrics.mean
        doc._.semantic_cohesion_indices["SECLOSgivd"] = metrics.std


def get_given_new_sentences(doc: Doc) -> (Span, Span):
    """
    Iterator that returns all pairs of new sentences with its given sentences.

    Parameters:
    doc(Doc): The document to analyze.

    Yields:
    Tuple[Span, Span]: Pair of spans that represent a new sentence with its given sentences.
    """
    (cur,) = tee(doc.sents, 1)
    next(cur, None)
    for sent in cur:
        yield (sent, Span(doc, 0, sent.start))


def get_adjacent_paragraph_pairs(doc: Doc) -> (Span, Span):
    """
    Iterator that returns all pairs of adjacent sentences.

    Parameters:
    doc(Doc): The document to analyze.

    Yields:
    Tuple[Span, Span]: Pair of spans that represent two adjacent sentences.
    """
    paragraphs = doc._.paragraphs
    prev, cur = tee(paragraphs)
    next(cur, None)
    # Return each pair of sentences
    for prev, cur in zip(prev, cur):
        yield prev, cur
