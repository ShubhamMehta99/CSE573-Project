import pandas as pd


def get_all_botnames_and_data(year):
    """This function will return all the bots that are present in the dataset for a particular year
    args:
        year: The year for which we need the botnames from the shares_dataframe after applying threshold one.
    return:
        all_bots_that_year: A set of all the bot_names present in the dataset
        data_for_second_threshold: A list of all the
    """
    #in this step we read all the bots that could be present in the file from the botsname csv
    all_bots = pd.read_csv('botnames.csv')
    all_bot_names = set()
    for i in all_bots.itertuples():
        all_bot_names.add(i[2])

    #In this step we read the data for 2016/2018
    if year == 2018:
        Data = pd.read_csv('shares_df_2018.csv')
    elif year == 2016:
        Data = pd.read_csv('shares_df_2016.csv')

    all_bots_that_year = set()
    Data_for_second_threshold = []
    unique_accounts = set()

    for datarow in Data.itertuples():
        #check if the datarow is a suspect after first threshold or not
        #true value of threshold means the datarow is a suspect

        coordinated = datarow[6]
        Screen_name_from = datarow[3]
        unique_accounts.add(Screen_name_from)


        if Screen_name_from in all_bot_names:
            all_bots_that_year.add(Screen_name_from)

        if coordinated:
            tid = datarow[1]
            retweet_tid = datarow[2]
            Screen_name_to = datarow[4]
            Data_for_second_threshold.append([tid, retweet_tid, Screen_name_from, Screen_name_to])

    return all_bots_that_year , Data_for_second_threshold,len(unique_accounts)



def get_data_for_tier_two(bots_predicted , year):
    """This function returns the data for tier two calculation.

    args:
        bots_predicted: bots that are predicted by tier one
    return:
        Data_for_tier_two: list of data for tier two
    """

    final_bots = set(bots_predicted)
    Whole_data = pd.read_csv('SWM-dataset.csv')
    Data_for_tier_two = []

    for datarow in Whole_data.itertuples():
        time = str(datarow[5])
        Screen_name_to = datarow[4]
        if Screen_name_to in final_bots and time[:4] == str(year):
            tid = datarow[1]
            retweet_tid = datarow[2]
            Screen_name_from = datarow[3]
            Data_for_tier_two.append([tid, retweet_tid, Screen_name_from, Screen_name_to])


    return Data_for_tier_two