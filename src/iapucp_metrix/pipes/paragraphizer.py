import re
from typing import Iterator

from spacy.language import Language
from spacy.tokens import Doc, Span


def doc_non_empty_sentences_getter(doc: Doc) -> Iterator:
    """
    Function that gets the non empty sentences for the entire document.

    Parameters:
    doc(Doc): Spacy Doc to analyze.

    Yields:
    Iterator: Iterator with the sentences for the text.
    """
    # Iterate all the paragraphs
    for para in doc._.paragraphs:
        for sent in para._.non_empty_sentences:
            yield sent


class Paragraphizer:
    """
    Pipe that splits the text into paragraphs. It must be the first custom pipe after sentencizer.
    """

    name = "paragraphizer"

    def __init__(self, nlp: Language, paragraph_delimiter: str = "\n\n") -> None:
        """
        This constructor sets the new extension attributes for Docs.

        It adds a list of Span paragraphs (and count) to the main Doc, as well as a list of non empty sentences (and count) to each Span paragraph. The list of said sentences and count for the entire text can be obtained as well.

        Parameters:
        nlp(Language): The spacy model that uses this pipeline
        paragraph_delimiter(str): Symbol used to split the paragraphs

        Returns:
        None.
        """
        required_pipes = ["sentencizer"]
        if not all((pipe in nlp.pipe_names for pipe in required_pipes)):
            message = "Paragraphizer need the following pipes: " + ", ".join(
                required_pipes
            )
            raise AttributeError(message)

        self._nlp = nlp
        self._paragraph_delimiter = paragraph_delimiter

        Doc.set_extension("paragraphs", default=[], force=True)  # List
        Doc.set_extension("paragraph_count", default=0, force=True)  # Paragraph count of text
        Doc.set_extension("non_empty_sentences", getter=doc_non_empty_sentences_getter, force=True)
        Doc.set_extension("sentence_count", default=0, force=True)  # Sentence count of text
        Span.set_extension(
            "non_empty_sentences", default=[], force=True
        )  # Sentences of a paragraph
        Span.set_extension("sentence_count", default=0, force=True)  # Sentence count of a paragraph

    def __call__(self, doc: Doc) -> Doc:
        """
        This method will divide the document into paragraphs.

        Parameters:
        doc(Doc): A Spacy document.

        Returns:
        Doc: The analyzed spacy document.
        """
        length_of_separator = len(self._paragraph_delimiter)
        separator_indices = re.finditer(self._paragraph_delimiter, doc.text)
        paragraphs = []
        token_i = 0
        # Iterate over all the matches of the separator
        for start_match in separator_indices:
            index_start_match = (
                start_match.start()
            )  # Initial character of the paragraph separator
            span_paragraph_sep = doc.char_span(
                index_start_match, index_start_match + length_of_separator
            )  # Get the span of the character separator
            # In case an empty paragraph was found
            if span_paragraph_sep is None:
                continue

            span_paragraph = doc[
                token_i : span_paragraph_sep.start + 1
            ]  # Get the paragraph
            # Add paragraph if it's not empty
            if len(span_paragraph.text.strip()) > 0:
                paragraphs.append(span_paragraph)  # Add the paragraph span
            token_i = span_paragraph_sep.end
        # Add the last paragraph
        if token_i != len(doc):
            paragraphs.append(doc[token_i : len(doc)])
        # Find the non empty sentences for each paragraphs
        for para in paragraphs:
            para._.non_empty_sentences = [
                sentence for sentence in para.sents if len(sentence.text.strip()) > 0
            ]  # Find the non empty sentences of the text
            para._.sentence_count = len(para._.non_empty_sentences)
            doc._.sentence_count += para._.sentence_count
        # Add the paragraphs found to the document
        doc._.paragraphs = paragraphs
        doc._.paragraph_count = len(doc._.paragraphs)

        return doc
