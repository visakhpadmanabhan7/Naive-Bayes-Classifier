import sys

import numpy as np
import csv
import pandas as pd

def mean(numbers):
    mean=np.mean(numbers)
    return mean

def variance(numbers):
    avg = mean(numbers)
    variance = sum([(x - avg) ** 2 for x in numbers]) / float(len(numbers) - 1)
    return variance

def compute_probability(x, mean, var):
    exponent = np.exp(-((x - mean) ** 2 / (2 * var)))
    return (1 / (np.sqrt(2 * np.pi * var))) * exponent

def calculate_class_probabilities(summaries, data):
    errors=0
    for i in range(len(data)):

        gaussian_A_col_1 = compute_probability(data.iloc[i,1], (summaries[0][0]), (summaries[0][1]))
        gaussian_A_col_2 = compute_probability(data.iloc[i,2], summaries[0][2], summaries[0][3])

        gaussian_B_col_1 = compute_probability(data.iloc[i,1],summaries[1][0], summaries[1][1])
        gaussian_B_col_2 = compute_probability(data.iloc[i,2], summaries[1][2], summaries[1][3])

        probability_a = summaries[0][4] * gaussian_A_col_1 * gaussian_A_col_2
        probability_b = summaries[1][4]  * gaussian_B_col_1 * gaussian_B_col_2

        if ((probability_a > probability_b) and (data.iloc[i, 0] != 'A')):
            errors += 1
        elif ((probability_b > probability_a) and (data.iloc[i, 0] != 'B')):
            errors += 1
        else:
            pass

    for i in range(0,2):
            for j in range(0,5):
                if(j==4):
                    print(summaries[i][j])
                else:
                    print(summaries[i][j], end=" ")

    print(errors)

if __name__ == "__main__":
    expected_args = ["--data"]
    arg_len = len(sys.argv)
    info = []

    for i in range(len(expected_args)):
        for j in range(1, len(sys.argv)):
            if expected_args[i] == sys.argv[j] and sys.argv[j + 1]:
                info.append(sys.argv[j + 1])

    data = pd.read_csv(info[0], header=None)

    filter_values=np.unique(data.iloc[:,0])
    summarise_data_sets=[[],[]]
    for i in range(0,len(filter_values)):
        filtered_df= data[data.iloc[:,0].isin([filter_values[i]])]
        summarise_data_sets[i]=((mean(filtered_df[1])),(variance(filtered_df[1])),(mean(filtered_df[2])),(variance(filtered_df[2])),len(filtered_df)/len(data))
    probabilities = calculate_class_probabilities(summarise_data_sets, data)

