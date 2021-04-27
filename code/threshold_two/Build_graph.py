"""
For predicting if there is some sort of CLBS present in the data frame we need to build a graph between all possible
screen_names that are present in the dataset if they are suspect after applying first threshold

The Task of building graph is divided in two parts
1. Check which suspects retweeted the same tweet. ( Tid is unique for each and every tweet but, if two bots have
retweeted a same tweet then the retweet_tid will be same for bot of them)
2. Check if a suspect pair has shared the same retweet more than 10 times. ( If they have then there is a good chance
that they are bots.)
The Dataset is quite skewed so we may classify lot of actual human users as bots, but the overall aim is to accurately
classify as many bots as we can.

For step 1.
we store all the unique names that have retweeted a particular tweet. we use retweet_id as key for the dictionary.
type of Dict:
    key -> retweet_id
    value -> set of all the screen_name_from who retweeted that original tweet.

For step 2:
we make yet another dictionary and we save the suspect pairs that have retweeted the same tweet.
we build a graph by iterating for each key in Dict and adding an edge between two screen_names that are in same set
over here adding an edge is similar to adding one to the value in Final_result_Dict
type of Dictionary:
    key -> (Screen_name_one, Screen_name_two)
    value -> number of times suspects, screen_name_one and screen_name_two shared the same tweet
"""

def build_graph(Data_for_second_threshold):

    #step one
    Dict = {}
    for i in Data_for_second_threshold:
        tid = i[0]
        retweet_tid = i[1]
        Screen_name_from = i[2]
        Screen_name_to = i[3]

        if retweet_tid not in Dict:
            Dict[retweet_tid] = set()
        Dict[retweet_tid].add(Screen_name_from)

    #step two
    Final_result_Dict = {}

    for i in Dict:
        Set_for_this_retweet = list(Dict[i])
        set_length = len(Set_for_this_retweet)

        if set_length > 1:
            for i in range(set_length - 1):
                for j in range(i + 1, set_length):
                    Screen_name_from_one = Set_for_this_retweet[i]
                    Screen_name_from_two = Set_for_this_retweet[j]
                    if (Screen_name_from_one, Screen_name_from_two) in Final_result_Dict:
                        Final_result_Dict[(Screen_name_from_one, Screen_name_from_two)] = Final_result_Dict[(
                            Screen_name_from_one, Screen_name_from_two)] + 1
                    elif (Screen_name_from_two, Screen_name_from_one) in Final_result_Dict:
                        Final_result_Dict[(Screen_name_from_two, Screen_name_from_one)] = Final_result_Dict[(
                            Screen_name_from_two, Screen_name_from_one)] + 1
                    else:
                        Final_result_Dict[(Screen_name_from_one, Screen_name_from_two)] = 1

    return Final_result_Dict
