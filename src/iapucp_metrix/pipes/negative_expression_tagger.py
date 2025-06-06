from spacy.matcher import Matcher
from spacy.tokens import Doc
from spacy.util import filter_spans

from typing import List


class NegativeExpressionTagger:
    '''
    This tagger has the task to find all verb phrases in a document. It needs to go after the 'Parser' pipeline component.
    '''
    name = 'negative expression tagger'

    def __init__(self, nlp, pattern: List[List[dict]]) -> None:
        '''
        This constructor will initialize the object that tags verb phrases.

        Parameters:
        nlp: The Spacy model to use this tagger with.
        pattern(List[List[dict]]): Pattern to match the degative expressions.

        Returns:
        None.
        '''
        required_pipes = ['parser']
        if not all((
            pipe in nlp.pipe_names
            for pipe in required_pipes
        )):
            message = 'Negative expression tagger pipe need the following pipes: ' + ', '.join(required_pipes)
            raise AttributeError(message)
        
        self._nlp = nlp
        self._pattern = pattern
        self._matcher = Matcher(nlp.vocab)
        # Add the patterns for the negative expressions
        for pattern in self._pattern:
            self._matcher.add('negative expression', [pattern])

        Doc.set_extension('negative_expressions', default=[], force=True)
        Doc.set_extension('negative_expressions_count', default=0, force=True)

    def __call__(self, doc: Doc) -> Doc:
        '''
        This method will find all negative expressions and store them in an iterable.

        Parameters:
        doc(Doc): A Spacy document.

        Returns:
        Doc: The spacy document that was analyzed
        '''
        matches = self._matcher(doc)
        negative_expression_spans = [doc[start:end] for _, start, end in matches]

        doc._.negative_expressions = [span for span in filter_spans(negative_expression_spans)] # Save the negative expressions found
        doc._.negative_expressions_count = len(doc._.negative_expressions)

        return doc