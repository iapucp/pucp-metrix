from spacy.tokens import Span


def analyze_noun_overlap(prev_sentence: Span, cur_sentence: Span) -> int:
    """
    This function analyzes whether or not there's noun overlap between two sentences for a language.

    Parameters:
    prev_sentence(Span): The previous sentence to analyze.
    cur_sentence(Span): The current sentence to analyze.

    Returns:
    int: 1 if there's overlap between the two sentences and 0 if no.
    """
    for token in cur_sentence._.alpha_words:
        if token.pos_ == "NOUN" and token.text.lower() in prev_sentence._.unique_nouns:
            return 1  # There's cohesion

    return 0  # No cohesion


def analyze_argument_overlap(prev_sentence: Span, cur_sentence: Span) -> int:
    """
    This function analyzes whether or not there's argument overlap between two sentences.

    Parameters:
    prev_sentence(Span): The previous sentence to analyze.
    cur_sentence(Span): The current sentence to analyze.

    Returns:
    int: 1 if there's overlap between the two sentences and 0 if no.
    """
    for (
        token
    ) in cur_sentence._.alpha_words:  # Iterate every token of the current sentence
        if (
            token.pos_ == "NOUN"
            and token.lemma_.lower() in prev_sentence._.unique_noun_lemmas
        ):
            return 1  # There's cohesion by noun lemma

        if (
            "PronType=Prs" in token.morph
            and token.text.lower() in prev_sentence._.unique_personal_pronouns
        ):
            return 1  # There's cohesion by personal pronoun

    return 0  # No cohesion


def analyze_stem_overlap(prev_sentence: Span, cur_sentence: Span) -> int:
    """
    This function analyzes whether or not there's stem overlap between two sentences.

    Parameters:
    prev_sentence(Span): The previous sentence to analyze.
    cur_sentence(Span): The current sentence to analyze.

    Returns:
    int: 1 if there's overlap between the two sentences and 0 if no.
    """
    # Place the tokens in a dictionary for search efficiency
    # print(prev_sentence, prev_sentence._.unique_content_word_lemmas, prev_sentence._.unique_nouns, cur_sentence, cur_sentence._.unique_content_word_lemmas, cur_sentence._.unique_nouns)
    for token in cur_sentence._.alpha_words:
        if (
            token.pos_ in ["NOUN", "PROPN"]
            and token.lemma_.lower() in prev_sentence._.unique_content_word_lemmas
        ):
            return 1  # There's cohesion

    return 0  # No cohesion


def analyze_content_word_overlap(prev_sentence: Span, cur_sentence: Span) -> float:
    """
    This function calculates the proportional content word overlap between two sentences.

    Parameters:
    prev_sentence(Span): The previous sentence to analyze.
    cur_sentence(Span): The current sentence to analyze.

    Returns:
    float: Proportion of tokens that overlap between the current and previous sentences
    """
    total_tokens = (
        prev_sentence._.content_words_count + cur_sentence._.content_words_count
    )

    if total_tokens == 0:  # Nothing to compute
        return 0
    else:
        matches = 0  # Matcher counter

        for token in cur_sentence._.content_words:
            if token.text.lower() in prev_sentence._.unique_content_words:
                matches += 2  # There's cohesion

        return matches / total_tokens


def analyze_anaphore_overlap(
    prev_sentence: Span, cur_sentence: Span, language: str = "es"
) -> int:
    """
    This function analyzes whether or not there's anaphore overlap between two sentences.

    Parameters:
    prev_sentence(Span): The previous sentence to analyze.
    cur_sentence(Span): The current sentence to analyze.
    language(str): The language of the sentences.

    Returns:
    int: 1 if there's overlap between the two sentences and 0 if no.
    """
    for token in cur_sentence._.alpha_words:
        if (
            token.pos_ == "PRON"
            and token.text.lower() in prev_sentence._.unique_pronouns
        ):
            return 1  # There's cohesion

    return 0  # No cohesion
