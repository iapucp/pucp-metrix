from typing import Iterator
from spacy.language import Language
from spacy.tokens import Doc
from spacy.tokens import Span


def doc_content_words_normalized_getter(doc: Doc) -> Iterator:
    '''
    Function that gets the content words for the entire text, all in lowercase and as a string.

    Parameters:
    doc(Doc): Spacy document to be analyzed.

    Yields:
    Iterator: Each content word as strings.
    '''
    for word in doc._.content_words:
        yield word.text.strip().lower()

def doc_content_words_getter(doc: Doc) -> Iterator:
    '''
    Function that gets the content words for the entire text.}

    Parameters:
    doc(Doc): Spacy document to be analyzed.

    Yields:
    Iterator: Each content word as Tokens.
    '''
    for para in doc._.paragraphs:
        for sent in para._.non_empty_sentences:
            for word in sent._.content_words:
                yield word

class CohesionWordsTokenizer:
    '''
    Pipe that tokenizes each sentence to find the cohesion words to use for each sentence. It goes after the Content/Alphanumeric word identifiers.
    '''
    
    name = 'cohesion_words_tokenizer'

    def __init__(self, nlp: Language) -> None:
        '''
        This constructor sets the new extension attributes for Docs.

        It adds lists to each sentence that contains unique nouns, their lemmas, content words, their lemmas, pronouns and personal pronouns

        Parameters:
        nlp(Language): The spacy model that uses this pipeline
        
        Returns:
        None.
        '''
        required_pipes = ['alphanumeric_word_identifier', 'content_word_identifier']
        if not all((
            pipe in nlp.pipe_names
            for pipe in required_pipes
        )):
            message = 'Cohesion words tokenizer pipe need the following pipes: ' + ', '.join(required_pipes)
            raise AttributeError(message)

        self._nlp = nlp
        Span.set_extension('unique_nouns', default=set(), force=True)
        Span.set_extension('unique_noun_lemmas', default=set(), force=True)
        Span.set_extension('unique_content_words', default=set(), force=True)
        Span.set_extension('unique_content_word_lemmas', default=set(), force=True)
        Span.set_extension('unique_pronouns', default=set(), force=True)
        Span.set_extension('unique_personal_pronouns', default=set(), force=True)

    def __call__(self, doc: Doc) -> Doc:
        '''
        This method will identify the cohesion wordsfor each sentence.

        Parameters:
        doc(Doc): A Spacy document.

        Returns:
        Doc: The analyzed spacy document.
        '''
        # Find the content words for the all paragraphs
        for para in doc._.paragraphs:
            for sent in para._.non_empty_sentences:
                sent._.unique_nouns = set(
                    token.text.lower()
                    for token in sent._.alpha_words
                    if token.pos_ == 'NOUN'
                )
                sent._.unique_noun_lemmas = set(
                    token.lemma_.lower()
                    for token in sent._.alpha_words
                    if token.pos_ == 'NOUN'
                )
                sent._.unique_content_words = set(
                    token.text.lower()
                    for token in sent._.content_words
                )
                sent._.unique_content_word_lemmas = set(
                    token.lemma_.lower()
                    for token in sent._.content_words
                )
                sent._.unique_pronouns = set(
                    token.text.lower()
                    for token in sent._.alpha_words
                    if token.pos_ == 'PRON'
                )
                sent._.unique_personal_pronouns = set(
                    token.text.lower()
                    for token in sent._.alpha_words
                    if 'PronType=Prs' in token.morph
                )

        return doc