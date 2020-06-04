import pandas as pd
import matplotlib.pyplot as plt
import csv

# reading csv file  
df = pd.read_csv("./data/movies_file.csv")

# Part 1
# Relation between Total number of ratings & Rating score
plt.scatter(df['total_number_of_ratings'], df['rating_score'])
plt.xlabel('total_number_of_ratings')
plt.ylabel('rating_score')
plt.savefig('./data/total_number_of_ratings-rating_score.png')

# Part 2
# Relation between Budget & Rating score
df.loc[df['budget'] == 10000000000, ['budget']] = 100000000
df.loc[df['budget'] == 2400000000, ['budget']] = 240000000

plt.scatter(df['budget'], df['rating_score'])
plt.xlabel('budget')
plt.ylabel('rating_score')
plt.savefig('./data/budget-rating_score.png')

# Part 3
# Average earnings (Gross USA) of each Genre in descending order
genres = df.genre.unique() # to get all unique generes
average_gross = {}
for genre in genres:
    tempDf = df[df.genre == genre] # filtering dataframe for a particular genere
    avg_gross = tempDf.gross_usa.mean() # taking average of a particular genere
    average_gross[genre] = int(avg_gross)

average_gross = sorted(average_gross.items(), key=lambda x: x[1], reverse=True) # sort it in descending order

# save average gross to a csv
with open('./data/average_gross.csv', mode='w', newline='') as gross_file:
    writer = csv.writer(gross_file, delimiter=',')
    
    for avg_gross in average_gross:
        writer.writerow([avg_gross[0], avg_gross[1]]) # write genre with average gross
        print(avg_gross[0], "=>", avg_gross[1]) # print genre with average gross