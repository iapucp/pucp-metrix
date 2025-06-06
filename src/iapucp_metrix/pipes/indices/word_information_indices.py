from time import time

from spacy.language import Language
from spacy.tokens import Doc


class WordInformationIndices:
    """
    This class will handle all operations to obtain the word information indices of a text according to Coh-Metrix.
    """

    name = "word_information_indices"

    def __init__(self, nlp: Language) -> None:
        """
        The constructor will initialize this object that calculates the word information indices for a specific language of those that are available.

        Parameters:
        nlp(Language): The spacy model that corresponds to a language.

        Returns:
        None.
        """
        required_pipes = ["alphanumeric_word_identifier", "informative_word_tagger"]

        if not all((pipe in nlp.pipe_names for pipe in required_pipes)):
            message = (
                "Word information indices pipe need the following pipes: "
                + ", ".join(required_pipes)
            )
            raise AttributeError(message)

        self._nlp = nlp
        self._incidence = 1000
        Doc.set_extension("word_information_indices", default={}, force=True)

    def __call__(self, doc: Doc) -> Doc:
        """
        This method will calculate the word information indices

        Parameters:
        doc(Doc): A Spacy document.

        Returns:
        Doc: The spacy document analyzed.
        """
        if len(doc.text) == 0:
            raise ValueError("The text is empty.")

        start = time()
        doc._.word_information_indices["WRDCONT"] = self.__get_content_word_incidence(
            doc
        )
        doc._.word_information_indices["WRDCONTc"] = doc._.content_words_count
        doc._.word_information_indices["WRDNOUN"] = self.__get_noun_incidence(doc)
        doc._.word_information_indices["WRDNOUNc"] = doc._.nouns_count
        doc._.word_information_indices["WRDVERB"] = self.__get_verb_incidence(doc)
        doc._.word_information_indices["WRDVERBc"] = doc._.verbs_count
        doc._.word_information_indices["WRDADJ"] = self.__get_adjective_incidence(doc)
        doc._.word_information_indices["WRDADJc"] = doc._.adjectives_count
        doc._.word_information_indices["WRDADV"] = self.__get_adverb_incidence(doc)
        doc._.word_information_indices["WRDADVc"] = doc._.adverbs_count
        doc._.word_information_indices["WRDPRO"] = (
            self.__get_personal_pronoun_incidence(doc)
        )
        doc._.word_information_indices["WRDPROc"] = doc._.pronouns_count
        doc._.word_information_indices["WRDPRP1s"] = (
            self.__get_personal_pronoun_first_person_singular_form_incidence(doc)
        )
        doc._.word_information_indices["WRDPRP1sc"] = (
            doc._.pronouns_singular_first_person_count
        )
        doc._.word_information_indices["WRDPRP1p"] = (
            self.__get_personal_pronoun_first_person_plural_form_incidence(doc)
        )
        doc._.word_information_indices["WRDPRP1pc"] = (
            doc._.pronouns_plural_first_person_count
        )
        doc._.word_information_indices["WRDPRP2s"] = (
            self.__get_personal_pronoun_second_person_singular_form_incidence(doc)
        )
        doc._.word_information_indices["WRDPRP2sc"] = (
            doc._.pronouns_singular_second_person_count
        )
        doc._.word_information_indices["WRDPRP2p"] = (
            self.__get_personal_pronoun_second_person_plural_form_incidence(doc)
        )
        doc._.word_information_indices["WRDPRP2pc"] = (
            doc._.pronouns_plural_second_person_count
        )
        doc._.word_information_indices["WRDPRP3s"] = (
            self.__get_personal_pronoun_third_person_singular_form_incidence(doc)
        )
        doc._.word_information_indices["WRDPRP3sc"] = (
            doc._.pronouns_singular_third_person_count
        )
        doc._.word_information_indices["WRDPRP3p"] = (
            self.__get_personal_pronoun_third_person_plural_form_incidence(doc)
        )
        doc._.word_information_indices["WRDPRP3pc"] = (
            doc._.pronouns_plural_third_person_count
        )

        return doc

    def __get_content_word_incidence(self, doc: Doc) -> float:
        """
        This method calculates the incidence of content words in a text per {self._incidence} words.

        Parameters:
        doc(Doc): The text to be analyzed.

        Returns:
        float: The incidence of content words per {self._incidence} words.
        """
        return (doc._.content_words_count / doc._.alpha_words_count) * self._incidence

    def __get_noun_incidence(self, doc: Doc) -> float:
        """
        This method calculates the incidence of nouns in a text per {self._incidence} words.

        Parameters:
        doc(Doc): The text to be analyzed.

        Returns:
        float: The incidence of nouns per {self._incidence} words.
        """
        return (doc._.nouns_count / doc._.alpha_words_count) * self._incidence

    def __get_verb_incidence(self, doc: Doc) -> float:
        """
        This method calculates the incidence of verb in a text per {self._incidence} words.

        Parameters:
        doc(Doc): The text to be analyzed.

        Returns:
        float: The incidence of verb per {self._incidence} words.
        """
        return (doc._.verbs_count / doc._.alpha_words_count) * self._incidence

    def __get_adjective_incidence(self, doc: Doc) -> float:
        """
        This method calculates the incidence of adjective in a text per {self._incidence} words.

        Parameters:
        doc(Doc): The text to be analyzed.

        Returns:
        float: The incidence of adjective per {self._incidence} words.
        """
        return (doc._.adjectives_count / doc._.alpha_words_count) * self._incidence

    def __get_adverb_incidence(self, doc: Doc) -> float:
        """
        This method calculates the incidence of adverb in a text per {self._incidence} words.

        Parameters:
        doc(Doc): The text to be analyzed.

        Returns:
        float: The incidence of adverb per {self._incidence} words.
        """
        return (doc._.adverbs_count / doc._.alpha_words_count) * self._incidence

    def __get_personal_pronoun_incidence(self, doc: Doc) -> float:
        """
        This method calculates the incidence of personal pronouns in a text per {self._incidence} words.

        Parameters:
        doc(Doc): The text to be analyzed.

        Returns:
        float: The incidence of personal pronouns per {self._incidence} words.
        """
        return (doc._.pronouns_count / doc._.alpha_words_count) * self._incidence

    def __get_personal_pronoun_first_person_singular_form_incidence(
        self, doc: Doc
    ) -> float:
        """
        This method calculates the incidence of personal pronouns in first person and singular in a text per {self._incidence} words.

        Parameters:
        doc(Doc): The text to be analyzed.

        Returns:
        float: The incidence of personal pronouns in first person and singular per {self._incidence} words.
        """
        return (
            doc._.pronouns_singular_first_person_count / doc._.alpha_words_count
        ) * self._incidence

    def __get_personal_pronoun_first_person_plural_form_incidence(
        self, doc: Doc
    ) -> float:
        """
        This method calculates the incidence of personal pronouns in first person and plural in a text per {self._incidence} words.

        Parameters:
        doc(Doc): The text to be analyzed.

        Returns:
        float: The incidence of personal pronouns in first person and plural per {self._incidence} words.
        """
        return (
            doc._.pronouns_plural_first_person_count / doc._.alpha_words_count
        ) * self._incidence

    def __get_personal_pronoun_second_person_singular_form_incidence(
        self, doc: Doc
    ) -> float:
        """
        This method calculates the incidence of personal pronouns in second person and singular in a text per {self._incidence} words.

        Parameters:
        doc(Doc): The text to be analyzed.

        Returns:
        float: The incidence of personal pronouns in second person and singular per {self._incidence} words.
        """
        return (
            doc._.pronouns_singular_second_person_count / doc._.alpha_words_count
        ) * self._incidence

    def __get_personal_pronoun_second_person_plural_form_incidence(
        self, doc: Doc
    ) -> float:
        """
        This method calculates the incidence of personal pronouns in second person and plural in a text per {self._incidence} words.

        Parameters:
        doc(Doc): The text to be analyzed.

        Returns:
        float: The incidence of personal pronouns in second person and plural per {self._incidence} words.
        """
        return (
            doc._.pronouns_plural_second_person_count / doc._.alpha_words_count
        ) * self._incidence

    def __get_personal_pronoun_third_person_singular_form_incidence(
        self, doc: Doc
    ) -> float:
        """
        This method calculates the incidence of personal pronouns in third person and singular in a text per {self._incidence} words.

        Parameters:
        doc(Doc): The text to be analyzed.

        Returns:
        float: The incidence of personal pronouns in third person and singular per {self._incidence} words.
        """
        return (
            doc._.pronouns_singular_third_person_count / doc._.alpha_words_count
        ) * self._incidence

    def __get_personal_pronoun_third_person_plural_form_incidence(
        self, doc: Doc
    ) -> float:
        """
        This method calculates the incidence of personal pronouns in third person and plural in a text per {self._incidence} words.

        Parameters:
        doc(Doc): The text to be analyzed.

        Returns:
        float: The incidence of personal pronouns in third person and plural per {self._incidence} words.
        """
        return (
            doc._.pronouns_plural_third_person_count / doc._.alpha_words_count
        ) * self._incidence
