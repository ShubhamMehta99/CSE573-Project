import numpy as np
import pandas as pd
import csv
from Read_data import get_all_botnames_and_data,get_data_for_tier_two
from Build_graph import build_graph
from verify_results_and_store import get_predicted_bots , get_predicted_bots_tier_two,save_bots_predicted,save_accurately_predicted,save_all_bots

if __name__ == "__main__":
    bot_names , Data_for_second_threshold,unique_accounts = get_all_botnames_and_data(2018)

    Final_result_Dict_tier_one = build_graph(Data_for_second_threshold)

    #just applying threshold of 10 retweets between bots
    bots_predicted = get_predicted_bots(Final_result_Dict_tier_one)

    #get data for tier two
    Data_for_tier_two = get_data_for_tier_two(bots_predicted,2018)

    #graph for tier two

    Final_result_Dict_tier_two = build_graph(Data_for_tier_two)

    #bots_predicted_finally
    final_bots = get_predicted_bots_tier_two(Final_result_Dict_tier_two , bots_predicted)

    Accurately_predicted = []
    for i in final_bots:
        if i in bot_names:
            Accurately_predicted.append(i)


    len_Accurately_predicted = len(Accurately_predicted)
    len_bot_names = len(bot_names)
    len_final_bots = len(final_bots)

    #saving final bots predicted
    save_bots_predicted(final_bots)

    #saving accurately predicted
    save_accurately_predicted(Accurately_predicted)

    #saving all bots names in data
    save_all_bots(bot_names)

    #recall
    recall = len_Accurately_predicted/len_bot_names
    print(recall)

    #precision
    precision = len_Accurately_predicted/len_final_bots
    print(precision)

    #accuracy
    Total_predictions = unique_accounts
    TP = len_Accurately_predicted
    FN = len_bot_names - len_Accurately_predicted
    FP = len_final_bots - len_Accurately_predicted
    TN = Total_predictions - TP - FN - FP

    correct_predictions = TP + TN
    wrong_predictions = FN + FP
    Accuracy = correct_predictions / Total_predictions
    print(Accuracy)
