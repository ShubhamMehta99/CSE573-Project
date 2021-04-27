import  csv

def get_predicted_bots(Final_result_Dict):
    """This function takes the graph in the form of dictionary and returns a list of predicted bot.

    args:
        Final_result_Dict: Graph of all the (screen_name_one,screen_name_two) in dictionary format
    return:
        final_bots: List of classified bots after applying threshold of 10 retweets
    """
    final_bots = set()
    for i in Final_result_Dict:
        if Final_result_Dict[i] > 10:
            final_bots.add(i[0])
            final_bots.add(i[1])

    final_bots = list(final_bots)
    return final_bots

def get_predicted_bots_tier_two(Final_result_Dict , bots_predicted):
    """This function takes the graph in the form of dictionary and returns a list of predicted bots.

        args:
            Final_result_Dict: Graph of all the (screen_name_one,screen_name_two) in dictionary format
        return:
            final_bots: List of classified bots after applying threshold of 10 retweets
    """
    final_bots = set(bots_predicted)
    for i in Final_result_Dict:
        if Final_result_Dict[i] > 10:
            final_bots.add(i[0])
            final_bots.add(i[1])

    return list(final_bots)



def save_bots_predicted(final_bots):
    with open("Bots_predicted_after_tier_two.csv", 'w', newline="") as f:
        thewriter = csv.writer(f)
        for i in final_bots:
            arr = [i]
            thewriter.writerow(arr)

def save_accurately_predicted(Accurately_predicted):
    # storing all accurately predicted bots after tier two
    with open("Bots_accurately_predicted_after_tier_two.csv", 'w', newline="") as f:
        thewriter = csv.writer(f)
        for i in Accurately_predicted:
            arr = [i]
            thewriter.writerow(arr)

def save_all_bots(bot_names):
    with open("all_bots.csv", 'w', newline="") as f:
        thewriter = csv.writer(f)
        for i in bot_names:
            arr = [i]
            thewriter.writerow(arr)

