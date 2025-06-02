import re
import textwrap
from itertools import tee
from typing import List, Tuple

import spacy
from spacy.tokens import Doc, Span, Token


def split_text_into_paragraphs(text: str) -> List[str]:
    """
    This function splits a text into paragraphs. It assumes paragraphs are separated by two line breaks.

    Parameters:
    text(str): The text to be split into paragraphs.

    Returns:
    List[str]: A list of paragraphs.
    """
    text_aux = text.strip()
    paragraphs = text_aux.split("\n\n")  # Strip any leading whitespaces

    for p in paragraphs:
        p = p.strip()

    return [p.strip() for p in paragraphs if len(p) > 0]  # Don't count empty paragraphs


def split_text_into_sentences(text: str, language: str = "es") -> List[str]:
    """
    This function splits a text into sentences.

    Parameters:
    text(str): The text to be split into sentences.

    Returns:
    List[str]: A list of sentences.
    """

    nlp = spacy.load(language, disable=["tagger", "parser", "ner"])
    nlp.add_pipe(nlp.create_pipe("sentencizer"))
    text_spacy = nlp(text)
    return [str(sentence) for sentence in text_spacy.sents]


def is_content_word(token: Token) -> bool:
    """
    This function checks if a token is a content word: Substantive, verb, adverb or adjective.

    Parameters:
    token(Token): A Spacy token to analyze.

    Returns:
    bool: True or false.
    """
    return token.is_alpha and token.pos_ in [
        "PROPN",
        "NOUN",
        "VERB",
        "ADJ",
        "ADV",
    ]


def is_function_word(token: Token) -> bool:
    """
    This function checks if a token is a function word.

    Parameters:
    token(Token): A Spacy token to analyze.

    Returns:
    bool: True or false.
    """
    return token.is_alpha and token.pos_ in [
        "DET",
        "PRON",
        "ADP",
        "CCONJ",
        "SCONJ",
        "AUX",
        "PART",
        "INTJ",
    ]


def is_word(token: Token) -> bool:
    """
    This function checks if a token is a word. All characters will be alphabetic.

    Parameters:
    token(Token): A Spacy token to analyze.

    Returns:
    bool: True or false.
    """
    return token.is_alpha


def split_doc_into_sentences(doc: Doc) -> List[Span]:
    """
    This function splits a text into sentences.

    Parameters:
    text(str): The text to be split into sentences.

    Returns:
    List[Span]: A list of sentences represented by spacy spans.
    """
    return [s for s in doc.sents if len(s.text.strip()) > 0]


def preprocess_text_spanish(text: str) -> str:
    """
    Function that deletes the extra line breaks in between paragraphs.

    Parameters:
    text(str): The text to clean.

    Returns:
    str: The text cleaned.
    """
    clean_text = re.sub(r"\n\n\n+", "\n\n", text)
    clean_text = textwrap.dedent(clean_text)
    return clean_text


def get_adjacent_sentences_pairs(doc: Doc) -> Tuple[Span, Span]:
    """
    Iterator that returns all pairs of adjacent sentences.

    Parameters:
    doc(Doc): The document to analyze.

    Yields:
    Tuple[Span, Span]: Pair of spans that represent two adjacent sentences.
    """
    sentences = doc._.non_empty_sentences
    prev, cur = tee(sentences)
    next(cur, None)
    # Return each pair of sentences
    for prev, cur in zip(prev, cur):
        yield prev, cur
