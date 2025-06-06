import statistics
from time import time
from typing import Callable

from spacy.language import Language
from spacy.tokens import Doc

from iapucp_metrix.utils.statistics_results import StatisticsResults


class DescriptiveIndices:
    """
    This class will handle all operations to obtain the descriptive indices of a text according to Coh-Metrix
    """

    def __init__(self, nlp: Language) -> None:
        """
        The constructor will initialize the extensions where to hold the descriptive indices of a doc. It needs the following pipes to be added before it: 'alphanumeric_word_identifier', 'paragraphizer', 'syllablelizer'

        Parameters:
        nlp(Lanuage): The spacy model that corresponds to a language.
        language(str): The language that the texts to process will have.

        Returns:
        None.
        """
        required_pipes = [
            "alphanumeric_word_identifier",
            "paragraphizer",
            "syllablelizer",
        ]
        if not all((pipe in nlp.pipe_names for pipe in required_pipes)):
            message = "Descriptive indices pipe need the following pipes: " + ", ".join(
                required_pipes
            )
            raise AttributeError(message)

        self._nlp = nlp
        self._incidence = 1000
        Doc.set_extension("descriptive_indices", default=dict(), force=True)  # Dictionary

    def __call__(self, doc: Doc) -> Doc:
        """
        This method will calculate the descriptive indices.

        Parameters:
        doc(Doc): A Spacy document.

        Returns:
        Doc: The processed doc.
        """
        if len(doc.text) == 0:
            raise ValueError("The text is empty.")

        start = time()

        doc._.descriptive_indices["DESPC"] = doc._.paragraph_count
        doc._.descriptive_indices["DESPCi"] = (
            self._incidence * (doc._.paragraph_count / doc._.alpha_words_count)
            if doc._.alpha_words_count > 0
            else 0
        )
        doc._.descriptive_indices["DESSC"] = doc._.sentence_count
        doc._.descriptive_indices["DESSCi"] = (
            self._incidence * (doc._.sentence_count / doc._.alpha_words_count)
            if doc._.alpha_words_count > 0
            else 0
        )
        doc._.descriptive_indices["DESWC"] = doc._.alpha_words_count
        doc._.descriptive_indices["DESWCU"] = doc._.alpha_words_different_count
        doc._.descriptive_indices["DESWCUi"] = (
            self._incidence
            * (doc._.alpha_words_different_count / doc._.alpha_words_count)
            if doc._.alpha_words_count > 0
            else 0
        )
        self.__get_length_of_paragraphs(doc)
        self.__get_length_of_sentences(doc)
        self.__get_length_of_sentences_no_stopwords(doc)
        self.__get_max_min_length_of_sentences(doc)
        self.__get_syllables_per_word(doc)
        self.__get_syllables_per_content_word(doc)
        self.__get_length_of_content_words(doc)
        self.__get_length_of_words(doc)
        self.__get_length_of_words_no_stopwords(doc)
        self.__get_length_of_lemmas(doc)

        return doc

    def _get_mean_std_of_metric(
        self, doc: Doc, counter_function: Callable, statistic_type: str = "all"
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

    def __get_length_of_paragraphs(self, doc: Doc) -> None:
        """
        This method calculates the average amount and standard deviation of sentences in each paragraph.

        Parameters:
        doc(doc): The text to be anaylized.
        """

        count_length_of_paragraphs = lambda complete_text: [
            para._.sentence_count for para in complete_text._.paragraphs
        ]
        metrics = self._get_mean_std_of_metric(
            doc, counter_function=count_length_of_paragraphs, statistic_type="all"
        )
        doc._.descriptive_indices["DESPL"] = metrics.mean
        doc._.descriptive_indices["DESPLd"] = metrics.std

    def __get_length_of_sentences(self, doc: Doc) -> None:
        """
        This method calculate the average amount and standard deviation of words in each sentence.

        Parameters:
        doc(Doc): The text to be anaylized.
        """
        count_length_of_sentences = lambda complete_text: [
            sentence._.alpha_words_count
            for sentence in complete_text._.non_empty_sentences
        ]

        metrics = self._get_mean_std_of_metric(
            doc, counter_function=count_length_of_sentences, statistic_type="all"
        )
        doc._.descriptive_indices["DESSL"] = metrics.mean
        doc._.descriptive_indices["DESSLd"] = metrics.std

    def __get_length_of_sentences_no_stopwords(self, doc: Doc) -> None:
        """
        This method calculate the average amount and standard deviation of words in each sentence, excluding stopwords.

        Parameters:
        doc(Doc): The text to be anaylized.
        """
        count_length_of_sentences = lambda complete_text: [
            len([token for token in sentence._.alpha_words if not token.is_stop])
            for sentence in complete_text._.non_empty_sentences
        ]

        metrics = self._get_mean_std_of_metric(
            doc, counter_function=count_length_of_sentences, statistic_type="all"
        )
        doc._.descriptive_indices["DESSNSL"] = metrics.mean
        doc._.descriptive_indices["DESSNSLd"] = metrics.std

    def __get_length_of_content_words(self, doc: Doc) -> None:
        """
        This method calculates the average amount and standard deviation of letters in each content word.

        Parameters:
        doc(Doc): The text to be anaylized.
        """
        count_letters_per_word = lambda complete_text: [
            len(token) for token in complete_text._.content_words
        ]

        metrics = self._get_mean_std_of_metric(
            doc, counter_function=count_letters_per_word, statistic_type="all"
        )
        doc._.descriptive_indices["DESCWLlt"] = metrics.mean
        doc._.descriptive_indices["DESCWLltd"] = metrics.std

    def __get_length_of_words(self, doc: Doc) -> None:
        """
        This method calculates the average amount and standard deviation of letters in each word.

        Parameters:
        doc(Doc): The text to be anaylized.
        """
        count_letters_per_word = lambda complete_text: [
            len(token) for token in complete_text._.alpha_words
        ]

        metrics = self._get_mean_std_of_metric(
            doc, counter_function=count_letters_per_word, statistic_type="all"
        )
        doc._.descriptive_indices["DESWLlt"] = metrics.mean
        doc._.descriptive_indices["DESWLltd"] = metrics.std

    def __get_length_of_words_no_stopwords(self, doc: Doc) -> None:
        """
        This method calculates the average amount and standard deviation of letters in each word, excluding stopwords.

        Parameters:
        doc(Doc): The text to be anaylized.
        """
        count_letters_per_word = lambda complete_text: [
            len(token) for token in complete_text._.alpha_words if not token.is_stop
        ]

        metrics = self._get_mean_std_of_metric(
            doc, counter_function=count_letters_per_word, statistic_type="all"
        )
        doc._.descriptive_indices["DESWNSLlt"] = metrics.mean
        doc._.descriptive_indices["DESWNSLltd"] = metrics.std

    def __get_length_of_lemmas(self, doc: Doc) -> None:
        """
        This method calculates the average amount and standard deviation of letters in each lemma.

        Parameters:
        doc(Doc): The text to be anaylized.
        """
        count_letters_per_lemma = lambda complete_text: [
            len(token.lemma_) for token in complete_text._.alpha_words
        ]

        metrics = self._get_mean_std_of_metric(
            doc, counter_function=count_letters_per_lemma, statistic_type="all"
        )
        doc._.descriptive_indices["DESLLlt"] = metrics.mean
        doc._.descriptive_indices["DESLLltd"] = metrics.std

    def __get_max_min_length_of_sentences(self, doc: Doc) -> None:
        """
        This method calculates the maximum and minimum amount of words in each sentence.

        Parameters:
        doc(Doc): The text to be anaylized.
        """
        sentences = [
            len(sentence._.alpha_words) for sentence in doc._.non_empty_sentences
        ]

        doc._.descriptive_indices["DESSLmax"] = (
            max(sentences) if len(sentences) > 0 else 0
        )
        doc._.descriptive_indices["DESSLmin"] = (
            min(sentences) if len(sentences) > 0 else 0
        )

    def __get_syllables_per_word(self, doc: Doc) -> StatisticsResults:
        """
        This method calculates the average amount and standard deviation of syllables in each word.

        Parameters:
        doc(Doc): The text to be anaylized.

        Returns:
        None
        """
        count_syllables_per_word = lambda doc: [
            token._.syllable_count
            for token in doc._.alpha_words
            if token._.syllables is not None
        ]

        metrics = self._get_mean_std_of_metric(
            doc, counter_function=count_syllables_per_word, statistic_type="all"
        )
        doc._.descriptive_indices["DESWLsy"] = metrics.mean
        doc._.descriptive_indices["DESWLsyd"] = metrics.std

    def __get_syllables_per_content_word(self, doc: Doc) -> StatisticsResults:
        """
        This method calculates the average amount and standard deviation of syllables in each content word.

        Parameters:
        doc(Doc): The text to be anaylized.

        Returns:
        None
        """
        count_syllables_per_word = lambda doc: [
            token._.syllable_count
            for token in doc._.content_words
            if token._.syllables is not None
        ]

        metrics = self._get_mean_std_of_metric(
            doc, counter_function=count_syllables_per_word, statistic_type="all"
        )
        doc._.descriptive_indices["DESCWLsy"] = metrics.mean
        doc._.descriptive_indices["DESCWLsyd"] = metrics.std
