from time import time

from spacy.language import Language
from spacy.tokens import Doc


class ConnectiveIndices:
    """
    This class will handle all operations to obtain the connective indices of a text according to Coh-Metrix
    """

    name = "connective_indices"

    def __init__(self, nlp: Language) -> None:
        """
        The constructor will initialize this object that calculates the connective indices for a specific language of those that are available.

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

        Doc.set_extension("connective_indices", default={}, force=True)

    def __call__(self, doc: Doc) -> Doc:
        """
        This method will calculate the connective indices.

        Parameters:
        doc(Doc): A Spacy document.

        Returns:
        Doc: The spacy document analyzed
        """
        if len(doc.text) == 0:
            raise ValueError("The text is empty.")

        doc._.connective_indices["CNCAll"] = self.__get_all_connectives_incidence(doc)
        doc._.connective_indices["CNCCaus"] = self.__get_causal_connectives_incidence(
            doc
        )
        doc._.connective_indices["CNCLogic"] = self.__get_logical_connectives_incidence(
            doc
        )
        doc._.connective_indices["CNCADC"] = (
            self.__get_adversative_connectives_incidence(doc)
        )
        doc._.connective_indices["CNCTemp"] = self.__get_temporal_connectives_incidence(
            doc
        )
        doc._.connective_indices["CNCAdd"] = self.__get_additive_connectives_incidence(
            doc
        )

        return doc

    def __get_causal_connectives_incidence(self, doc: Doc) -> float:
        """
        This method returns the incidence per {self._incidence} words for causal connectives.

        Parameters:
        doc(Doc): The text to be analyzed.

        Returns:
        float: The incidence of causal connectives per {self._incidence} words.
        """
        return (
            doc._.causal_connectives_count / doc._.alpha_words_count
        ) * self._incidence

    def __get_logical_connectives_incidence(self, doc: Doc) -> float:
        """
        This method returns the incidence per {self._incidence} words for logical connectives.

        Parameters:
        doc(Doc): The text to be analyzed.

        Returns:
        float: The incidence of logical connectives per {self._incidence} words.
        """
        return (
            doc._.logical_connectives_count / doc._.alpha_words_count
        ) * self._incidence

    def __get_adversative_connectives_incidence(self, doc: Doc) -> float:
        """
        This method returns the incidence per {self._incidence} words for adversative connectives.

        Parameters:
        doc(Doc): The text to be analyzed.

        Returns:
        float: The incidence of adversative connectives per {self._incidence} words.
        """
        return (
            doc._.adversative_connectives_count / doc._.alpha_words_count
        ) * self._incidence

    def __get_temporal_connectives_incidence(self, doc: Doc) -> float:
        """
        This method returns the incidence per {self._incidence} words for temporal connectives.

        Parameters:
        doc(Doc): The text to be analyzed.

        Returns:
        float: The incidence of temporal connectives per {self._incidence} words.
        """
        return (
            doc._.temporal_connectives_count / doc._.alpha_words_count
        ) * self._incidence

    def __get_additive_connectives_incidence(self, doc: Doc) -> float:
        """
        This method returns the incidence per {self._incidence} words for additive connectives.

        Parameters:
        doc(Doc): The text to be analyzed.

        Returns:
        float: The incidence of additive connectives per {self._incidence} words.
        """
        return (
            doc._.additive_connectives_count / doc._.alpha_words_count
        ) * self._incidence

    def __get_all_connectives_incidence(self, doc: Doc) -> float:
        """
        This method returns the incidence per {self._incidence} words for all connectives.

        Parameters:
        doc(Doc): The text to be analyzed.

        Returns:
        float: The incidence of all connectives per {self._incidence} words.
        """
        return (
            (
                doc._.causal_connectives_count
                + doc._.logical_connectives_count
                + doc._.adversative_connectives_count
                + doc._.temporal_connectives_count
                + doc._.additive_connectives_count
            )
            / doc._.alpha_words_count
        ) * self._incidence
