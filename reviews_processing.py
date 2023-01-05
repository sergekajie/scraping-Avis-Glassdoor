
import pandas as pd
import position_mapping
import re
import warnings
import config
import sentiment_classification

warnings.filterwarnings("ignore")
logger = config.get_logger("main")


def statut_processing(df_reviews):
    """
    Détermine le statut (ancien/nouveau employé) et l'ancienneté
    :param df_reviews:
    :return:
    """
    df_reviews["statut_actuel_ancien_employe"] = df_reviews["statut"].apply(lambda statut: statut.split(",")[0])
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


def pros_processing(df_reviews):
    # df_reviews["pros_rec"] = df_reviews["pros"].apply(lambda pros: pros.replace("\n", "; ").replace("\r", "; "))
    df_reviews["pros_rec"] = df_reviews["pros"].apply(lambda pros: re.split(r"\n|\r|,", pros))
    return df_reviews


def cons_processing(df_reviews):
    # df_reviews["cons_rec"] = df_reviews["cons"].apply(lambda pros: pros.replace("\n", "; ").replace("\r", "; "))
    df_reviews["cons_rec"] = df_reviews["cons"].apply(lambda cons: re.split(r"\n|\r|,", cons))

    return df_reviews


def reviews_processing(logger=logger):

    ### Extract ###
    logger.info("Reading reviews scrapped")
    df_reviews = pd.read_excel(config.output_reviews_path)

    ### Transform ###
    logger.info("Statut processing")
    df_reviews = statut_processing(df_reviews)

    logger.info("Position processing")
    df_reviews = position_processing(df_reviews)

    logger.info("Location processing")
    df_reviews = location_processing(df_reviews)

    logger.info("Appreciation processing")
    df_reviews = appreciation_processing(df_reviews)

    ### Load Data ###
    logger.info(f"Saving {len(df_reviews)} processed reviews")
    df_reviews.to_excel(config.output_processed_reviews_path, index=False)


if __name__ == "__main__":
    reviews_processing()
