import pandas as pd

filepath = 'SWM-dataset.csv'


def get_estimated_threshold(datarows):
    ''' Estimates a threshold in seconds that defines a coordinated link share. Here threshold is calculated as a function of the median co-share time difference. More specifically, the function ranks all
        co-shares by time-difference from first share and focuses on the behaviour of the quickest second share performing q\% (default 0.5) retweets
        The value returned is the median time in seconds spent by these URLs to cumulate the p\% (default 0.1) of their total shares.'''

    # count #of different original tweets
    orig_df = pd.DataFrame(datarows['retweet_tid'].value_counts())
    orig_df.reset_index(level=0, inplace=True)
    orig_df.columns = ['retweet_tid', "share_count"]
    # filter the retweets where count>1
    orig_df = orig_df[orig_df["share_count"] > 1]
    # filter those retweet_ids from original dataframe
    datarows = datarows[datarows.set_index('retweet_tid').index.isin(orig_df.set_index('retweet_tid').index)]
    # metrics creation
    datarows['postedtime'] = datarows['postedtime'].astype('datetime64[ns]')
    ranks_df = datarows[['retweet_tid', 'postedtime']]
    grouped_tweets = datarows.groupby('retweet_tid')
    ranks_df['tweet_share_count'] = grouped_tweets['tid'].transform('nunique')
    ranks_df['first_share_date'] = grouped_tweets['postedtime'].transform('min')
    ranks_df['rank'] = grouped_tweets['postedtime'].rank(ascending=True, method='first')
    ranks_df['perc_shares'] = ranks_df['rank'] / ranks_df['tweet_share_count']
    ranks_df['seconds_from_1st_share'] = (ranks_df['postedtime'] - ranks_df['first_share_date']).dt.total_seconds()
    ranks_df = ranks_df.sort_values(by='retweet_tid')
    # find retweet's with an unusual fast second share and keep the quickest
    filter_ranks_df = ranks_df[ranks_df['rank'] == 2].copy(deep=True)
    filter_ranks_df['seconds_from_1st_share'] = filter_ranks_df.groupby('retweet_tid')[
        'seconds_from_1st_share'].transform('min')
    filter_ranks_df = filter_ranks_df[['retweet_tid', 'seconds_from_1st_share']]
    filter_ranks_df = filter_ranks_df.drop_duplicates()
    filter_ranks_df = filter_ranks_df[
        filter_ranks_df['seconds_from_1st_share'] <= filter_ranks_df['seconds_from_1st_share'].quantile(0.1)]
    # filter ranks_df that join with filter_ranks_df
    ranks_df = ranks_df[ranks_df.set_index('retweet_tid').index.isin(filter_ranks_df.set_index('retweet_tid').index)]
    # filter values by 0.5
    ranks_sub_df = ranks_df[ranks_df['perc_shares'] > 0.5].copy(deep=True)
    ranks_sub_df['seconds_from_1st_share'] = ranks_sub_df.groupby('retweet_tid')['seconds_from_1st_share'].transform(
        'min')
    ranks_sub_df = ranks_sub_df[['retweet_tid', 'seconds_from_1st_share']]
    ranks_sub_df = ranks_sub_df.drop_duplicates()

    summary_secs = ranks_sub_df['seconds_from_1st_share'].describe()
    coordination_interval = ranks_sub_df['seconds_from_1st_share'].quantile(0.5)
    coord_interval = (None, None)
    if coordination_interval == 0:
        coordination_interval = 1
        coord_interval = (summary_secs, coordination_interval)
    else:
        coord_interval = (summary_secs, coordination_interval)

    return coord_interval


def coord_shares(datarows):
    coordination_interval = get_estimated_threshold(datarows)
    coordination_interval = coordination_interval[1]

    orig_df = pd.DataFrame(datarows['retweet_tid'].value_counts())
    orig_df.reset_index(level=0, inplace=True)
    orig_df.columns = ['retweet_tid', "share_count"]
    orig_df = orig_df[orig_df["share_count"] > 1]
    orig_df = orig_df.sort_values('retweet_tid')
    shares_df = datarows[datarows.set_index('retweet_tid').index.isin(orig_df.set_index('retweet_tid').index)]

    data_list = []
    retweets_count = orig_df.shape[0]
    i = 0

    for index, row in orig_df.iterrows():
        i = i + 1
        try:
            print(f"processing {i} of {retweets_count}, retweet_tid={row['retweet_tid']}")
            summary_df = shares_df[shares_df['retweet_tid'] == row['retweet_tid']].copy(deep=True)
            summary_df['postedtime'] = summary_df['postedtime'].astype('datetime64[ns]')
            date_series = summary_df['postedtime'].astype('int64') // 10 ** 9
            max_value = date_series.max()
            min_value = date_series.min()
            div = (max_value - min_value) / coordination_interval + 1
            summary_df["cut"] = pd.cut(summary_df['postedtime'], int(div)).apply(lambda x: x.left).astype(
                'datetime64[ns]')
            cut_gb = summary_df.groupby('cut')
            summary_df.loc[:, 'count'] = cut_gb['cut'].transform('count')
            summary_df.loc[:, 'retweet_tid'] = row['retweet_tid']
            summary_df.loc[:, 'share_date'] = cut_gb['postedtime'].transform(lambda x: [x.tolist()] * len(x))
            summary_df = summary_df[['cut', 'count', 'share_date', 'retweet_tid']]
            summary_df = summary_df[summary_df['count'] > 1]
            if summary_df.shape[0] > 1:
                summary_df = summary_df.loc[summary_df.astype(str).drop_duplicates().index]
                data_list.append(summary_df)
        except Exception as e:
            pass

    data_df = pd.concat(data_list)

    coor_shares_df = data_df.reset_index(drop=True).apply(pd.Series.explode).reset_index(drop=True)
    shares_df = shares_df.reset_index(drop=True)
    shares_df.loc[:, 'coord_expanded'] = shares_df['retweet_tid'].isin(coor_shares_df['retweet_tid'])
    shares_df.loc[:, 'coord_date'] = shares_df['postedtime'].astype('datetime64[ns]').isin(coor_shares_df['share_date'])

    shares_df.loc[:, 'is_coordinated'] = shares_df.apply(
        lambda x: True if (x['coord_expanded'] and x['coord_date']) else False, axis=1)
    shares_df.drop(['coord_expanded', 'coord_date'], inplace=True, axis=1)
    shares_df.to_csv('file_name.csv', encoding='utf-8')
    return shares_df