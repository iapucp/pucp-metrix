from spacy.language import Language
from spacy.matcher import PhraseMatcher
from spacy.tokens import Doc
from spacy.util import filter_spans
from typing import List


class LogicalConnectivesTagger:
    '''
    This tagger has the task to find all logical connectives in a document. It needs to go after the 'Morphologizer' pipeline component.
    '''
    name = 'logical_connectives_tagger'

    def __init__(self, nlp: Language, connectives: List[str]) -> None:
        '''
        This constructor will initialize the object that tags logical connectives.

        Parameters:
        nlp: The Spacy model to use this tagger with.
        connectives(List[str]): Connectives to match.

        Returns:
        None.
        '''
        required_pipes = ['morphologizer']
        if not all((
            pipe in nlp.pipe_names
            for pipe in required_pipes
        )):
            message = 'Logical connectives tagger pipe need the following pipes: ' + ', '.join(required_pipes)
            raise AttributeError(message)

        self._nlp = nlp
        self._matcher = PhraseMatcher(nlp.vocab, attr='LOWER')
        self._connectives = connectives

        Doc.set_extension('logical_connectives', default=[], force=True)
        Doc.set_extension('logical_connectives_count', default=0, force=True)
        # Add the connectives to the matcher
        for con in self._connectives:
            #con_doc = self._nlp.tokenizer(con, disable=self._nlp.pipe_names)
            con_doc = self._nlp.tokenizer(con)
            self._matcher.add(con, [con_doc])

    def __call__(self, doc: Doc) -> Doc:
        '''
        This method will find all logical connectives and store them in an iterable.

        Parameters:
        doc(Doc): A Spacy document.

        Returns:
        Doc: The spacy document analyzed
        '''
        matches = self._matcher(doc)
        logical_connectives_spans = [doc[start:end] for _, start, end in matches]

        doc._.logical_connectives = [span for span in filter_spans(logical_connectives_spans)] # Save the logical connectives found
        doc._.logical_connectives_count = len(doc._.logical_connectives)

        return doc