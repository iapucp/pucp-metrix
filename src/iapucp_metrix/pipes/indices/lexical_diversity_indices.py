import math
import random
from time import time

import numpy as np
from scipy.optimize import curve_fit
from spacy.language import Language
from spacy.tokens import Doc


class LexicalDiversityIndices:
    """
    This class will handle all operations to obtain the lexical diversity indices of a text according to Coh-Metrix
    """

    name = "lexical_diversity_indices"

    def __init__(self, nlp: Language) -> None:
        """
        The constructor will initialize this object that calculates the lexical diversity indices for a specific language of those that are available.
        It needs the following pipes to be added before it: Content word identifier, alphanumeric word identifier and informative word tagger.

        Parameters:
        nlp: The spacy model that corresponds to a language.

        Returns:
        None.
        """
        required_pipes = [
            "content_word_identifier",
            "alphanumeric_word_identifier",
            "informative_word_tagger",
        ]
        if not all((pipe in nlp.pipe_names for pipe in required_pipes)):
            message = (
                "Lexical diversity indices pipe need the following pipes: "
                + ", ".join(required_pipes)
            )
            raise AttributeError(message)

        self._nlp = nlp
        self._mltd_segment_size = 100
        Doc.set_extension("lexical_diversity_indices", default=dict())  # Dictionary

    def __call__(self, doc: Doc) -> Doc:
        """
        This method will calculate the lexical diversity indices.

        Parameters:
        doc(Doc): A Spacy document.

        Returns:
        Doc: The processed doc.
        """
        if len(doc.text) == 0:
            raise ValueError("The text is empty.")

        start = time()
        doc._.lexical_diversity_indices["LDTTRa"] = (
            self.__get_type_token_ratio_between_all_words(doc)
        )
        doc._.lexical_diversity_indices["LDTTRcw"] = (
            self.__get_type_token_ratio_of_content_words(doc)
        )
        doc._.lexical_diversity_indices["LDTTRno"] = (
            self.__get_type_token_ratio_of_nouns(doc)
        )
        doc._.lexical_diversity_indices["LDTTRvb"] = (
            self.__get_type_token_ratio_of_verbs(doc)
        )
        doc._.lexical_diversity_indices["LDTTRadv"] = (
            self.__get_type_token_ratio_of_adverbs(doc)
        )
        doc._.lexical_diversity_indices["LDTTRadj"] = (
            self.__get_type_token_ratio_of_adjectives(doc)
        )
        doc._.lexical_diversity_indices["LDTTRLa"] = (
            self.__get_type_token_ratio_between_all_lemma_words(doc)
        )
        doc._.lexical_diversity_indices["LDTTRLno"] = (
            self.__get_type_token_ratio_of_lemma_nouns(doc)
        )
        doc._.lexical_diversity_indices["LDTTRLvb"] = (
            self.__get_type_token_ratio_of_lemma_verbs(doc)
        )
        doc._.lexical_diversity_indices["LDTTRLadv"] = (
            self.__get_type_token_ratio_of_lemma_adverbs(doc)
        )
        doc._.lexical_diversity_indices["LDTTRLadj"] = (
            self.__get_type_token_ratio_of_lemma_adjectives(doc)
        )
        doc._.lexical_diversity_indices["LDTTRLpron"] = (
            self.__get_type_token_ratio_of_pronouns(doc)
        )
        doc._.lexical_diversity_indices["LDTTRLrpron"] = (
            self.__get_type_token_ratio_of_pronouns_relative(doc)
        )
        doc._.lexical_diversity_indices["LDTTRLipron"] = (
            self.__get_type_token_ratio_of_pronouns_indefinite(doc)
        )
        doc._.lexical_diversity_indices["LDTTRLifn"] = (
            self.__get_type_token_ratio_of_functional_words(doc)
        )
        doc._.lexical_diversity_indices["LDMLTD"] = self.__calculate_mtld(doc)
        doc._.lexical_diversity_indices["LDVOCd"] = self.__calculate_vocd(doc)
        doc._.lexical_diversity_indices["LDMaas"] = self.__calculate_maas(doc)
        doc._.lexical_diversity_indices["LDDno"] = self.__get_noun_density(doc)
        doc._.lexical_diversity_indices["LDDvb"] = self.__get_verb_density(doc)
        doc._.lexical_diversity_indices["LDDadv"] = self.__get_adverb_density(doc)
        doc._.lexical_diversity_indices["LDDadj"] = self.__get_adjective_density(doc)

        return doc

    def __calculate_maas(self, doc: Doc) -> float:
        """
        This method return the Maas' index of a text.

        Parameters:
        doc(Doc): The text to be anaylized.

        Returns:
        float: The Maas' index of a text.
        """
        n = doc._.alpha_words_count
        v = doc._.alpha_words_different_count
        return 0 if v == 1 else (math.log10(n) - math.log10(v)) / math.log10(v) ** 2

    def __calculate_mtld(self, doc: Doc) -> float:
        """
        This method return the Measure of Textual Lexical Diversity (MTLD) of a text.

        Parameters:
        doc(Doc): The text to be anaylized.

        Returns:
        float: The Measure of Textual Lexical Diversity (MTLD) of a text.
        """

        tokens = [word.text.lower() for word in doc._.alpha_words]
        total_tokens = doc._.alpha_words_count

        def mtld_pass(tokens, threshold=0.72):
            seg_count = 0
            token_count = 0
            types = set()

            for tok in tokens:
                token_count += 1
                types.add(tok)
                ttr = len(types) / token_count
                if ttr <= threshold:
                    seg_count += 1
                    types.clear()
                    token_count = 0

            # handle the final partial segment
            if token_count > 0:
                ttr = len(types) / token_count
                remainder = (1 - ttr) / (1 - threshold)
                seg_count += remainder

            return total_tokens / seg_count if seg_count else 0

        forward = mtld_pass(tokens)
        backward = mtld_pass(list(reversed(tokens)))
        return (forward + backward) / 2

    def __calculate_vocd(self, doc: Doc) -> float:
        """
        This method return the Vocabulary Complexity Diversity (VoCD) of a text.

        Parameters:
        doc(Doc): The text to be anaylized.

        Returns:
        float: The Vocabulary Complexity Diversity (VoCD) of a text.
        """
        n_iterations = 3
        n_min = 36
        n_max = 50
        tokens = [word.text.lower() for word in doc._.alpha_words]

        if len(tokens) < n_max:
            return 0

        def ttr_model(N, D):
            return (D / N) * (np.sqrt(1 + 2 * (N / D)) - 1) if D > 0 else 0

        def ttr_mean(n_tokens: int, samples=100):
            ttrs = []
            for _ in range(samples):
                sample = random.sample(tokens, n_tokens)
                ttrs.append(len(set(sample)) / n_tokens)
            return float(np.mean(ttrs))

        fitted_d = []
        for _ in range(n_iterations):
            n_tokens = list(range(n_min, n_max + 1))
            ttrs = [ttr_mean(n) for n in n_tokens]
            popt, _ = curve_fit(ttr_model, n_tokens, ttrs)
            fitted_d.append(popt[0])

        return float(np.mean(fitted_d))

    def __get_type_token_ratio_between_all_words(self, doc: Doc) -> float:
        """
        This method returns the type token ratio between all words of a text.

        Parameters:
        doc(Doc): The text to be anaylized.

        Returns:
        float: The type token ratio between all words of a text.
        """
        return (
            0
            if doc._.alpha_words_count == 0
            else doc._.alpha_words_different_count / doc._.alpha_words_count
        )

    def __get_type_token_ratio_of_content_words(self, doc: Doc) -> float:
        """
        This method returns the type token ratio of content words of a text. Content words are nouns, verbs, adjectives and adverbs.

        Parameters:
        doc(Doc): The text to be anaylized.

        Returns:
        float: The type token ratio between the content words of a text.
        """
        return (
            0
            if doc._.content_words_count == 0
            else doc._.content_words_different_count / doc._.content_words_count
        )

    def __get_type_token_ratio_of_nouns(self, doc: Doc) -> float:
        """
        This method returns the type token ratio of nouns of a text.

        Parameters:
        doc(Doc): The text to be anaylized.

        Returns:
        float: The type token ratio between the nouns of a text.
        """
        return (
            0
            if doc._.nouns_count == 0
            else len(set([word.text.lower() for word in doc._.nouns]))
            / doc._.nouns_count
        )

    def __get_type_token_ratio_of_verbs(self, doc: Doc) -> float:
        """
        This method returns the type token ratio of verbs of a text.

        Parameters:
        doc(Doc): The text to be anaylized.

        Returns:
        float: The type token ratio between the verbs of a text.
        """
        return (
            0
            if doc._.verbs_count == 0
            else len(set([word.text.lower() for word in doc._.verbs]))
            / doc._.verbs_count
        )

    def __get_type_token_ratio_of_adverbs(self, doc: Doc) -> float:
        """
        This method returns the type token ratio of adverbs of a text.

        Parameters:
        doc(Doc): The text to be anaylized.

        Returns:
        float: The type token ratio between the adverbs of a text.
        """
        return (
            0
            if doc._.adverbs_count == 0
            else len(set([word.text.lower() for word in doc._.adverbs]))
            / doc._.adverbs_count
        )

    def __get_type_token_ratio_of_adjectives(self, doc: Doc) -> float:
        """
        This method returns the type token ratio of adjectives of a text.

        Parameters:
        doc(Doc): The text to be anaylized.

        Returns:
        float: The type token ratio between the adjectives of a text.
        """
        return (
            0
            if doc._.adjectives_count == 0
            else len(set([word.text.lower() for word in doc._.adjectives]))
            / doc._.adjectives_count
        )

    def __get_type_token_ratio_between_all_lemma_words(self, doc: Doc) -> float:
        """
        This method returns the type token ratio of all lemma words of a text.

        Parameters:
        doc(Doc): The text to be anaylized.

        Returns:
        float: The type token ratio between all lemma words of a text.
        """
        return (
            0
            if doc._.alpha_words_count == 0
            else len(set([word.lemma_ for word in doc._.alpha_words]))
            / doc._.alpha_words_count
        )

    def __get_type_token_ratio_of_lemma_nouns(self, doc: Doc) -> float:
        """
        This method returns the type token ratio of lemma nouns of a text.

        Parameters:
        doc(Doc): The text to be anaylized.

        Returns:
        float: The type token ratio between the lemma nouns of a text.
        """
        return (
            0
            if doc._.nouns_count == 0
            else len(set([word.lemma_ for word in doc._.nouns])) / doc._.nouns_count
        )

    def __get_type_token_ratio_of_lemma_verbs(self, doc: Doc) -> float:
        """
        This method returns the type token ratio of lemma verbs of a text.

        Parameters:
        doc(Doc): The text to be anaylized.

        Returns:
        float: The type token ratio between the lemma verbs of a text.
        """
        return (
            0
            if doc._.verbs_count == 0
            else len(set([word.lemma_ for word in doc._.verbs])) / doc._.verbs_count
        )

    def __get_type_token_ratio_of_lemma_adverbs(self, doc: Doc) -> float:
        """
        This method returns the type token ratio of lemma adverbs of a text.

        Parameters:
        doc(Doc): The text to be anaylized.

        Returns:
        float: The type token ratio between the lemma adverbs of a text.
        """
        return (
            0
            if doc._.adverbs_count == 0
            else len(set([word.lemma_ for word in doc._.adverbs])) / doc._.adverbs_count
        )

    def __get_type_token_ratio_of_lemma_adjectives(self, doc: Doc) -> float:
        """
        This method returns the type token ratio of lemma adjectives of a text.

        Parameters:
        doc(Doc): The text to be anaylized.

        Returns:
        float: The type token ratio between the lemma adjectives of a text.
        """
        return (
            0
            if doc._.adjectives_count == 0
            else len(set([word.lemma_ for word in doc._.adjectives]))
            / doc._.adjectives_count
        )

    def __get_type_token_ratio_of_pronouns(self, doc: Doc) -> float:
        """
        This method returns the type token ratio of pronouns of a text.

        Parameters:
        doc(Doc): The text to be anaylized.

        Returns:
        float: The type token ratio between the pronouns of a text.
        """
        return (
            0
            if doc._.pronouns_count == 0
            else len(set([word.text.lower() for word in doc._.pronouns]))
            / doc._.pronouns_count
        )

    def __get_type_token_ratio_of_pronouns_relative(self, doc: Doc) -> float:
        """
        This method returns the type token ratio of relative pronouns of a text.

        Parameters:
        doc(Doc): The text to be anaylized.

        Returns:
        float: The type token ratio between the relative pronouns of a text.
        """
        return (
            0
            if doc._.pronouns_relative_count == 0
            else len(set([word.text.lower() for word in doc._.pronouns_relative]))
            / doc._.pronouns_relative_count
        )

    def __get_type_token_ratio_of_pronouns_indefinite(self, doc: Doc) -> float:
        """
        This method returns the type token ratio of indefinite pronouns of a text.

        Parameters:
        doc(Doc): The text to be anaylized.

        Returns:
        float: The type token ratio between the indefinite pronouns of a text.
        """
        return (
            0
            if doc._.pronouns_indefinite_count == 0
            else len(set([word.text.lower() for word in doc._.pronouns_indefinite]))
            / doc._.pronouns_indefinite_count
        )

    def __get_type_token_ratio_of_functional_words(self, doc: Doc) -> float:
        """
        This method returns the type token ratio of functional words of a text.

        Parameters:
        doc(Doc): The text to be anaylized.

        Returns:
        float: The type token ratio between the functional words of a text.
        """
        return (
            0
            if doc._.functors_count == 0
            else len(set([word.text.lower() for word in doc._.functors]))
            / doc._.functors_count
        )

    def __get_noun_density(self, doc: Doc) -> float:
        """
        This method returns the noun density of a text.

        Parameters:
        doc(Doc): The text to be anaylized.

        Returns:
        float: The type token ratio between the content words of a text.
        """
        return (
            0
            if doc._.alpha_words_count == 0
            else doc._.nouns_count / doc._.alpha_words_count
        )

    def __get_verb_density(self, doc: Doc) -> float:
        """
        This method returns the verb density of a text.

        Parameters:
        doc(Doc): The text to be anaylized.

        Returns:
        float: The type token ratio between the content words of a text.
        """
        return (
            0
            if doc._.content_words_count == 0
            else doc._.verbs_count / doc._.content_words_count
        )

    def __get_adverb_density(self, doc: Doc) -> float:
        """
        This method returns the adverb density of a text.

        Parameters:
        doc(Doc): The text to be anaylized.

        Returns:
        float: The type token ratio between the content words of a text.
        """
        return (
            0
            if doc._.content_words_count == 0
            else doc._.adverbs_count / doc._.content_words_count
        )

    def __get_adjective_density(self, doc: Doc) -> float:
        """
        This method returns the adjective density of a text.

        Parameters:
        doc(Doc): The text to be anaylized.

        Returns:
        float: The type token ratio between the content words of a text.
        """
        return (
            0
            if doc._.content_words_count == 0
            else doc._.adjectives_count / doc._.content_words_count
        )
