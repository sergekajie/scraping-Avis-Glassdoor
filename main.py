
import reviews_scrapping
import reviews_processing
import pros_and_cons_processing
import config

logger = config.get_logger("main")


def main():

    logger.info("_____________BEGIN________________")
    logger.info(f"scrapping all reviews")
    reviews_scrapping.get_all_reviews(n_pages=config.n_pages, logger=logger)
    logger.info("___________________________________________")

    logger.info("Processing reviews")
    reviews_processing.reviews_processing(logger=logger)
    logger.info("___________________________________________")

    logger.info("Processing pros and cons")
    pros_and_cons_processing.pros_cons_processing(logger=logger)
    logger.info("___________________________________________")
    logger.info("_____________FINISHED________________")


if __name__ == "__main__":
    main()