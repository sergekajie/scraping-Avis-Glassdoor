import requests
from bs4 import BeautifulSoup as soup
import pandas as pd
import config

logger = config.get_logger("main")


def get_all_reviews(n_pages=config.n_pages, logger=logger):
    """
    Return all reviews
    :param n_pages: numbers of pages where we have reviews
    :return: a dataframe with all reviews
    """
    all_reviews_data = pd.DataFrame()

    # extract reviews for each pages
    for i in range(1, n_pages + 1):
        logger.info(f"Page {i} : {config.url_prefix}{i}{config.url_suffix}")
        soup_data = get_soup_data(url_reviews=f"{config.url_prefix}{i}{config.url_suffix}")
        reviews_data = get_reviews(soup_data)
        all_reviews_data = pd.concat([all_reviews_data, reviews_data], ignore_index=True)

    ### load data ###
    logger.info(f"Saving {len(all_reviews_data)} reviews into {config.output_reviews_path}")
    all_reviews_data.to_excel(config.output_reviews_path, index=False)

    return all_reviews_data


def get_soup_data(url_reviews):
    """
    Get and parsed the html content 
    :param url_reviews: url of reviews
    :return: html content parsed
    """
    html_data = requests.get(url=url_reviews, headers=config.headers)
    soup_data = soup(html_data.content, "html.parser")

    return soup_data


def get_reviews(soup_data):
    """
    :param soup_data: html content parsed
    :return: Reviews on a particular page
    """
    ### Extract ###
    note = [note.text for note in soup_data.findAll("span", {"class": "ratingNumber mr-xsm"})]
    statut = [statut.text for statut in soup_data.findAll("span", {"class": "pt-xsm pt-md-0 css-1qxtz39 eg4psks0"})]
    appreciation_generale = [app.text for app in soup_data.findAll("a", {"class": "reviewLink"})]
    date_and_positions = get_date_position(soup_data)
    recommandations = get_recommandations(soup_data)
    pros = [advantage.text for advantage in soup_data.findAll("span", {"data-test": "pros"})]
    cons = [disadvantage.text for disadvantage in soup_data.findAll("span", {"data-test": "cons"})]

    reviews_data = pd.DataFrame(data={
        "note": note,
        "statut": statut,
        "appreciation_generale": appreciation_generale,
        "date_and_positions": date_and_positions,
        "recommandations": recommandations,
        "pros": pros,
        "cons": cons
    })

    ### Transform ###
    if not reviews_data.empty:

        reviews_data[["date", "position"]] = reviews_data.date_and_positions.apply(lambda row: row.split("-")).apply(pd.Series)
        reviews_data[["recommander", "approbation_pdg", "perpective_commerciale"]] = reviews_data.recommandations.apply(pd.Series)

        reviews_data["recommander"] = reviews_data["recommander"].map({"path": True, "rect": False, "circle": None})
        reviews_data["approbation_pdg"] = reviews_data["approbation_pdg"].map({"path": True, "rect": False, "circle": None})
        reviews_data["perpective_commerciale"] = reviews_data["perpective_commerciale"].map({"path": True, "rect": False, "circle": None})

        reviews_data["note"] = reviews_data["note"].apply(lambda row: float(row.replace(",", ".")))
        reviews_data["date"] = pd.to_datetime(reviews_data["date"].str.strip(), format="%b %d, %Y")

        reviews_data = reviews_data.drop(columns=["date_and_positions", "recommandations"])

        # drop spaces at the end and beginning of each text
        reviews_data[['statut', 'appreciation_generale', 'pros', 'cons', 'position', ]] = \
            reviews_data[['statut', 'appreciation_generale', 'pros', 'cons', 'position']].applymap(lambda cell: cell.strip() if cell is not None else cell)

    return reviews_data


def get_date_position(soup_data):
    """
    :param soup_data: html content parsed
    :return: date of the review and location of the person who wrote the post
    """
    poste_date_and_location = soup_data.findAll("span", {"class": "common__EiReviewDetailsStyle__newUiJobLine"})
    possitions_and_date = [poste.findAll('span', {"class": "authorJobTitle middle common__EiReviewDetailsStyle__newGrey"})[0].text for poste in poste_date_and_location]

    return possitions_and_date


def get_recommandations(soup_data):
    """
    :param soup_data: html content parsed
    :return: recommandations
    """
    recommandations = soup_data.findAll("div", attrs={"class": "d-flex my-std reviewBodyCell recommends css-1y3jl3a e1868oi10"})
    recommandations = [rec.findAll("svg") for rec in recommandations]
    recommandations = [[rec.findChild().name for rec in r] for r in recommandations]

    return recommandations


def get_salary():
    pass


def get_social_advantages():
    pass


if __name__ == "__main__":
    get_all_reviews()
