import requests
from bs4 import BeautifulSoup as soup
import pandas as pd

# headers = ""
ouput_path = "data/reviews_data.xlsx"


def get_all_reviews(n_pages=14):
    """
    Return all reviews
    :param n_pages: numbers of pages where we have reviews
    :return: a dataframe with all reviews
    """
    all_reviews_data = pd.DataFrame()

    # extract reviews for each pages
    for i in range(1, n_pages + 1):
        print(f"Page {i} : https://www.glassdoor.fr/Avis/TNP-Consultants-Avis-E455516_P{i}.htm?filter.iso3Language=fra")
        soup_data = get_soup_data(url_reviews=f"https://www.glassdoor.fr/Avis/TNP-Consultants-Avis-E455516_P{i}.htm?filter.iso3Language=fra")
        reviews_data = get_reviews(soup_data)
        all_reviews_data = pd.concat([all_reviews_data, reviews_data], ignore_index=True)

    ### load data ###
    all_reviews_data.to_excel(ouput_path, index=False)

    return all_reviews_data


def get_soup_data(url_reviews):
    """
    :param url_reviews: url of reviews
    :return: html content parsed
    """
    html_data = requests.get(url=url_reviews)
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
    date_and_positions, locations = get_date_position_location(soup_data)
    recommandations = get_recommandations(soup_data)
    pros = [advantage.text for advantage in soup_data.findAll("span", {"data-test": "pros"})]
    cons = [disadvantage.text for disadvantage in soup_data.findAll("span", {"data-test": "cons"})]

    reviews_data = pd.DataFrame(data={
        "note": note,
        "statut": statut,
        "appreciation_generale": appreciation_generale,
        "date_and_positions": date_and_positions,
        "location": locations,
        "recommandations": recommandations,
        "pros": pros,
        "cons": cons
    })

    ### Transform ###
    reviews_data[["date", "position"]] = reviews_data.date_and_positions.apply(lambda row: row.split("-")).apply(pd.Series)
    reviews_data[["recommander", "approbation_pdg", "perpective_commerciale"]] = reviews_data.recommandations.apply(pd.Series)

    reviews_data["recommander"] = reviews_data["recommander"].map({"path": True, "rect": False, "circle": None})
    reviews_data["approbation_pdg"] = reviews_data["approbation_pdg"].map({"path": True, "rect": False, "circle": None})
    reviews_data["perpective_commerciale"] = reviews_data["perpective_commerciale"].map({"path": True, "rect": False, "circle": None})

    reviews_data["note"] = reviews_data["note"].apply(lambda row: float(row.replace(",", ".")))
    reviews_data["date"] = pd.to_datetime(reviews_data["date"].str.strip(), format="%d %b %Y")

    reviews_data = reviews_data.drop(columns=["date_and_positions", "recommandations"])

    # drop spaces at the end and beginning of each text
    reviews_data[['statut', 'appreciation_generale', 'location', 'pros', 'cons', 'position', ]] = \
        reviews_data[['statut', 'appreciation_generale', 'location', 'pros', 'cons', 'position']].applymap(lambda cell: cell.strip() if cell is not None else cell)

    return reviews_data


def get_date_position_location(soup_data):
    """
    :param soup_data: html content parsed
    :return: date of the review and location of the person who wrote the post
    """
    poste_date_and_location = soup_data.findAll("span", {"class": "common__EiReviewDetailsStyle__newUiJobLine"})
    possitions_and_date = [poste.findAll('span', {"class": "middle common__EiReviewDetailsStyle__newGrey"})[0].text for poste in poste_date_and_location]

    all_values = [loc.findAll("span", {"class": "middle"}) for loc in poste_date_and_location]
    locations = [loc[1] if len(loc) > 1 else None for loc in all_values]
    locations = [loc.find("span").text if loc is not None else None for loc in locations]

    return possitions_and_date, locations


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
    get_all_reviews(n_pages=14)
