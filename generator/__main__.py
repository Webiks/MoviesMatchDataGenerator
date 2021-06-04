import logging
from generator.logger import setup_logger
from generator.configuration import Config
from generator.distribution_load import load_distribution
from generator.generate import start_records_generation

if __name__ == "__main__":
    print("Loading configuration...")
    config = Config()

    setup_logger(config.log_level)
    logger = logging.getLogger("main")
    logger.info(
        f"Starting generator with following configuration: {config.get_sanitized()}"
    )

    movie_dist = load_distribution(config.movies_ratings_distribution_file, logger)

    logger.info("Starting records generation")
    start_records_generation(config, movie_dist, logger)
