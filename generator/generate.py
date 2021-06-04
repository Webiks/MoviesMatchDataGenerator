from time import sleep
from uuid import uuid4
import pandas as pd
import numpy as np


def geneate_record(config, movie_dist, movie_ids, transaction_id, logger):
    is_new_user = np.random.uniform() < config.new_user_rating_prob
    if is_new_user:
        first_id = config.existing_users_first_id
        last_id = config.existing_users_last_id
    else:
        first_id = config.new_users_first_id
        last_id = config.new_users_last_id
    user_id = np.random.randint(first_id, last_id + 1)

    movie_index = np.random.randint(0, len(movie_ids))
    movie_id = int(movie_ids[movie_index])

    dist = movie_dist[movie_id]
    rating = np.random.choice(dist["rating"], p=dist["prob"])

    logger.debug(
        f"Generating record for new_user={is_new_user}, user_id={user_id}, "
        f"movie_id={movie_id}, probs={dist['prob']}, rating={rating}",
        extra={"transaction_id": transaction_id},
    )
    return [user_id, movie_id, rating]


def generate_records(config, movie_dist, movie_ids, logger):
    transaction_id = uuid4()
    logger.info("Generating records", extra={"transaction_id": transaction_id})

    records_count = config.records_to_generate
    if config.records_to_generate_jitter:
        jitter = config.records_to_generate_jitter
        records_count += np.random.randint(-jitter, jitter + 1)
        records_count = max(records_count, 1)
    logger.info(
        f"Creating {records_count} records...", extra={"transaction_id": transaction_id}
    )

    records = []
    for _ in range(records_count):
        records.append(
            geneate_record(config, movie_dist, movie_ids, transaction_id, logger)
        )

    df = pd.DataFrame(records, columns=["user_id", "movie_id", "rating"])
    logger.debug(
        f"Data frame head:\n{df.head()}", extra={"transaction_id": transaction_id}
    )
    # TODO stream records
    return transaction_id


def get_sleep_interval(config):
    interval = config.generate_interval_sec
    if config.generate_interval_jitter_sec:
        jitter = config.generate_interval_jitter_sec
        interval += np.random.uniform(-jitter, jitter, 1)[0]
    return max(round(interval, 2), 0.1)


def start_records_generation(config, movie_dist, logger):
    try:
        if config.random_seed:
            logger.info(f"Setting random seed to {config.random_seed}")
            np.random.seed(config.random_seed)
        movie_ids = list(movie_dist.keys())
        while True:
            transaction_id = generate_records(config, movie_dist, movie_ids, logger)
            sleep_interval = get_sleep_interval(config)
            logger.info(
                f"Waiting for {sleep_interval} seconds before generating new records",
                extra={"transaction_id": transaction_id},
            )
            sleep(sleep_interval)
    except KeyboardInterrupt:
        logger.info("Shuting down due to keyboard interrupt")
