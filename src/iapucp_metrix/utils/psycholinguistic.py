from importlib.resources import files

import pandas as pd


class PsycholinguisticBank:
    """
    Dataset of psycholinguistic ratings, contains concreteness, imageability, familiarity, valence and arousal.
    """

    def __init__(self):
        models_dir = files("iapucp_metrix.models")
        espal_path = str(models_dir / "espal.csv")
        stadthagen_path = str(models_dir / "stadthagen.csv")
        alonso_path = str(models_dir / "alonso.csv")

        self.espal_df = pd.read_csv(espal_path)
        self.stadthagen_df = pd.read_csv(stadthagen_path)
        self.alonso_df = pd.read_csv(alonso_path)

        self.espal_df.set_index("word", inplace=True)
        self.stadthagen_df.set_index("word", inplace=True)
        self.alonso_df.set_index("word", inplace=True)

    def get_ratings(self, word: str) -> dict:
        ratings = {}
        word = word.lower()
        if word in self.espal_df.index:
            e = self.espal_df.loc[word]
            ratings.update(
                {
                    "concreteness": e["concreteness"],
                    "imageability": e["imageability"],
                    "familiarity": e["familiarity"],
                }
            )
        if word in self.stadthagen_df.index:
            s = self.stadthagen_df.loc[word]
            ratings.update(
                {
                    "valence": s["valence"],
                    "arousal": s["arousal"],
                }
            )
        if word in self.alonso_df.index:
            a = self.alonso_df.loc[word]
            ratings["aoa"] = a["aoa"]

        return ratings


PSY_BANK = PsycholinguisticBank()
