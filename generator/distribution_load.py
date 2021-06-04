import sys
import pandas as pd


def load_distribution(path, logger):
    logger.info(f"Loading movies distribution from '{path}'...")
    df = pd.read_csv(path)
    logger.info("Transforming distribution data...")
    movie_dist = {}
    for index, row in df.iterrows():
        movie_id = row.movieId
        try:
            movie_data = movie_dist[movie_id]
        except:
            movie_data = {"rating": [], "prob": []}
            movie_dist[movie_id] = movie_data
        movie_data["rating"].append(row.rating)
        movie_data["prob"].append(row.prob)
    logger.info("Movie distribution load completed")
    return movie_dist


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Expecting input a file to load")
    else:
        import logging

        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger("main")
        load_distribution(sys.argv[1], logger)
