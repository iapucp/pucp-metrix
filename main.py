import spacy


def main():
    texts = ["Este es un texto de prueba. Otra sentencia."]
    nlp = spacy.load("es_core_news_lg")

    for doc in nlp.pipe(texts):
        print(doc.text)
        for sent in doc.sents:
            print(sent.text)


if __name__ == "__main__":
    main()
