from pprint import pprint

from iapucp_metrix.analyzer import Analyzer


def test_dummy():
    texts = [
        "Tenia que comer mucho. El sol se escondió tras el horizonte lentamente, tiñendo el cielo de tonos naranjas y rosados. Una brisa suave movía las hojas, susurrando la promesa de una noche tranquila.\n\nEn la tranquila biblioteca, el polvo flotaba a través de los rayos de luz. Las filas de libros se erguían como centinelas silenciosos, cada uno guardando un mundo esperando ser explorado."
    ]
    analyzer = Analyzer()

    docs = analyzer.analyze(texts)
    for doc in docs:
        pprint(doc._.coh_metrix_indices)
        for verb in doc._.verbs:
            pprint.print("Verb", verb.text, verb._.tag, verb._.tag_)
        print(f"Number of metrics: {len(doc._.coh_metrix_indices)}")
        assert doc._.coh_metrix_indices["DESPC"] == 2
