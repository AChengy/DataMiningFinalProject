import re, csv

CLEWordCloud = {}
GSWWordCloud = {}
g4WordCloud = {}
ignoreWords = ['.', '!', '?', ';', ':' ]

with open('100common.txt', 'r') as f1:
    for word in f1:
        ignoreWords.append(word.rstrip())

print ignoreWords



# with open('CLEWinsCmts.txt', 'r') as f:
#     for i in f:
#         words = re.findall(r"[\w']+|[.,!?;]", i.rstrip())
#         for word in words:
#             word = word.lower()
#             if word in CLEWordCloud.keys() and word not in ignoreWords:
#                 CLEWordCloud[word] = CLEWordCloud[word] + 1
#             elif word not in CLEWordCloud.keys() and word not in ignoreWords:
#                 CLEWordCloud[word] = 1
#             else:
#                 continue
#
with open('CLEWinWords.csv', 'wb') as csv_file:
    writer = csv.writer(csv_file)
    for key, value in CLEWordCloud.items():
        writer.writerow([key, value])

with open('GSWWinsCmts.txt', 'r') as f:
    for i in f:
        words = re.findall(r"[\w']+|[.,!?;]", i.rstrip())
        for word in words:
            word = word.lower()
            if word in GSWWordCloud.keys() and word not in ignoreWords:
                GSWWordCloud[word] = GSWWordCloud[word] + 1
            elif word not in GSWWordCloud.keys() and word not in ignoreWords:
                GSWWordCloud[word] = 1
            else:
                continue

with open('GSWWinCmts.csv', 'wb') as csv_file:
    writer = csv.writer(csv_file)
    for key, value in GSWWordCloud.items():
        writer.writerow([key, value])


with open('g4comments.txt', 'r') as f:
    for i in f:
        words = re.findall(r"[\w']+|[.,!?;]", i.rstrip())
        for word in words:
            word = word.lower()
            if word in g4WordCloud.keys() and word not in ignoreWords:
                g4WordCloud[word] = g4WordCloud[word] + 1
            elif word not in g4WordCloud.keys() and word not in ignoreWords:
                g4WordCloud[word] = 1
            else:
                continue

with open('g4comments.csv', 'wb') as csv_file:
    writer = csv.writer(csv_file)
    for key, value in g4WordCloud.items():
        writer.writerow([key, value])