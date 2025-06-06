from typing import List

from spacy.language import Language
from spacy.matcher import Matcher
from spacy.tokens import Doc
from spacy.util import filter_spans


class VerbPhraseTagger:
    """
    This tagger has the task to find all verb phrases in a document. It needs to go after the 'Parser' pipeline component.
    """

    name = "verb phrase tagger"

    def __init__(self, nlp: Language, pattern: List[List[dict]]) -> None:
        """
        This constructor will initialize the object that tags verb phrases.

        Parameters:
        nlp(Language): The Spacy model to use this tagger with.
        pattern(List[List[dict]]): Pattern to match the verb phrases.

        Returns:
        None.
        """
        required_pipes = ["parser"]
        if not all((pipe in nlp.pipe_names for pipe in required_pipes)):
            message = "Verb phrase tagger pipe need the following pipes: " + ", ".join(
                required_pipes
            )
            raise AttributeError(message)

        self._nlp = nlp
        self._matcher = Matcher(nlp.vocab)
        self._pattern = pattern

        Doc.set_extension("verb_phrases", default=[], force=True)
        Doc.set_extension("verb_phrases_count", default=0, force=True)
        # Add the patterns to find the verb phrases
        for pattern in self._pattern:
            self._matcher.add("verb phrase", [pattern])

    def __call__(self, doc: Doc) -> Doc:
        """
        This method will find all verb phrases and store them in an iterable.

        Parameters:
        doc(Doc): A Spacy document.

        Reeturns:
        Doc: The spacy document that was analyzed
        """
        matches = self._matcher(doc)
        verb_phrase_spans = [doc[start:end] for _, start, end in matches]

        doc._.verb_phrases = [
            span for span in filter_spans(verb_phrase_spans)
        ]  # Save the noun phrases found
        doc._.verb_phrases_count = len(doc._.verb_phrases)

        return doc

