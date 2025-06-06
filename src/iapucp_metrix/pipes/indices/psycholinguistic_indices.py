from time import time

from spacy.language import Language
from spacy.tokens import Doc

from iapucp_metrix.utils.psycholinguistic import PSY_BANK


def get_psycholinguistic_ratio(
    doc: Doc, pyscholinguistic_name: str, lower_bound: float, upper_bound: float
) -> tuple[float, float, float, float]:
    """
    Returns the ratio of words in a text that have a psycholinguistic value between a given range.

    Parameters:
    doc(Doc): The text to be anaylized.
    pyscholinguistic_name(str): The name of the psycholinguistic value to be used.
    lower_bound(float): The lower bound of the range.
    upper_bound(float): The upper bound of the range.

    Returns:
    float: The psycholinguistic ratio.
    """
    count = 0
    total_count = 0

    for word in doc._.alpha_words:
        value = PSY_BANK.get_ratings(word.text).get(pyscholinguistic_name)
        if value is None:
            continue

        if value >= lower_bound and value < upper_bound:
            count += 1
        total_count += 1

    return count / total_count if total_count > 0 else 0


class PsycholinguisticIndices:
    """
    This class will handle all operations to obtain the psycholinguistic indices of a text according to Coh-Metrix
    """

    def __init__(self, nlp: Language) -> None:
        """
        The constructor will initialize the extensions where to hold the descriptive indices of a doc. It needs the following pipes to be added before it: 'alphanumeric_word_identifier', 'paragraphizer', 'syllablelizer'

        Parameters:
        nlp(Lanuage): The spacy model that corresponds to a language.
        language(str): The language that the texts to process will have.

        Returns:
        None.
        """
        required_pipes = [
            "alphanumeric_word_identifier",
            "paragraphizer",
        ]
        if not all((pipe in nlp.pipe_names for pipe in required_pipes)):
            message = (
                "Psycholinguistic indices pipe need the following pipes: "
                + ", ".join(required_pipes)
            )
            raise AttributeError(message)

        self._nlp = nlp
        Doc.set_extension("psycholinguistic_indices", default=dict(), force=True)

    def __call__(self, doc: Doc) -> Doc:
        """
        This method will calculate the psycholinguistic indices.

        Parameters:
        doc(Doc): A Spacy document.

        Returns:
        Doc: The processed doc.
        """
        if len(doc.text) == 0:
            raise ValueError("The text is empty.")

        start = time()
        doc._.psycholinguistic_indices["PSYC"] = get_psycholinguistic_ratio(
            doc, "concreteness", 0, 99
        )
        doc._.psycholinguistic_indices["PSYC0"] = get_psycholinguistic_ratio(
            doc, "concreteness", 1, 2.5
        )
        doc._.psycholinguistic_indices["PSYC1"] = get_psycholinguistic_ratio(
            doc, "concreteness", 2.5, 4
        )
        doc._.psycholinguistic_indices["PSYC2"] = get_psycholinguistic_ratio(
            doc, "concreteness", 4, 5.5
        )
        doc._.psycholinguistic_indices["PSYC3"] = get_psycholinguistic_ratio(
            doc, "concreteness", 5.5, 7
        )

        doc._.psycholinguistic_indices["PSYIM"] = get_psycholinguistic_ratio(
            doc, "imageability", 0, 99
        )
        doc._.psycholinguistic_indices["PSYIM0"] = get_psycholinguistic_ratio(
            doc, "imageability", 1, 2.5
        )
        doc._.psycholinguistic_indices["PSYIM1"] = get_psycholinguistic_ratio(
            doc, "imageability", 2.5, 4
        )
        doc._.psycholinguistic_indices["PSYIM2"] = get_psycholinguistic_ratio(
            doc, "imageability", 4, 5.5
        )
        doc._.psycholinguistic_indices["PSYIM3"] = get_psycholinguistic_ratio(
            doc, "imageability", 5.5, 7
        )

        doc._.psycholinguistic_indices["PSYFM"] = get_psycholinguistic_ratio(
            doc, "familiarity", 0, 99
        )
        doc._.psycholinguistic_indices["PSYFM0"] = get_psycholinguistic_ratio(
            doc, "familiarity", 1, 2.5
        )
        doc._.psycholinguistic_indices["PSYFM1"] = get_psycholinguistic_ratio(
            doc, "familiarity", 2.5, 4
        )
        doc._.psycholinguistic_indices["PSYFM2"] = get_psycholinguistic_ratio(
            doc, "familiarity", 4, 5.5
        )
        doc._.psycholinguistic_indices["PSYFM3"] = get_psycholinguistic_ratio(
            doc, "familiarity", 5.5, 7
        )

        doc._.psycholinguistic_indices["PSYAoA"] = get_psycholinguistic_ratio(
            doc, "aoa", 0, 99
        )
        doc._.psycholinguistic_indices["PSYAoA0"] = get_psycholinguistic_ratio(
            doc, "aoa", 1, 2.5
        )
        doc._.psycholinguistic_indices["PSYAoA1"] = get_psycholinguistic_ratio(
            doc, "aoa", 2.5, 4
        )
        doc._.psycholinguistic_indices["PSYAoA2"] = get_psycholinguistic_ratio(
            doc, "aoa", 4, 5.5
        )
        doc._.psycholinguistic_indices["PSYAoA3"] = get_psycholinguistic_ratio(
            doc, "aoa", 5.5, 7
        )

        doc._.psycholinguistic_indices["PSYARO"] = get_psycholinguistic_ratio(
            doc, "arousal", 0, 99
        )
        doc._.psycholinguistic_indices["PSYARO0"] = get_psycholinguistic_ratio(
            doc, "arousal", 1, 3
        )
        doc._.psycholinguistic_indices["PSYARO1"] = get_psycholinguistic_ratio(
            doc, "arousal", 3, 5
        )
        doc._.psycholinguistic_indices["PSYARO2"] = get_psycholinguistic_ratio(
            doc, "arousal", 5, 7
        )
        doc._.psycholinguistic_indices["PSYARO3"] = get_psycholinguistic_ratio(
            doc, "arousal", 7, 9
        )

        doc._.psycholinguistic_indices["PSYVAL"] = get_psycholinguistic_ratio(
            doc, "valence", 0, 99
        )
        doc._.psycholinguistic_indices["PSYVAL0"] = get_psycholinguistic_ratio(
            doc, "valence", 1, 4
        )
        doc._.psycholinguistic_indices["PSYVAL1"] = get_psycholinguistic_ratio(
            doc, "valence", 3, 5
        )
        doc._.psycholinguistic_indices["PSYVAL2"] = get_psycholinguistic_ratio(
            doc, "valence", 5, 7
        )
        doc._.psycholinguistic_indices["PSYVAL3"] = get_psycholinguistic_ratio(
            doc, "valence", 7, 9
        )

        return doc
