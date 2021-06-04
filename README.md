# MoviesMatchDataGenerator
Data generator code for Movies Match.  
Generates users (fictitious) ratings.

The code is meant to be a baseline and doesn't include code to 
stream the data to an actual system

[![Python 3.6](https://img.shields.io/badge/python-v3.6-blue)](https://www.python.org/downloads/release/python-360/)
[![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)](https://github.com/tterb/atomic-design-ui/blob/master/LICENSEs)

## Run Locally
Clone the project
```bash
  git clone https://github.com/Webiks/MoviesMatchDataGenerator
```

Go to the project directory
```bash
  cd MoviesMatchDataGenerator
```

Create virtual env:
```bash
  python -m venv .venv
  source .venv/bin/activate
```

Install dependencies
```bash
  pip install -r requirements.txt
```

Create local .env file
```bash
  cp .env.example .env
```

Run the generator
```bash
  python -m generator
```
  
## Generated data

The code generates dataframe with user_id, movie_id and rating.  
The `user_id` and `movie_id` matches id's from [Kaggle's The Movies Dataset](https://www.kaggle.com/rounakbanik/the-movies-dataset) 
and can include new ids dependeing on configuration.  
`rating` values are 0.5 to 5 (inclusive) in increments of 0.5

Example of generated data (in CSV format):
```CSV
user_id,movie_id,rating
300082,4,3.0
300199,2,4.0
47427,9,3.0
210960,2,3.0
300100,8,4.5
```

## Configuration

### Environment Variables
Environment variables can be set via `.env` file.  
The following is explanation of the variables to configure:
* `MOVIES_MATCH_LOG_LEVEL`: Log level, default is INFO
* `MOVIES_MATCH_GENERATE_INTERVAL_SEC`: Interval in seconds to trigger data generation
* `MOVIES_MATCH_GENERATE_INTERVAL_JITTER_SEC`: Introducing jitter to interval to simulate delays.
  * For example for interval of 60 seconds and jitter of 10 seconds, interval will be [50-70] seconds.
* `MOVIES_MATCH_RECORDS_TO_GENERATE`: How many records to generate per interval
* `MOVIES_MATCH_RECORDS_TO_GENERATE_JITTER`: Introducing jitter to records count to simulate different workloads.
  * For example for 250 records to generate and jitter of 140, each interval will generate [110-390] records.
* `MOVIES_MATCH_EXISTING_USERS_FIRST_ID`: First ID of existing users, defaults is 1
* `MOVIES_MATCH_EXISTING_USERS_LAST_ID`: Last ID of existing users, defaults is 270896
* `MOVIES_MATCH_EXISTING_USERS_FIRST_ID`: First ID of new users, defaults is 300001
* `MOVIES_MATCH_EXISTING_USERS_LAST_ID`: Last ID of new users, defaults is 300300
* `MOVIES_MATCH_NEW_USER_RATING_PROB`: The probability of generating a record for a new user
  * Set to 0 to generate data for existing users only
  * Set to 1 to generate data for new users only
  * The user to generate rating for is selected at random
* `MOVIES_MATCH_MOVIES_RATINGS_DISTRIBUTION_FILE`: Path to distribution file, defaults to `movies_ratings_distribution.csv`
  * See details in section below
* `MOVIES_MATCH_RANDOM_SEED=0`: Optional random seed so we'll get the same records re-running the generator.
  * Defaults to 0 which means ignore, i.e., different records each run
  * Mainly used in development to re-stream predictable data

### Movies Rating Distribution CSV
The data generator loads movies rating distributions from file to generate new rating based on existing per-movie distribution and not just randomly.  
The file is also used as the source for movies ids.  
Update or create new file with new movies to better simulate real-world environment where movies and ratings are added constantly.

The file is in CSV format and includes the following columns:
* (index): Running index
* movieId: Movie's unique id
* rating: Movie's rating ([0.5-5] in increments of 0.5)
* prob: Movie's rating probability

Each movie ratings probabilities must have sum of 1 to create a valid distribution

Example:
```CSV
150,16,0.5,0.0033630647755519814
151,16,1.0,0.012867378271677147
152,16,1.5,0.004484086367402642
153,16,2.0,0.037578593361602575
154,16,2.5,0.02349271335965297
155,16,3.0,0.20422088999366378
156,16,3.5,0.09772383876785105
157,16,4.0,0.34498220987473804
158,16,4.5,0.10142808402787933
159,16,5.0,0.1698591411999805
```
