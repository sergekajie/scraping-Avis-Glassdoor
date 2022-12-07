# https://linogaliana-teaching.netlify.app/lda/
# import numpy as np
import pandas as pd
import position_mapping
import sentiment_classification

# load datasets
df_reviews = pd.read_excel("data/reviews_data.xlsx")


def statut_processing(df_reviews):
    """
    Détermine le statut (ancien/nouveau employé) et l'ancienneté
    :param df_reviews:
    :return:
    """
    df_reviews["statut_date"] = df_reviews["statut"].apply(lambda statut: statut.split(",")[0])
    df_reviews["statut_anciennete"] = df_reviews["statut"].apply(lambda statut: statut.split(",")[1].strip() if len(statut.split(",")) > 1 else None)
    return df_reviews


def position_processing(df_reviews):
    """
    Recode la position des employés ayant répondu
    """
    df_reviews["position_rec"] = df_reviews["position"].replace(position_mapping.position_mapping)
    return df_reviews


def location_processing(df_reviews):
    """
    Recode la localisation de l'employé (ou son pole de rattachement)
    :param df_reviews:
    :return:
    """
    df_reviews["location_rec"] = df_reviews.location.replace({"Neuilly": "Paris", "Cormeilles": "Paris"})
    return df_reviews


def pros_processing(df_reviews):
    df_reviews["pros_rec"] = df_reviews["pros"].apply(lambda pros: pros.replace("\n", "; ").replace("\r", "; "))
    return df_reviews


def cons_processing(df_reviews):
    df_reviews["cons_rec"] = df_reviews["cons"].apply(lambda pros: pros.replace("\n", "; ").replace("\r", "; "))
    return df_reviews

def text_processing(text):
    text = "Le Maroc et l’Espagne seront face à face mardi 6 décembre dans l'après-midi en huitièmes " \
           "de finale de la Coupe du monde. Encore un match à forte dimension politique. Pour des tas de " \
           "raisons. C’est sans doute le match le plus politique de ces huitièmes de finale."

    text = "Organisation hiérarchique orientée résultat au détriment de l’évolution et de la progression"
    # from spacy.lang.fr import French
    from spacy.lang.fr.stop_words import STOP_WORDS
    import spacy

    # nlp = French()
    nlp = spacy.load("fr_core_news_sm")
    doc = nlp(text)



    pos = [tok.pos_ for tok in doc ] #if tok.text not in STOP_WORDS]


    # delete stopwords
    tokens = [tok.text for tok in doc if tok.text not in STOP_WORDS]

    # lemmatization
    lems = [tok.lemma_ for tok in doc if tok.text not in STOP_WORDS and tok.pos_ in ["NOUN", "ADJ"]]

    # pos tagging


def appreciation_processing(df_reviews):
    """
    classifie l'appréciation générale en deux catégories (positif et négatif)
    :param df_reviews:
    :return:
    """
    df_reviews["sentiment"] = df_reviews["appreciation_generale"].apply(sentiment_classification.get_sentiment)
    df_reviews["sentiment_rec"] = df_reviews["sentiment"].replace({"positive": "positif",
                                                                   "very_positive": "positif",
                                                                   "negative": "négatif",
                                                                   "very_negative": 'négatif',
                                                                   "mixed": "négatif"
                                                                   })
    return df_reviews