import math
from collections import Counter
from math import sqrt
from time import time

from spacy.language import Language
from spacy.tokens import Doc


class ReadabilityIndices:
    """
    This pipe will handle all operations to find the readability indices of a text according to Coh-Metrix. It needs the descriptive indices pipe to be added before it.
    """

    name = "readability_indices"

    def __init__(self, nlp: Language) -> None:
        """
        The constructor will initialize this object that calculates the readability indices for a specific language of those that are available.

        Parameters:
        nlp(Language): The spacy model that corresponds to a language.

        Returns:
        None.
        """
        required_pipes = ["descriptive_indices"]
        if not all((pipe in nlp.pipe_names for pipe in required_pipes)):
            message = (
                "Readability diversity indices pipe need the following pipes: "
                + ", ".join(required_pipes)
            )
            raise AttributeError(message)

        self._nlp = nlp
        Doc.set_extension("readability_indices", default={})

    def __call__(self, doc: Doc) -> Doc:
        """
        This method will calculate the readability indices.

        Parameters:
        doc(Doc): A Spacy document.

        Returns:
        Doc: The processed doc.
        """
        if len(doc.text) == 0:
            raise ValueError("The text is empty.")

        start = time()

        doc._.readability_indices["RDFHGL"] = (
            self.__calculate_fernandez_huertas_grade_level(doc)
        )
        doc._.readability_indices["RDSPP"] = (
            self.__calculate_szigriszt_pazos_perspicuity(doc)
        )
        doc._.readability_indices["RDMU"] = self.__calculate_readability_mu(doc)
        doc._.readability_indices["RDSMOG"] = self.__calculate_smog(doc)
        doc._.readability_indices["RDFOG"] = self.__calculate_gunning_fog(doc)
        doc._.readability_indices["RDHS"] = self.__calculate_honore_statistic(doc)
        doc._.readability_indices["RDBR"] = self.__calculate_brunet_index(doc)

        return doc

    def __calculate_fernandez_huertas_grade_level(self, doc: Doc) -> float:
        """
        This function obtains the Fernández-Huertas readability index for a text.

        Parameters:
        doc(Doc): The text to be analized.

        Returns:
        float: The Fernández-Huertas readability index for a text.
        """
        return (
            206.84
            - 0.6 * doc._.descriptive_indices["DESWLsy"]
            - 1.02 * doc._.descriptive_indices["DESSL"]
        )

    def __calculate_szigriszt_pazos_perspicuity(self, doc: Doc) -> float:
        """
        This function obtains the Szigriszt-Pazos Perspicuity index for a text.

        Parameters:
        doc(Doc): The text to be analized.

        Returns:
        float: The Szigriszt-Pazos Perspicuity index for a text.
        """
        syllable_count = doc._.syllable_count
        sentence_count = doc._.sentence_count
        words_count = doc._.alpha_words_count

        return (
            (
                206.835
                - 62.3 * syllable_count / words_count
                - words_count / sentence_count
            )
            if words_count > 0
            else 0
        )

    def __calculate_brunet_index(self, doc: Doc) -> float:
        """
        This function obtains the Brunet index for a text.

        Parameters:
        doc(Doc): The text to be analized.

        Returns:
        float: The Brunet index for a text.
        """
        words_count = doc._.alpha_words_count
        unique_words_count = doc._.alpha_words_different_count

        return (
            words_count ** (unique_words_count**-0.165) if unique_words_count > 0 else 0
        )

    def __calculate_honore_statistic(self, doc: Doc) -> float:
        """
        This function obtains the Honore's Statistic for a text.

        Parameters:
        doc(Doc): The text to be analized.

        Returns:
        float: The Honore's Statistic for a text.
        """
        words_count = doc._.alpha_words_count
        unique_words_count = doc._.alpha_words_different_count

        freqs = Counter(doc._.alpha_words_different)
        hapaxes_legomena = [word for word, freq in freqs.items() if freq == 1]

        return (
            0
            if unique_words_count == 0 or len(hapaxes_legomena) == unique_words_count
            else (
                100
                * (math.log10(words_count))
                / (1 - (len(hapaxes_legomena) / unique_words_count))
            )
        )

    def __calculate_readability_mu(self, doc: Doc) -> float:
        """
        This function obtains the Readability µ index for a text.

        Parameters:
        doc(Doc): The text to be analized.

        Returns:
        float: The Readability µ index for a text.
        """
        words_count = doc._.alpha_words_count
        letters_mean = doc._.descriptive_indices["DESWLlt"]
        letters_std = doc._.descriptive_indices["DESWLltd"]

        return (
            (words_count / (words_count - 1)) * (letters_mean / (letters_std**2))
            if (words_count > 1 and letters_std > 0)
            else 0
        )

    def __calculate_smog(self, doc: Doc) -> float:
        """
        This function obtains the SMOG index for a text.

        Parameters:
        doc(Doc): The text to be analized.

        Returns:
        float: The SMOG index for a text.
        """
        sentence_count = doc._.sentence_count
        polysyllabic_count = doc._.polysyllabic_words_count

        return 1.0430 * sqrt(30 * polysyllabic_count / sentence_count) + 3.1291

    def __calculate_gunning_fog(self, doc: Doc) -> float:
        """
        This function obtains the Gunning Fog index for a text.

        Parameters:
        doc(Doc): The text to be analized.

        Returns:
        float: The Gunning Fog index for a text.
        """
        words_count = doc._.alpha_words_count
        sentence_count = doc._.sentence_count
        polysyllabic_count = doc._.polysyllabic_words_count

        return (
            0.4
            * (
                (words_count / sentence_count)
                + 100 * (polysyllabic_count / words_count)
            )
            if words_count > 0
            else 0
        )
