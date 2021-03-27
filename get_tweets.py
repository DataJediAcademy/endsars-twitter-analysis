import pandas as pd
from searchtweets import gen_request_parameters, load_credentials, collect_results
from datetime import datetime, timedelta, date
import logging
logging.getLogger().setLevel(logging.INFO)

bode_all_search_args = load_credentials(".twitter_keys.yaml",
                                        yaml_key="search_tweets_all_bode_v2",
                                        env_overwrite=False)


def retrieve_tweets(start_date,
                    end_date,
                    max_tweets=30000,
                    results_per_call=100,
                    search_args=bode_all_search_args,
                    keywords_query="""#EndSARS OR "Soro Soke" OR "lekki toll gate" OR "anti-robbery squad" OR
"lekki massacre" OR "End bad governance" OR "End swat" OR #LekkiMassacre lang:en""",
                    tweet_resp_fields="id,author_id,created_at,text,geo,referenced_tweets,in_reply_to_user_id,\
                    entities,public_metrics",
                    expansions_resp_fields="author_id,entities.mentions.username,geo.place_id,in_reply_to_user_id,\
referenced_tweets.id,referenced_tweets.id.author_id",
                    user_resp_fields="id,created_at,location,username,verified,public_metrics",
                    place_resp_fields="country,country_code,full_name,geo,id,name,place_type"):
    """
    Create a function that gets tweets using the premium search API where matching a certain keyword during a
    certain date range and returns all these tweets as a list
    """
    tweets_query = gen_request_parameters(query=keywords_query,
                                          start_time=start_date,
                                          end_time=end_date,
                                          expansions=expansions_resp_fields,
                                          tweet_fields=tweet_resp_fields,
                                          user_fields=user_resp_fields,
                                          place_fields=place_resp_fields,
                                          results_per_call=results_per_call)
    tweets = collect_results(tweets_query,
                             max_tweets=max_tweets,
                             result_stream_args=search_args)
    return tweets


def get_dt_after(start_date, delta=timedelta(days=7)):
    start_dt = datetime.strptime(start_date, "%Y-%m-%d")
    end_dt = start_dt + delta
    return end_dt.strftime("%Y-%m-%d")


def days_cur_month(m=1, y=2021):
    if m == 12:
        ndays = (date(y+1, 1, 1) - date(y, m, 1)).days
    else:
        ndays = (date(y, m+1, 1) - date(y, m, 1)).days
    d1 = date(y, m, 1)
    d2 = date(y, m, ndays)
    delta = d2 - d1
    return [(d1 + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(0, delta.days+1, 7)]


def create_tweets_df(dates_list,
                     max_tweets=30000,
                     results_per_call=100,
                     search_args=bode_all_search_args,
                     keywords_query="""#EndSARS OR "Soro Soke" OR "lekki toll gate" OR "anti-robbery squad" OR
"lekki massacre" OR "End bad governance" OR "End swat" OR #LekkiMassacre lang:en""",
                     tweet_resp_fields="""id,author_id,created_at,text,geo,referenced_tweets,in_reply_to_user_id,entities,public_metrics""",
                     expansions_resp_fields="""author_id,entities.mentions.username,geo.place_id,in_reply_to_user_id,referenced_tweets.id,referenced_tweets.id.author_id""",
                     # user_resp_fields="id,created_at,location,username,verified,public_metrics",
                     place_resp_fields="country,country_code,full_name,geo,id,name,place_type"):
    """
    Create a function that Creates a dataframe from the tweets you've retrieved using the retieve_tweets function
    you created above. This functions should also take a list of datest you want to get tweets from
    """
    tweets = []
    logging.info('Starting to retrieve tweets')
    for dt in dates_list:
        end_date = get_dt_after(start_date=dt)
        logging.info(f'Retrieving tweets from {dt} to {end_date}')
        tweets += retrieve_tweets(start_date=dt, end_date=end_date,
                                  max_tweets=max_tweets, results_per_call=results_per_call,
                                  search_args=search_args, keywords_query=keywords_query,
                                  tweet_resp_fields=tweet_resp_fields,
                                  # user_resp_fields=user_resp_fields,
                                  place_resp_fields=place_resp_fields, expansions_resp_fields=expansions_resp_fields
                                  )
    logging.info('Finished retrieving tweets')
    df = pd.DataFrame(tweets)
    df.to_pickle(f"./data/endsars_tweets_{dates_list[0].replace('-', '')}_{dates_list[-1].replace('-', '')}.pkl")
    logging.info('Finished process and saved tweets to pickle file')


if __name__ == '__main__':
    dates = []
    dates += days_cur_month(8, 2020)
    create_tweets_df(dates_list=dates, max_tweets=10000)
