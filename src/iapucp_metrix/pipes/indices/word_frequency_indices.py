import statistics
from time import time

from spacy.language import Language
from spacy.tokens import Doc
from wordfreq import zipf_frequency


class WordFrequencyIndices:
    """
    This class will handle all operations to obtain the word frequency indices of a text according to Pucp-Metrix
    """

    name = "word_frequency_indices"

    def __init__(self, nlp: Language) -> None:
        """
        The constructor will initialize this object that calculates the word frequency indices for a specific language of those that are available.

        Parameters:
        nlp(Language): The spacy model that corresponds to a language.

        Returns:
        None.
        """
        required_pipes = ["sentencizer"]
        if not all((pipe in nlp.pipe_names for pipe in required_pipes)):
            message = (
                "Referential cohesion indices pipe need the following pipes: "
                + ", ".join(required_pipes)
            )
            raise AttributeError(message)

        self._nlp = nlp
        self._incidence = 1000
        self._rare_word_frequency = 4

        Doc.set_extension("word_frequency_indices", default={}, force=True)

    def __call__(self, doc: Doc) -> Doc:
        """
        This method will calculate the word frequency indices.

        Parameters:
        doc(Doc): A Spacy document.

        Returns:
        Doc: The spacy document analyzed
        """
        if len(doc.text) == 0:
            raise ValueError("The text is empty.")

        start = time()
        (
            doc._.word_frequency_indices["WFRCno"],
            doc._.word_frequency_indices["WFRCnoi"],
        ) = self.__get_rare_nouns_count(doc)
        (
            doc._.word_frequency_indices["WFRCvb"],
            doc._.word_frequency_indices["WFRCvbi"],
        ) = self.__get_rare_verbs_count(doc)
        (
            doc._.word_frequency_indices["WFRCadj"],
            doc._.word_frequency_indices["WFRCadji"],
        ) = self.__get_rare_adjectives_count(doc)
        (
            doc._.word_frequency_indices["WFRCadv"],
            doc._.word_frequency_indices["WFRCadvi"],
        ) = self.__get_rare_adverbs_count(doc)
        (
            doc._.word_frequency_indices["WFRCcw"],
            doc._.word_frequency_indices["WFRCcwi"],
        ) = self.__get_rare_content_words_count(doc)
        (
            doc._.word_frequency_indices["WFRCcwd"],
            doc._.word_frequency_indices["WFRCcwdi"],
        ) = self.__get_distinct_rare_content_words_count(doc)
        doc._.word_frequency_indices["WFMcw"] = (
            self.__get_mean_of_content_words_frequency(doc)
        )
        doc._.word_frequency_indices["WFMw"] = self.__get_mean_of_words_frequency(doc)
        doc._.word_frequency_indices["WFMrw"] = (
            self.__get_mean_of_rarest_words_frequency_per_sentence(doc)
        )
        doc._.word_frequency_indices["WFMrcw"] = (
            self.__get_mean_of_rarest_content_words_frequency_per_sentence(doc)
        )

        return doc

    def __get_rare_nouns_count(self, doc: Doc) -> (float, float):
        """
        This method returns the number of rare nouns and its incidence per {self._incidence} words.

        Parameters:
        doc(Doc): The text to be analyzed.

        Returns:
        (float, float): The number of rare nouns and its incidence per {self._incidence} words.
        """
        num_rare_nouns = 0
        for word in doc._.nouns:
            freq = zipf_frequency(word.text.lower(), "es")
            if freq <= self._rare_word_frequency:
                num_rare_nouns += 1

        return (
            num_rare_nouns,
            (num_rare_nouns / doc._.alpha_words_count) * self._incidence,
        )

    def __get_rare_verbs_count(self, doc: Doc) -> (float, float):
        """
        This method returns the number of rare verbs and its incidence per {self._incidence} words.

        Parameters:
        doc(Doc): The text to be analyzed.

        Returns:
        (float, float): The number of rare verbs and its incidence per {self._incidence} words.
        """
        num_rare_verbs = 0
        for word in doc._.verbs:
            freq = zipf_frequency(word.text.lower(), "es")
            if freq <= self._rare_word_frequency:
                num_rare_verbs += 1

        return (
            num_rare_verbs,
            (num_rare_verbs / doc._.alpha_words_count) * self._incidence,
        )

    def __get_rare_adjectives_count(self, doc: Doc) -> (float, float):
        """
        This method returns the number of rare adjectives and its incidence per {self._incidence} words.

        Parameters:
        doc(Doc): The text to be analyzed.

        Returns:
        (float, float): The number of rare adjectives and its incidence per {self._incidence} words.
        """
        num_rare_adjectives = 0
        for word in doc._.adjectives:
            freq = zipf_frequency(word.text.lower(), "es")
            if freq <= self._rare_word_frequency:
                num_rare_adjectives += 1

        return (
            num_rare_adjectives,
            (num_rare_adjectives / doc._.alpha_words_count) * self._incidence,
        )

    def __get_rare_adverbs_count(self, doc: Doc) -> (float, float):
        """
        This method returns the number of rare adverbs and its incidence per {self._incidence} words.

        Parameters:
        doc(Doc): The text to be analyzed.

        Returns:
        (float, float): The number of rare adverbs and its incidence per {self._incidence} words.
        """
        num_rare_adverbs = 0
        for word in doc._.adverbs:
            freq = zipf_frequency(word.text.lower(), "es")
            if freq <= self._rare_word_frequency:
                num_rare_adverbs += 1

        return (
            num_rare_adverbs,
            (num_rare_adverbs / doc._.alpha_words_count) * self._incidence,
        )

    def __get_rare_content_words_count(self, doc: Doc) -> (float, float):
        """
        This method returns the number of rare content_words and its incidence per {self._incidence} words.

        Parameters:
        doc(Doc): The text to be analyzed.

        Returns:
        (float, float): The number of rare content_words and its incidence per {self._incidence} words.
        """
        num_rare_content_words = 0
        for word in doc._.content_words:
            freq = zipf_frequency(word.text.lower(), "es")
            if freq <= self._rare_word_frequency:
                num_rare_content_words += 1

        return (
            num_rare_content_words,
            (num_rare_content_words / doc._.alpha_words_count) * self._incidence,
        )

    def __get_distinct_rare_content_words_count(self, doc: Doc) -> (float, float):
        """
        This method returns the number of distinct rare content words and its incidence per {self._incidence} words.

        Parameters:
        doc(Doc): The text to be analyzed.

        Returns:
        (float, float): The number of distinct rare content words and its incidence per {self._incidence} words.
        """
        num_rare_content_words = 0
        for word in doc._.content_words_different:
            freq = zipf_frequency(word.lower(), "es")
            if freq <= self._rare_word_frequency:
                num_rare_content_words += 1

        return (
            num_rare_content_words,
            (num_rare_content_words / doc._.alpha_words_count) * self._incidence,
        )

    def __get_mean_of_content_words_frequency(self, doc: Doc) -> float:
        """
        This method returns the average frequency of content words.

        Parameters:
        doc(Doc): The text to be analyzed.

        Returns:
        float: The average frequency of content words.
        """

        return (
            statistics.mean(
                [
                    zipf_frequency(word.text.lower(), "es")
                    for word in doc._.content_words
                ]
            )
            if doc._.content_words_count > 0
            else 0
        )

    def __get_mean_of_words_frequency(self, doc: Doc) -> float:
        """
        This method returns the average frequency words.

        Parameters:
        doc(Doc): The text to be analyzed.

        Returns:
        float: The average frequency of content words.
        """

        return statistics.mean(
            [zipf_frequency(word.text.lower(), "es") for word in doc._.alpha_words]
        )

    def __get_mean_of_rarest_content_words_frequency_per_sentence(
        self, doc: Doc
    ) -> float:
        """
        This method returns the average frequency of the rarest content words per sentence.

        Parameters:
        doc(Doc): The text to be analyzed.

        Returns:
        float: The average frequency of the rarest content words per sentence.
        """

        min_freqs = []
        for sent in doc._.non_empty_sentences:
            freqs = [
                zipf_frequency(word.text.lower(), "es")
                for word in sent._.content_words
                if sent._.content_words_count > 0
            ]
            if len(freqs) > 0:
                min_freqs.append(min(freqs))

        return min(min_freqs) / len(min_freqs) if len(min_freqs) > 0 else 0

    def __get_mean_of_rarest_words_frequency_per_sentence(self, doc: Doc) -> float:
        """
        This method returns the average frequency of the rarest words per sentence.

        Parameters:
        doc(Doc): The text to be analyzed.

        Returns:
        float: The average frequency of the rarest words per sentence.
        """

        min_freqs = []
        for sent in doc._.non_empty_sentences:
            freqs = [
                zipf_frequency(word.text.lower(), "es")
                for word in sent._.alpha_words
                if sent._.alpha_words_count > 0
            ]
            if len(freqs) > 0:
                min_freqs.append(min(freqs))

        return min(min_freqs) / len(min_freqs) if len(min_freqs) > 0 else 0
