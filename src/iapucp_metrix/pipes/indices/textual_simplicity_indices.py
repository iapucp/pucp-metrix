from time import time

from spacy.language import Language
from spacy.tokens import Doc


class TextualSimplicityIndices:
    """
    This class will handle all operations to obtain the textual simplicity indices of a text according to Coh-Metrix
    """

    def __init__(self, nlp: Language) -> None:
        """
        The constructor will initialize the extensions where to hold the textual simplicity indices of a doc. It needs the following pipes to be added before it: 'alphanumeric_word_identifier', 'paragraphizer', 'syllablelizer'

        Parameters:
        nlp(Lanuage): The spacy model that corresponds to a language.
        language(str): The language that the texts to process will have.

        Returns:
        None.
        """
        required_pipes = [
            "alphanumeric_word_identifier",
            "paragraphizer",
        ]
        if not all((pipe in nlp.pipe_names for pipe in required_pipes)):
            message = (
                "TextualSimplicity indices pipe need the following pipes: "
                + ", ".join(required_pipes)
            )
            raise AttributeError(message)

        self._nlp = nlp
        self.short_threshold = 11
        self.medium_threshold = 13
        self.long_threshold = 15

        Doc.set_extension("textual_simplicity_indices", default=dict())  # Dictionary

    def __call__(self, doc: Doc) -> Doc:
        """
        This method will calculate the textual simplicity indices.

        Parameters:
        doc(Doc): A Spacy document.

        Returns:
        Doc: The processed doc.
        """
        if len(doc.text) == 0:
            raise ValueError("The text is empty.")

        start = time()
        self.__get_sentences_length_ratio(doc)
        return doc

    def __get_sentences_length_ratio(self, doc: Doc) -> None:
        """
        This method calculates the ratio of sentences that are short, medium, long and very long.

        Parameters:
        doc(Doc): The text to be anaylized.
        """

        short_sentences = 0
        medium_sentences = 0
        long_sentences = 0
        very_long_sentences = 0
        sentence_count = doc._.sentence_count
        for sentence in doc._.non_empty_sentences:
            sentence_length = sentence._.alpha_words_count
            if sentence_length < self.short_threshold:
                short_sentences += 1
            elif sentence_length < self.medium_threshold:
                medium_sentences += 1
            elif sentence_length < self.long_threshold:
                long_sentences += 1
            else:
                very_long_sentences += 1

        doc._.textual_simplicity_indices["TSSRsh"] = short_sentences / sentence_count
        doc._.textual_simplicity_indices["TSSRmd"] = medium_sentences / sentence_count
        doc._.textual_simplicity_indices["TSSRlg"] = long_sentences / sentence_count
        doc._.textual_simplicity_indices["TSSRxl"] = (
            very_long_sentences / sentence_count
        )
