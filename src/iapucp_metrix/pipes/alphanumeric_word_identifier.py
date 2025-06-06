from typing import Iterator

from spacy.language import Language
from spacy.tokens import Doc, Span

from iapucp_metrix.utils.utils import is_word


def doc_alpha_words_getter(doc: Doc) -> Iterator:
    """
    Function that gets the alphabetic words for the entire text.}

    Parameters:
    doc(Doc): Spacy document to be analyzed.

    Yields:
    Iterator: Each alphabetic word as Tokens.
    """
    for para in doc._.paragraphs:
        for sent in para._.non_empty_sentences:
            for word in sent._.alpha_words:
                yield word


def doc_alpha_words_normalized_getter(doc: Doc) -> Iterator:
    """
    Function that gets the alphabetic words for the entire text, all in lowercase and as a string.

    Parameters:
    doc(Doc): Spacy document to be analyzed.

    Yields:
    Iterator: Each alphabetic word as strings.
    """
    for word in doc._.alpha_words:
        yield word.text.strip().lower()


class AlphanumericWordIdentifier:
    """
    Pipe that identifies the alphanumeric words in a doc. It goes after Paragraphizer.
    """

    name = "alphanumeric_word_identifier"

    def __init__(self, nlp: Language) -> None:
        """
        This constructor sets the new extension attributes for Docs.

        It adds a list of alphabetic words to each sentence, as well as the count. It also provides the way to obtain those values for the entire Document/Text

        Parameters:
        nlp(Language): The spacy model that uses this pipeline

        Returns:
        None.
        """
        required_pipes = ["paragraphizer"]
        if not all((pipe in nlp.pipe_names for pipe in required_pipes)):
            message = (
                "Alphanumeric word identifier pipe need the following pipes: "
                + ", ".join(required_pipes)
            )
            raise AttributeError(message)

        self._nlp = nlp
        Span.set_extension("alpha_words", default=[], force=True)  # List of words for sentence
        Span.set_extension(
            "alpha_words_count", default=0, force=True
        )  # Count of words for sentence
        Doc.set_extension("alpha_words", getter=doc_alpha_words_getter, force=True)
        Doc.set_extension(
            "alpha_words_normalized", getter=doc_alpha_words_normalized_getter, force=True
        )
        Doc.set_extension("alpha_words_count", default=0, force=True)
        Doc.set_extension("alpha_words_different", default=set(), force=True)
        Doc.set_extension("alpha_words_different_count", default=0, force=True)

    def __call__(self, doc: Doc) -> Doc:
        """
        This method will identify the words that are considered alphanumeric.

        Parameters:
        doc(Doc): A Spacy document.

        Returns:
        Doc: The analyzed spacy document.
        """
        # Find the alphanumeric words for each sentence of the paragraph
        for para in doc._.paragraphs:
            for sent in para._.non_empty_sentences:
                sent._.alpha_words = [token for token in sent if is_word(token)]
                sent._.alpha_words_count = len(sent._.alpha_words)
                doc._.alpha_words_count += sent._.alpha_words_count

        doc._.alpha_words_different = set(doc._.alpha_words_normalized)
        doc._.alpha_words_different_count = len(doc._.alpha_words_different)

        return doc

