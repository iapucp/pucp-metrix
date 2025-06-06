from typing import Iterator

from spacy.language import Language
from spacy.tokens import Doc, Span

from iapucp_metrix.utils.utils import is_content_word


def doc_content_words_normalized_getter(doc: Doc) -> Iterator:
    """
    Function that gets the content words for the entire text, all in lowercase and as a string.

    Parameters:
    doc(Doc): Spacy document to be analyzed.

    Yields:
    Iterator: Each content word as strings.
    """
    for word in doc._.content_words:
        yield word.text.strip().lower()


def doc_content_words_getter(doc: Doc) -> Iterator:
    """
    Function that gets the content words for the entire text.}

    Parameters:
    doc(Doc): Spacy document to be analyzed.

    Yields:
    Iterator: Each content word as Tokens.
    """
    for para in doc._.paragraphs:
        for sent in para._.non_empty_sentences:
            for word in sent._.content_words:
                yield word


class ContentWordIdentifier:
    """
    Pipe that identifies the content words in a doc. It goes after Paragraphizer.
    """

    name = "content_word_identifier"

    def __init__(self, nlp: Language) -> None:
        """
        This constructor sets the new extension attributes for Docs.

        It adds a list of alphabetic words to each sentence, as well as the count. It also provides the way to obtain those values for the entire Document/Text

        Parameters:
        nlp(Language): The spacy model that uses this pipeline

        Returns:
        None.
        """
        required_pipes = ["paragraphizer", "morphologizer"]
        if not all((pipe in nlp.pipe_names for pipe in required_pipes)):
            message = (
                "Content word identifier pipe need the following pipes: "
                + ", ".join(required_pipes)
            )
            raise AttributeError(message)

        self._nlp = nlp
        Span.set_extension("content_words", default=[], force=True)
        Span.set_extension("content_words_count", default=0, force=True)
        Doc.set_extension("content_words", getter=doc_content_words_getter, force=True)
        Doc.set_extension("content_words_count", default=0, force=True)
        Doc.set_extension(
            "content_words_normalized", getter=doc_content_words_normalized_getter, force=True
        )
        Doc.set_extension("content_words_different", default=set(), force=True)
        Doc.set_extension("content_words_different_count", default=0, force=True)

    def __call__(self, doc: Doc) -> Doc:
        """
        This method will identify the words that are considered alphanumeric.

        Parameters:
        doc(Doc): A Spacy document.

        Returns:
        Doc: The analyzed spacy document.
        """
        # Find the content words for the all paragraphs
        for para in doc._.paragraphs:
            for sent in para._.non_empty_sentences:
                sent._.content_words = [
                    token for token in sent if is_content_word(token)
                ]
                sent._.content_words_count = len(sent._.content_words)
                doc._.content_words_count += sent._.content_words_count

        doc._.content_words_different = set(doc._.content_words_normalized)
        doc._.content_words_different_count = len(doc._.content_words_different)

        return doc

