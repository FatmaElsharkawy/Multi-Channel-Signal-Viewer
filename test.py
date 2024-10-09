# import csv
# with open('rec_1r.csv', mode ='r')as file:
#   csvFile = csv.reader(file)
#   for lines in csvFile:
#         print(lines)

# import csv
# with open('rec_1r.csv', mode ='r') as file:    
#        csvFile = csv.DictReader(file)
#        for lines in csvFile:
#             print(lines)


import pandas as pd
csvFile = pd.read_csv('rec_1r.csv')
first_column = csvFile.iloc[:, 0].values
second_column = csvFile.iloc[:, 1].values

# Print the arrays
print("First Column:", first_column)
print("Second Column:", second_column)