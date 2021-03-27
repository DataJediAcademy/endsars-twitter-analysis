import pandas as pd
import requests
from searchtweets import load_credentials
import logging
import time
logging.getLogger().setLevel(logging.INFO)


my_search_args = load_credentials(".twitter_keys.yaml",
                                  yaml_key="search_tweets_recent_v2",
                                  env_overwrite=False)


def create_url(user_ids, user_fields="user.fields=username,name,created_at,location,verified,public_metrics"):
    url = "https://api.twitter.com/2/users?ids={}&{}".format(user_ids, user_fields)
    return url


def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def connect_to_endpoint(url, headers):
    max_tries = 10
    tries = 0
    total_sleep_seconds = 0

    while True:
        try:
            resp = requests.request("GET", url, headers=headers)

        except requests.exceptions.ConnectionError as exc:
            exc.msg = "Connection error for session; exiting"
            raise exc

        except requests.exceptions.HTTPError as exc:
            exc.msg = "HTTP error for session; exiting"
            raise exc

        if resp.status_code != 200 and tries < max_tries:

            tries += 1

            logging.info(f" HTTP Error code: {resp.status_code}: {resp.text} | {resp.reason}")
            # logging.info(f" Request payload: {kwargs['request_parameters']}")

            if resp.status_code == 429:
                logging.info("Rate limit hit... Will retry...")
                # Expontential backoff, but within a 15-minute (900 seconds) period. No sense in backing off for more than 15 minutes.
                sleep_seconds = min(((tries * 2) ** 2), max(900 - total_sleep_seconds, 30))
                total_sleep_seconds = total_sleep_seconds + sleep_seconds

            elif resp.status_code >= 500:
                logging.info("Server-side error... Will retry...")
                sleep_seconds = 30
            else:
                # Other errors are a "one and done", no use in retrying error...
                logging.info('Quitting... ')
                raise requests.exceptions.HTTPError

            logging.info(f"Will retry in {sleep_seconds} seconds...")
            time.sleep(sleep_seconds)
            continue

        break

    return resp.json()['data']


def get_user_details(user_id_list, fname="endsars_tweets_user_details"):
    users = []
    headers = create_headers(my_search_args['bearer_token'])
    logging.info('Starting to retrieve user details')
    for i, user_list in enumerate(user_id_list):
        # if i % 300 == 0 & i != 0:
        #     time.sleep(300)
        logging.info(f'Retrieving user details from user list item: {i}')
        user_ids = ",".join(user_list)
        url = create_url(user_ids=user_ids)
        users += connect_to_endpoint(url=url, headers=headers)
    logging.info('Finished retrieving user details')
    users_df = pd.DataFrame(users)
    users_df.to_pickle(f"./data/{fname}.pkl")
    logging.info('Finished process and saved user details to pickle file')


if __name__ == '__main__':
    df = pd.read_pickle("./data/endsars_tweets_0820_0920.pkl")
    author_ids = list(df[~df.author_id.isnull()].author_id.unique())
    list_of_auth_ids = []
    temp_list = []
    for auth_id in author_ids:
        temp_list.append(auth_id)
        if len(temp_list) == 99:
            list_of_auth_ids.append(temp_list)
            temp_list = []
    list_of_auth_ids.append(temp_list)
    get_user_details(user_id_list=list_of_auth_ids, fname="endsars_tweets_user_details_tweets_0820_0920")
