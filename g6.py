import csv

f1 = open('g4comments.txt', 'w')

with open('g4.csv', 'r') as f:
    csvreader = csv.reader(f, delimiter = '|')
    for comment, team, score in csvreader:
        print("Comment: "+comment)
        print("Team: "+team)
        print("Score: "+score)
        if int(score) > 5 and comment != '[deleted]':
            f1.write(comment)
            f1.write('\n')

f1.close()