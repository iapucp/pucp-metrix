import pyphen
from spacy.language import Language
from spacy.tokens import Doc, Token


class Syllablelizer:
    """
    Pipe that separates the tokens in syllables. It goes after alphanumeric_word_identifier.

    The pipe adds to each alphabetic token a list of syllables as well as the count of syllables.
    """

    name = "Syllablelizer"

    def __init__(self, nlp: Language, language: str = "es") -> None:
        """
        This constructor will initialize the object that handles syllable processing.

        Parameters:
        nlp(Language): Spacy model used for this pipe.
        language(str): The language that this pipeline will be used in.

        Returns:
        None.
        """
        required_pipes = ["alphanumeric_word_identifier"]
        if not all((pipe in nlp.pipe_names for pipe in required_pipes)):
            message = "Syllablelizer pipe need the following pipes: " + ", ".join(
                required_pipes
            )
            raise AttributeError(message)

        self._nlp = nlp
        self._language = language
        self._dic = pyphen.Pyphen(lang="es")
        Token.set_extension("syllables", default=[], force=True)
        Token.set_extension("syllable_count", default=0)
        Doc.set_extension("syllable_count", default=0)
        Doc.set_extension("polysyllabic_words_count", default=0)

    def __call__(self, doc: Doc) -> Doc:
        """
        This method will find the syllables for each token that is a word.

        Parameters:
        doc(Doc): A Spacy document.

        Returns:
        Doc: The analyzed spacy document.
        """
        for token in doc._.alpha_words:  # Iterate every token
            token._.syllables = self._dic.inserted(token.text).split("-")
            token._.syllable_count = len(token._.syllables)
            doc._.syllable_count += token._.syllable_count

            if token._.syllable_count >= 3:
                doc._.polysyllabic_words_count += 1

        return doc
