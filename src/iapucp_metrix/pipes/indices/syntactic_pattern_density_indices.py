from time import time

from spacy.language import Language
from spacy.tokens import Doc


class SyntacticPatternDensityIndices:
    """
    This class will handle all operations to find the synthactic pattern density indices of a text according to Coh-Metrix.
    """

    name = "syntactic_pattern_density_indices"

    def __init__(self, nlp: Language) -> None:
        """
        The constructor will initialize this object that calculates the synthactic pattern density indices for a specific language of those that are available.

        Parameters:
        nlp: The spacy model that corresponds to a language.

        Returns:
        None.
        """
        required_pipes = [
            "negative_expression_tagger",
            "noun_phrase_tagger",
            "alphanumeric_word_identifier",
        ]
        if not all((pipe in nlp.pipe_names for pipe in required_pipes)):
            message = (
                "Syntatic pattern density indices pipe need the following pipes: "
                + ", ".join(required_pipes)
            )
            raise AttributeError(message)

        self._nlp = nlp
        self._incidence = 1000
        Doc.set_extension("syntactic_pattern_density_indices", default={}, force=True)

    def __call__(self, doc: Doc) -> Doc:
        """
        This method calculates the syntatic pattern density indices.

        Parameters:
        doc(Doc): A Spacy document.

        Reeturns:
        Doc: The spacy document that was analyzed
        """
        if len(doc.text) == 0:
            raise ValueError("The text is empty.")

        start = time()
        doc._.syntactic_pattern_density_indices["DRNP"] = (
            self.__get_noun_phrase_density(doc)
        )
        doc._.syntactic_pattern_density_indices["DRNPc"] = doc._.noun_phrases_count
        doc._.syntactic_pattern_density_indices["DRVP"] = (
            self.__get_verb_phrase_density(doc)
        )
        doc._.syntactic_pattern_density_indices["DRVPc"] = doc._.verb_phrases_count
        doc._.syntactic_pattern_density_indices["DRNEG"] = (
            self.__get_negation_expressions_density(doc)
        )
        doc._.syntactic_pattern_density_indices["DRNEGc"] = (
            doc._.negative_expressions_count
        )
        doc._.syntactic_pattern_density_indices["DRGER"] = (
            self.__get_gerund_forms_density(doc)
        )
        doc._.syntactic_pattern_density_indices["DRGERc"] = doc._.gerunds_count
        doc._.syntactic_pattern_density_indices["DRINF"] = (
            self.__get_infinitive_forms_density(doc)
        )
        doc._.syntactic_pattern_density_indices["DRINFc"] = doc._.infinitives_count
        doc._.syntactic_pattern_density_indices["DRCCONJ"] = (
            self.__get_coordinating_conjunctions_density(doc)
        )
        doc._.syntactic_pattern_density_indices["DRCCONJc"] = (
            doc._.coordinating_conjunctions_count
        )
        doc._.syntactic_pattern_density_indices["DRSCONJ"] = (
            self.__get_subordinating_conjunctions_density(doc)
        )
        doc._.syntactic_pattern_density_indices["DRSCONJc"] = (
            doc._.subordinating_conjunctions_count
        )

        return doc

    def __get_noun_phrase_density(self, doc: Doc) -> float:
        """
        This function obtains the incidence of noun phrases that exist on a text per {self._incidence} words.

        Parameters:
        doc(Doc): The text to be analized.

        Returns:
        float: The incidence of noun phrases per {self._incidence} words.
        """
        return (doc._.noun_phrases_count / doc._.alpha_words_count) * self._incidence

    def __get_verb_phrase_density(self, doc: Doc) -> float:
        """
        This function obtains the incidence of verb phrases that exist on a text per {self._incidence} words.

        Parameters:
        doc(Doc): The text to be analized.

        Returns:
        float: The incidence of verb phrases per {self._incidence} words.
        """
        return (doc._.verb_phrases_count / doc._.alpha_words_count) * self._incidence

    def __get_negation_expressions_density(self, doc: Doc) -> float:
        """
        This function obtains the incidence of negation expressions that exist on a text per {self._incidence} words.

        Parameters:
        doc(Doc): The text to be analized.

        Returns:
        float: The incidence of negation expressions per {self._incidence} words.
        """
        return (
            doc._.negative_expressions_count / doc._.alpha_words_count
        ) * self._incidence

    def __get_gerund_forms_density(self, doc: Doc) -> float:
        """
        This function obtains the incidence of verbs in gerund form that exist on a text per {self._incidence} words.

        Parameters:
        doc(Doc): The text to be analized.

        Returns:
        float: The incidence of verbs in gerund form per {self._incidence} words.
        """
        return (doc._.gerunds_count / doc._.alpha_words_count) * self._incidence

    def __get_infinitive_forms_density(self, doc: Doc) -> float:
        """
        This function obtains the incidence of verbs in infinitive form that exist on a text per {self._incidence} words.

        Parameters:
        doc(Doc): The text to be analized.

        Returns:
        float: The incidence of verbs in infinitive form per {self._incidence} words.
        """
        return (doc._.infinitives_count / doc._.alpha_words_count) * self._incidence

    def __get_coordinating_conjunctions_density(self, doc: Doc) -> float:
        """
        This function obtains the incidence of coordinating conjunctions that exist on a text per {self._incidence} words.

        Parameters:
        doc(Doc): The text to be analized.

        Returns:
        float: The incidence of coordinating conjunctions per {self._incidence} words.
        """
        num_conjunctions = (
            doc._.coordinating_conjunctions_count
            + doc._.subordinating_conjunctions_count
        )
        return (
            0
            if num_conjunctions == 0
            else (doc._.coordinating_conjunctions_count / num_conjunctions)
            * self._incidence
        )

    def __get_subordinating_conjunctions_density(self, doc: Doc) -> float:
        """
        This function obtains the incidence of subordinating conjunctions that exist on a text per {self._incidence} words.

        Parameters:
        doc(Doc): The text to be analized.

        Returns:
        float: The incidence of subordinating conjunctions per {self._incidence} words.
        """
        num_conjunctions = (
            doc._.coordinating_conjunctions_count
            + doc._.subordinating_conjunctions_count
        )
        return (
            0
            if num_conjunctions == 0
            else (doc._.subordinating_conjunctions_count / num_conjunctions)
            * self._incidence
        )
