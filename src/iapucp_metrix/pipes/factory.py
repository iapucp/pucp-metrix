from spacy.lang.es import Spanish
from spacy.language import Language

from iapucp_metrix.pipes.additive_connectives_tagger import AdditiveConnectivesTagger
from iapucp_metrix.pipes.adversative_connectives_tagger import (
    AdversativeConnectivesTagger,
)
from iapucp_metrix.pipes.alphanumeric_word_identifier import AlphanumericWordIdentifier
from iapucp_metrix.pipes.causal_connectives_tagger import CausalConnectivesTagger
from iapucp_metrix.pipes.cohesion_words_tokenizer import CohesionWordsTokenizer
from iapucp_metrix.pipes.content_word_identifier import ContentWordIdentifier
from iapucp_metrix.pipes.indices.connective_indices import ConnectiveIndices
from iapucp_metrix.pipes.indices.descriptive_indices import DescriptiveIndices
from iapucp_metrix.pipes.indices.lexical_diversity_indices import (
    LexicalDiversityIndices,
)
from iapucp_metrix.pipes.indices.psycholinguistic_indices import PsycholinguisticIndices
from iapucp_metrix.pipes.indices.readability_indices import ReadabilityIndices
from iapucp_metrix.pipes.indices.referential_cohesion_indices import (
    ReferentialCohesionIndices,
)
from iapucp_metrix.pipes.indices.semantic_cohesion_indices import (
    SemanticCohesionIndices,
)
from iapucp_metrix.pipes.indices.syntactic_complexity_indices import (
    SyntacticComplexityIndices,
)
from iapucp_metrix.pipes.indices.syntactic_pattern_density_indices import (
    SyntacticPatternDensityIndices,
)
from iapucp_metrix.pipes.indices.textual_simplicity_indices import (
    TextualSimplicityIndices,
)
from iapucp_metrix.pipes.indices.word_frequency_indices import WordFrequencyIndices
from iapucp_metrix.pipes.indices.word_information_indices import WordInformationIndices
from iapucp_metrix.pipes.informative_word_tagger import InformativeWordTagger
from iapucp_metrix.pipes.logical_connectives_tagger import LogicalConnectivesTagger
from iapucp_metrix.pipes.negative_expression_tagger import NegativeExpressionTagger
from iapucp_metrix.pipes.noun_phrase_tagger import NounPhraseTagger
from iapucp_metrix.pipes.overlap_analyzers import (
    analyze_anaphore_overlap,
    analyze_argument_overlap,
    analyze_content_word_overlap,
    analyze_noun_overlap,
    analyze_stem_overlap,
)
from iapucp_metrix.pipes.paragraphizer import Paragraphizer
from iapucp_metrix.pipes.syllablelizer import Syllablelizer
from iapucp_metrix.pipes.temporal_connectives_tagger import TemporalConnectivesTagger
from iapucp_metrix.pipes.verb_phrase_tagger import VerbPhraseTagger
from iapucp_metrix.pipes.words_before_main_verb_counter import (
    WordsBeforeMainVerbCounter,
)
from iapucp_metrix.pipes.wrapper_serializer import WrapperSerializer


@Language.factory("wrapper_serializer")
def create_wrapper_serializer(nlp: Language, name: str) -> WrapperSerializer:
    """
    Function that creates a wrapper serializer pipe.

    Parameters:
    nlp(Language): Language model to use.
    name(str): Name of the pipe.

    Returns:
    WrapperSerializer: Pipe that wraps all entities of a Doc, and the doc itself, to prepare it for serialization.
    """
    return WrapperSerializer(nlp)


@Spanish.factory("alphanumeric_word_identifier")
def create_es_alphanumeric_word_identifier(
    nlp: Language, name: str
) -> AlphanumericWordIdentifier:
    """
    Function that creates an alphanumeric word identifier for spanish.

    Paramters:
    nlp(Language): Spacy model that will be used for the pipeline.
    name(str): Name of the pipe.

    Returns:
    AlphanumericWordIdentifier: The pipe that finds alphanumeric words.
    """
    return AlphanumericWordIdentifier(nlp)


@Spanish.factory("paragraphizer", default_config={"paragraph_delimiter": "\n\n"})
def create_es_paragraphizer(
    nlp: Language, name: str, paragraph_delimiter: str
) -> Paragraphizer:
    """
    Function that creates a paragraph splitter for spanish.

    Paramters:
    nlp(Language): Spacy model that will be used for the pipeline.
    name(str): Name of the pipe.
    paragraph_delimiter(str): Character used to split the paragraphs.

    Returns:
    Paragraphizer: The pipe that separates the text into paragraphs.
    """
    return Paragraphizer(nlp, paragraph_delimiter)


@Spanish.factory("syllablelizer", default_config={"language": "es"})
def create_es_syllablelizer(nlp: Language, name: str, language: str) -> Syllablelizer:
    """
    Function that creates a syllable splitter for spanish.

    Paramters:
    nlp(Language): Spacy model that will be used for the pipeline.
    name(str): Name of the pipe.
    language(str): Character used to split the paragraphs

    Returns:
    Syllablelizer: The pipe that finds divides the words by syllables.
    """
    return Syllablelizer(nlp, language)


@Spanish.factory("descriptive_indices")
def create_es_descriptive_indices(nlp: Language, name: str) -> DescriptiveIndices:
    """
    Function that creates descriptive indices pipe.

    Paramters:
    nlp(Language): Spacy model that will be used for the pipeline.
    name(str): Name of the pipe.

    Returns:
    ParagraphSplitter: The pipe that finds descriptive indices.
    """
    return DescriptiveIndices(nlp)


@Spanish.factory("psycholinguistic_indices")
def create_es_psycholinguistic_indices(
    nlp: Language, name: str
) -> PsycholinguisticIndices:
    """
    Function that creates psycholinguistic indices pipe.

    Paramters:
    nlp(Language): Spacy model that will be used for the pipeline.
    name(str): Name of the pipe.

    Returns:
    ParagraphSplitter: The pipe that finds psycholinguistic indices.
    """
    return PsycholinguisticIndices(nlp)


@Spanish.factory("content_word_identifier")
def create_es_content_word_identifier(
    nlp: Language, name: str
) -> ContentWordIdentifier:
    """
    Function that creates content word identifier pipe.

    Paramters:
    nlp(Language): Spacy model that will be used for the pipeline.
    name(str): Name of the pipe.

    Returns:
    ContentWordIdentifier: The pipe that finds content words.
    """
    return ContentWordIdentifier(nlp)


@Spanish.factory("lexical_diversity_indices")
def create_es_lexical_diversity_indices(
    nlp: Language, name: str
) -> LexicalDiversityIndices:
    """
    Function that creates lexical diversity indices pipe.

    Paramters:
    nlp(Language): Spacy model that will be used for the pipeline.
    name(str): Name of the pipe.

    Returns:
    ParagraphSplitter: The pipe that finds the lexical diversity indices.
    """
    return LexicalDiversityIndices(nlp)


@Spanish.factory("readability_indices")
def create_es_readability_indices(nlp: Language, name: str) -> ReadabilityIndices:
    """
    Function that creates readability indices pipe.

    Paramters:
    nlp(Language): Spacy model that will be used for the pipeline.
    name(str): Name of the pipe.

    Returns:
    ReadabilityIndices: The pipe that finds the readability indices.
    """
    return ReadabilityIndices(nlp)


@Spanish.factory("noun_phrase_tagger")
def create_es_noun_phrase_tagger(nlp: Language, name: str) -> NounPhraseTagger:
    """
    Function that creates a noun phrase tagger.

    Paramters:
    nlp(Language): Spacy model that will be used for the pipeline.
    name(str): Name of the pipe.

    Returns:
    NounPhraseTagger: The pipe that tags the noun phrases.
    """
    return NounPhraseTagger(nlp)


@Spanish.factory("syntactic_complexity_indices")
def create_es_syntactic_complexity_indices(
    nlp: Language, name: str
) -> SyntacticComplexityIndices:
    """
    Function that creates a syntactic complexity indices pipe.

    Paramters:
    nlp(Language): Spacy model that will be used for the pipeline.
    name(str): Name of the pipe.

    Returns:
    SyntacticComplexityIndices: The pipe that calculates the syntactic complexity indices.
    """
    return SyntacticComplexityIndices(nlp)


@Spanish.factory("words_before_main_verb_counter")
def create_es_words_before_main_verb_counter(
    nlp: Language, name: str
) -> WordsBeforeMainVerbCounter:
    """
    Function that creates words before main verb counter pipe.

    Paramters:
    nlp(Language): Spacy model that will be used for the pipeline.
    name(str): Name of the pipe.

    Returns:
    SyntacticComplexityIndices: The pipe that calculates the amount of words before the main verb of every sentence.
    """
    return WordsBeforeMainVerbCounter(nlp)


@Spanish.factory("verb_phrase_tagger")
def create_es_verb_phrase_tagger(nlp: Language, name: str) -> VerbPhraseTagger:
    """
    Function that creates verb phrase tagger pipe.

    Paramters:
    nlp(Language): Spacy model that will be used for the pipeline.
    name(str): Name of the pipe.

    Returns:
    VerbPhraseTagger: The pipe that tags the verb phrases.
    """
    """return VerbPhraseTagger(nlp, [[
        {'POS': {'IN': ['AUX', 'VERB']}, 'OP': '+'},
        {'POS': {'IN': ['ADP', 'SCONJ', 'CONJ', 'INTJ']}, 'OP': '*'},
        {'POS': 'ADP', 'TAG': 'ADP__AdpType=Prep', 'OP': '*'},
        {'POS': {'IN': ['AUX', 'VERB']}}
    ]])"""
    return VerbPhraseTagger(
        nlp,
        [
            [
                {"POS": {"IN": ["AUX", "VERB"]}, "OP": "+"},
                {"POS": {"IN": ["ADP", "SCONJ", "CONJ", "INTJ"]}, "OP": "*"},
                {"POS": "ADP", "OP": "*"},
                {"POS": {"IN": ["AUX", "VERB"]}},
            ]
        ],
    )


@Spanish.factory("negative_expression_tagger")
def create_es_negative_expression_tagger(
    nlp: Language, name: str
) -> NegativeExpressionTagger:
    """
    Function that creates negative expression tagger pipe.

    Paramters:
    nlp(Language): Spacy model that will be used for the pipeline.
    name(str): Name of the pipe.

    Returns:
    NegativeExpressionTagger: The pipe that tags the negative expressions.
    """
    return NegativeExpressionTagger(
        nlp, [[{"POS": "ADV", "LOWER": {"IN": ["no", "nunca", "jamás", "tampoco"]}}]]
    )


@Spanish.factory("syntactic_pattern_density_indices")
def create_es_syntactic_pattern_density_indices(
    nlp: Language, name: str
) -> SyntacticPatternDensityIndices:
    """
    Function that creates syntactic pattern density indices pipe.

    Paramters:
    nlp(Language): Spacy model that will be used for the pipeline.
    name(str): Name of the pipe.

    Returns:
    SyntacticPatternDensityIndices: The pipe that calculates the syntactic pattern density indices.
    """
    return SyntacticPatternDensityIndices(nlp)


@Spanish.factory("causal_connectives_tagger")
def create_es_causal_connectives_tagger(
    nlp: Language, name: str
) -> CausalConnectivesTagger:
    """
    Function that creates causal connective tagger pipe.

    Paramters:
    nlp(Language): Spacy model that will be used for the pipeline.
    name(str): Name of the pipe.

    Returns:
    CausalConnectivesTagger: The pipe that tags the causal connectives.
    """
    return CausalConnectivesTagger(
        nlp,
        [
            "por",
            "porque",
            "a causa de",
            "puesto que",
            "con motivo de",
            "pues",
            "ya que",
            "conque",
            "luego",
            "pues",
            "por consiguiente",
            "así que",
            "en consecuencia",
            "de manera que",
            "tan",
            "tanto que",
            "por lo tanto",
            "de modo que",
        ],
    )


@Spanish.factory("logical_connectives_tagger")
def create_es_logical_connectives_tagger(
    nlp: Language, name: str
) -> LogicalConnectivesTagger:
    """
    Function that creates logical connective tagger pipe.

    Paramters:
    nlp(Language): Spacy model that will be used for the pipeline.
    name(str): Name of the pipe.

    Returns:
    LogicalConnectivesTagger: The pipe that tags the logical connectives.
    """
    return LogicalConnectivesTagger(nlp, ["y", "o"])


@Spanish.factory("adversative_connectives_tagger")
def create_es_adversative_connectives_tagger(
    nlp: Language, name: str
) -> AdversativeConnectivesTagger:
    """
    Function that creates adversative connective tagger pipe.

    Paramters:
    nlp(Language): Spacy model that will be used for the pipeline.
    name(str): Name of the pipe.

    Returns:
    LogicalConnectivesTagger: The pipe that tags the adversative connectives.
    """
    return AdversativeConnectivesTagger(
        nlp,
        [
            "pero",
            "sino",
            "no obstante",
            "sino que",
            "sin embargo",
            "pero sí",
            "aunque",
            "menos",
            "solo",
            "excepto",
            "salvo",
            "más que",
            "en cambio",
            "ahora bien",
            "más bien",
        ],
    )


@Spanish.factory("temporal_connectives_tagger")
def create_es_temporal_connectives_tagger(
    nlp: Language, name: str
) -> TemporalConnectivesTagger:
    """
    Function that creates temporal connective tagger pipe.

    Paramters:
    nlp(Language): Spacy model that will be used for the pipeline.
    name(str): Name of the pipe.

    Returns:
    TemporalConnectivesTagger: The pipe that tags the temporal connectives.
    """
    return TemporalConnectivesTagger(
        nlp,
        [
            "actualmente",
            "ahora",
            "después",
            "más tarde",
            "más adelante",
            "a continuación",
            "antes",
            "mientras",
            "érase una vez",
            "hace mucho tiempo",
            "tiempo antes",
            "finalmente",
            "inicialmente",
            "ya",
            "simultáneamente",
            "previamente",
            "anteriormente",
            "posteriormente",
            "al mismo tiempo",
            "durante",
        ],
    )


@Spanish.factory("additive_connectives_tagger")
def create_es_additive_connectives_tagger(
    nlp: Language, name: str
) -> AdditiveConnectivesTagger:
    """
    Function that creates additive connective tagger pipe.

    Paramters:
    nlp(Language): Spacy model that will be used for the pipeline.
    name(str): Name of the pipe.

    Returns:
    AdditiveConnectivesTagger: The pipe that tags the additive connectives.
    """
    return AdditiveConnectivesTagger(
        nlp,
        [
            "asimismo",
            "igualmente" "de igual modo",
            "de igual manera",
            "de igual forma",
            "del mismo modo",
            "de la misma manera",
            "de la misma forma",
            "en primer lugar",
            "en segundo lugar",
            "en tercer lugar",
            "en último lugar",
            "por su parte",
            "por otro lado",
            "además",
            "encima",
            "es más",
            "por añadidura",
            "incluso",
            "inclusive",
            "para colmo",
        ],
    )


@Spanish.factory("connective_indices")
def create_es_connective_indices(nlp: Language, name: str) -> ConnectiveIndices:
    """
    Function that creates connective indices pipe.

    Paramters:
    nlp(Language): Spacy model that will be used for the pipeline.
    name(str): Name of the pipe.

    Returns:
    ConnectiveIndices: The pipe that calculates the connective indices.
    """
    return ConnectiveIndices(nlp)


@Spanish.factory("cohesion_words_tokenizer")
def create_es_cohesion_words_tokenizer(
    nlp: Language, name: str
) -> CohesionWordsTokenizer:
    """
    Function that creates a cohesion word tokenizer pipe.

    Paramters:
    nlp(Language): Spacy model that will be used for the pipeline.
    name(str): Name of the pipe.

    Returns:
    CohesionWordsTokenizer: The pipe that tokenizes the cohesion words for each sentence.
    """
    return CohesionWordsTokenizer(nlp)


@Spanish.factory("referential_cohesion_indices")
def create_es_referential_cohesion_indices(
    nlp: Language, name: str
) -> ReferentialCohesionIndices:
    """
    Function that creates referential cohesion pipe.

    Paramters:
    nlp(Language): Spacy model that will be used for the pipeline.
    name(str): Name of the pipe.

    Returns:
    ReferentialCohesionIndices: The pipe that calculates the referential cohesion indices.
    """
    return ReferentialCohesionIndices(
        nlp,
        analyze_noun_overlap,
        analyze_argument_overlap,
        analyze_stem_overlap,
        analyze_content_word_overlap,
        analyze_anaphore_overlap,
    )


@Spanish.factory("semantic_cohesion_indices")
def create_es_semantic_cohesion_indices(
    nlp: Language, name: str
) -> SemanticCohesionIndices:
    """
    Function that creates semantic cohesion pipe.

    Paramters:
    nlp(Language): Spacy model that will be used for the pipeline.
    name(str): Name of the pipe.

    Returns:
    SemanticCohesionIndices: The pipe that calculates the referential cohesion indices.
    """
    return SemanticCohesionIndices(
        nlp,
    )


@Spanish.factory("textual_simplicity_indices")
def create_es_textual_simplicity_indices(
    nlp: Language, name: str
) -> TextualSimplicityIndices:
    """
    Function that creates textual simplicity pipe.

    Paramters:
    nlp(Language): Spacy model that will be used for the pipeline.
    name(str): Name of the pipe.

    Returns:
    TextualSimplicityIndices: The pipe that calculates the textual simplicity indices.
    """
    return TextualSimplicityIndices(
        nlp,
    )


@Spanish.factory("informative_word_tagger")
def create_es_informative_word_tagger(
    nlp: Language, name: str
) -> InformativeWordTagger:
    """
    Function that creates a informative word tagger pipe.

    Paramters:
    nlp(Language): Spacy model that will be used for the pipeline.
    name(str): Name of the pipe.

    Returns:
    CohesionWordsTokenizer: The pipe that tags the informative words.
    """
    return InformativeWordTagger(nlp)


@Spanish.factory("word_information_indices")
def create_es_word_information_indices(
    nlp: Language, name: str
) -> WordInformationIndices:
    """
    Function that creates word information pipe.

    Paramters:
    nlp(Language): Spacy model that will be used for the pipeline.
    name(str): Name of the pipe.

    Returns:
    WordInformationIndices: The pipe that calculates the word information indices.
    """
    return WordInformationIndices(nlp)


@Spanish.factory("word_frequency_indices")
def create_es_word_frequency_indices(nlp: Language, name: str) -> WordFrequencyIndices:
    """
    Function that creates word frequency indices pipe.

    Paramters:
    nlp(Language): Spacy model that will be used for the pipeline.
    name(str): Name of the pipe.

    Returns:
    WordFrequencyIndices: The pipe that calculates the word frequency indices.
    """
    return WordFrequencyIndices(nlp)
