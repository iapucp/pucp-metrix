from spacy.language import Language
from spacy.tokens import Doc
from spacy.tokens import Span


class WordsBeforeMainVerbCounter:
    '''
    This pipe counts the amount of words before the main verb of sentences. It needs to go after Paragraphizer and the alphanumeric word identifier.
    '''
    name = 'words_before_main_verb_counter'

    def __init__(self, nlp: Language) -> None:
        '''
        This constructor will initialize the object that counts the words before the main verb of sentences.

        Parameters:
        language: The language that this pipeline will be used in.

        Returns:
        None.
        '''
        required_pipes = ['paragraphizer', 'alphanumeric_word_identifier']
        if not all((
            pipe in nlp.pipe_names
            for pipe in required_pipes
        )):
            message = 'Words before main verb pipe need the following pipes: ' + ', '.join(required_pipes)
            raise AttributeError(message)
        
        self._nlp = nlp

        Span.set_extension('count_of_words_before_main_verb', default=0) # Count of adjectives in a noun phrase

    def __call__(self, doc: Doc) -> Doc:
        '''
        This method will find all noun phrases and store them in an iterable.

        Parameters:
        doc(Doc): A Spacy document.

        Returns:
        Doc: The spacy document analyzed.
        '''
        # Iterate every non empty sentence of the document
        for sent in doc._.non_empty_sentences:
            left_words = []
            # Iterate every alphanumeric word of the sentence
            for token in sent._.alpha_words:
                if token.pos_ in ['VERB', 'AUX'] and token.dep_ == 'ROOT':
                    break
                else:
                    left_words.append(token.text)
            # Compute the count of words before the main verb for the current sentence
            sent._.count_of_words_before_main_verb = len(left_words)

        return doc