
import logging
import sys

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"}

n_pages=17  # il y a 10 avis par page

output_reviews_path = "data/TNP/reviews_data.xlsx"
output_processed_reviews_path = "data/TNP/df_reviews_processed.xlsx"
output_pros_processed_path = "data/TNP/pros_df.xlsx"
output_cons_processed_path = "data/TNP/cons_df.xlsx"

cabinet = "TNP"  # TNP or EY


if cabinet == "TNP":
    url_prefix = "https://www.glassdoor.fr/Avis/TNP-Consultants-Avis-E455516_P"
    url_suffix = ".htm?filter.iso3Language=fra"
else:
    url_prefix = "https://www.glassdoor.fr/Avis/EY-Avis-E2784_P"
    url_suffix = ".htm?filter.iso3Language=fra"


def get_logger(name):
    logging.basicConfig(stream=sys.stdout,format='%(asctime)s - %(levelname)s - %(name)s - %(message)s', level=logging.INFO)
    logger = logging.getLogger(name)
    return logger
