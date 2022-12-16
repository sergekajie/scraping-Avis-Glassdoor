
import logging
import sys


n_pages=14
output_reviews_path = "data/reviews_data.xlsx"
output_processed_reviews_path = "data/df_reviews_processed.xlsx"
output_pros_processed_path = "data/pros_df.xlsx"
output_cons_processed_path = "data/cons_df.xlsx"

def get_logger(name):
    logging.basicConfig(stream=sys.stdout,format='%(asctime)s - %(levelname)s - %(name)s - %(message)s', level=logging.INFO)
    logger = logging.getLogger(name)
    return logger
