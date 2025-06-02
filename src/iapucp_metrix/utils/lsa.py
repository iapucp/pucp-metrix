from datasets import load_dataset
from gensim import corpora
from gensim.corpora import Dictionary
from gensim.matutils import cossim
from gensim.models import LsiModel
from spacy.language import Language
from spacy.tokens import Doc, Span


class LsaModel:
    """
    LSA model for computing similarity between Spans or Documents.
    """

    def __init__(
        self, nlp: Language, model_path: str = None, dictionary_path: str = None
    ):
        """
        The constructor will load the trained LSA model and the dictionary.

        Parameters:
        nlp(Language): The spacy model that corresponds to a language.
        model_path(str): Path to the trained LSA model.
        dictionary_path(str): Path to the trained LSA dictionary.

        Returns:
        None.
        """
        self._model = LsiModel.load(model_path) if model_path else None
        self._dictionary = Dictionary.load(dictionary_path) if dictionary_path else None
        self._nlp = nlp

    def compute_similarity(self, doc1: Doc | Span, doc2: Doc | Span) -> float:
        """
        This method will compute the similarity between two documents or two spans.

        Parameters:
        doc1(Doc | Span): The first document or span to compare.
        doc2(Doc | Span): The second document or span to compare.

        Returns:
        float: The cosine similarity between the two documents or spans, between -1 and 1.
        """
        if not self._model or not self._dictionary:
            raise ValueError("LSA model not trained")

        bow1 = self._model[self._dictionary.doc2bow(self.preprocess_doc(doc1))]
        bow2 = self._model[self._dictionary.doc2bow(self.preprocess_doc(doc2))]
        return cossim(bow1, bow2)

    def train(self):
        """
        This method will train the LSA model and save it for later use.

        Parameters:
        None.

        Returns:
        None.
        """
        dataset = load_dataset("crscardellino/spanish_billion_words")

        print("Loading the corpus and preprocessing the texts")

        # Load the corpus and preprocess the texts
        texts = [data["text"] for data in dataset["train"]]

        print("Number of documents", len(texts))

        documents = self.preprocess_text_batch(texts)

        # documents = [
        #     self.preprocess_text(" ".join(words)) for words in cess_esp.sents()
        # ]

        self._dictionary = corpora.Dictionary(documents)

        # Convert the processed documents into BoW format (Bag-of-Words)
        corpus = [self._dictionary.doc2bow(doc) for doc in documents]

        print("Training the LSA model")

        self._model = LsiModel(corpus, id2word=self._dictionary, num_topics=400)

        print("Saving the LSA model and dictionary")

        self._model.save("lsa_model.gensim")
        self._dictionary.save("lsa_dictionary.gensim")

    def preprocess_text(self, text: str) -> list[str]:
        """
        This method will preprocess a text to remove stop words and punctuation.

        Parameters:
        text(str): The text to preprocess.

        Returns:
        list[str]: List of tokens
        """
        doc = self._nlp(text)
        return [
            token.lemma_.lower()
            for token in doc
            if token.is_alpha and not token.is_stop
        ]

    def preprocess_text_batch(self, texts: list[str]) -> list[list[str]]:
        """
        This method will preprocess a list of texts to remove stop words and punctuation.

        Parameters:
        texts(list[str]): List of texts to preprocess.

        Returns:
        list[list[str]]: List of lists of tokens
        """
        docs = self._nlp.pipe(texts, n_process=8)
        tokens = []
        for doc in docs:
            tokens.append(
                [
                    token.lemma_.lower()
                    for token in doc
                    if token.is_alpha and not token.is_stop
                ]
            )

        return tokens

    def preprocess_doc(self, doc: Doc | Span) -> list[str]:
        """
        This method will preprocess a spacy Doc or Span to remove stop words and punctuation.

        Parameters:
        doc(Doc | Span): The document to preprocess.

        Returns:
        list[str]: List of tokens
        """
        return [
            token.lemma_.lower()
            for token in doc
            if token.is_alpha and not token.is_stop
        ]


if __name__ == "__main__":
    import spacy

    nlp = spacy.load("es_core_news_lg")
    lsa_model = LsaModel(nlp)
    lsa_model.train()
    print(
        lsa_model.compute_similarity(
            nlp("El pescado es un animal de gran tamaño."),
            nlp("El pescado es un animal grande."),
        )
    )
