
"""
Ce module prépare les avantages et inconvénients qui seront importés dans Power BI pour le wordcloud 
des avantages et inconvénients
"""

import pandas as pd
from spacy.lang.fr.stop_words import STOP_WORDS
import spacy
from nltk import ngrams
import re
from nltk.stem.snowball import SnowballStemmer
from unidecode import unidecode
import config

logger = config.get_logger("main")
stemmer = SnowballStemmer(language='french')
# nlp = spacy.lang.fr.French()
nlp = spacy.load("fr_core_news_sm")


def pros_processing(df_reviews):
    """
    Les avantages sont divisés par n-grams (n allant de 1 à 3 selon la longueur du texte d'entrée)
    Un avantage en sortie est présent autant de fois qu'il a été cité
    """
    all_pros = (
        [
            pro.replace("- ", "").replace("/", " ").strip() 
            for i in df_reviews["pros"].apply(lambda pros: re.split(r"\n|\r|,", pros)).tolist() 
            for pro in i
        ]
    )
    from unidecode import unidecode

    all_pros_processed = [
        unidecode(" ".join([tok.lemma_.lower() for tok in nlp(pros) if tok.pos_ in ["NOUN", "ADJ", "ADV", "PROPN"]])) 
        # unidecode(" ".join([stemmer.stem(str(tok.text)) for tok in nlp(pros) if tok.pos_ in ["NOUN", "ADJ", "ADV", "PROPN"]])) 
        for pros in all_pros
    ]

    all_pros_processed_with_ngrams = []

    for pros in all_pros_processed:
        if len(pros.split(" ")) >= 3:
            all_pros_processed_with_ngrams = all_pros_processed_with_ngrams + [" ".join(bigram) for bigram in ngrams(pros.split(" "), 3) if pros != ""]
        elif len(pros.split(" ")) >= 2:
            all_pros_processed_with_ngrams = all_pros_processed_with_ngrams + [" ".join(bigram) for bigram in ngrams(pros.split(" "), 2) if pros != ""]
        else:
            all_pros_processed_with_ngrams = all_pros_processed_with_ngrams + [" ".join(bigram) for bigram in ngrams(pros.split(" "), 1) if pros != ""]

    return all_pros_processed_with_ngrams


def cons_processing(df_reviews):
    """
    Les inconvénients sont divisés par n-grams (n allant de 1 à 3 selon la longueur du texte d'entrée)
    Un inconvénient en sortie est présent autant de fois qu'il a été cité
    """
    all_cons = (
        [
            pro.replace("- ", "").replace("/", " ").strip() 
            for i in df_reviews["cons"].apply(lambda cons: re.split(r"\n|\r|,", cons)).tolist() 
            for pro in i
        ]
    )

    all_cons_processed = [
        unidecode(" ".join([tok.lemma_.lower() for tok in nlp(cons) if tok.pos_ in ["NOUN", "ADJ", "ADV", "PROPN"]])) 
        for cons in all_cons
    ]

    all_cons_processed_with_ngrams = []

    for cons in all_cons_processed:
        if len(cons.split(" ")) >= 4:
            all_cons_processed_with_ngrams = all_cons_processed_with_ngrams + [" ".join(bigram) for bigram in ngrams(cons.split(" "), 3) if cons != ""]
        elif len(cons.split(" ")) >= 3:
            all_cons_processed_with_ngrams = all_cons_processed_with_ngrams + [" ".join(bigram) for bigram in ngrams(cons.split(" "), 3) if cons != ""]
        elif len(cons.split(" ")) >= 2:
            all_cons_processed_with_ngrams = all_cons_processed_with_ngrams + [" ".join(bigram) for bigram in ngrams(cons.split(" "), 2) if cons != ""]
        else:
            all_cons_processed_with_ngrams = all_cons_processed_with_ngrams + [" ".join(bigram) for bigram in ngrams(cons.split(" "), 1) if cons != ""]

    return all_cons_processed_with_ngrams


def pros_cons_processing(logger=logger):

    ### Extract ###
    logger.info("Reading reviews scrapped")
    df_reviews = pd.read_excel(config.output_reviews_path)

    ### Transform ###
    logger.info("Pros processing")
    all_pros_processed_with_ngrams = pros_processing(df_reviews)

    logger.info("Cons processing")
    all_cons_processed_with_ngrams = cons_processing(df_reviews)

    ### Load ###
    logger.info("Saving Pros and Cons processid into data folder")
    pd.DataFrame(all_pros_processed_with_ngrams, columns=["pros"]).to_excel(config.output_pros_processed_path, index=False)
    pd.DataFrame(all_cons_processed_with_ngrams, columns=["cons"]).to_excel(config.output_cons_processed_path, index=False)


if __name__ == "__main__":
    pros_cons_processing()
