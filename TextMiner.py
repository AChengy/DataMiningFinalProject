import nltk, functools, gensim, re, csv

games = ['g1.csv', 'g2.csv', 'g3.csv', 'g4.csv', 'g5.csv', 'g6.csv', 'g7.csv']
gm = 1
illegalWords= ['MJ(x2)', 'seat', 'MVP.\\n\\nAlso', 'fans', 'him','points', 'life', 'kyrie', 'Damn']

replacePlayers = {'Bryant': 'Lakers', 'James':'Cavaliers', 'Durant':'Thunder', 'Richardson':'Warriors', 'Smith':'Knicks',
                  'Curry':'Warriors', 'Green':'Warriors', 'Sprewell':'Knicks', 'Iguodala':'Warriors','Westbrook':'Thuder',
                  'Wade':'Heat','Duncan':'Spurs', 'Oakley':'Suns', 'Jordan':'Bulls', 'Thompson':'Warriors', 'Perkins':'Thunder', 'Hardaway':'Warriors', 'Irving':'Cavaliers',
                  'Livingston':'Warriors','Madsen':'Lakers', 'Davis':'Pelicans', 'Garnett':'Celtics', 'Dellavedova':'Cavaliers',
                  "Robertson":'Kings', 'Leonard':'Spurs', 'Nowitzki':"Mavericks", 'Olajuwon':'Rockets', 'Nash':'Suns',
                  'Iverson':'76ers', 'Parker':'Spurs','Adams':'Thunder', 'Lillard':'Blazers', 'Bullets':'Wizards', 'Ilgauskas':'Cavaliers',
                  'Mudiay':'Nuggets', 'Porzingis':'Knicks', 'Allen':'Celtics', 'Wall':'Wizards', 'Norris':'Rockets', "Johnson":'Raptors',
                  'Pierce':'Celtics', 'George':'Pacers'}

for game in games:
    #gather team comments and score
    NumComments = {}
    ScoreByTeam = {}

    with open(game, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            for item in row:
               if '|' in item and '[deleted]' not in item:
                   list = item.split()
                   word = list[len(list)-1]
                   list2 = word.split('|')
                   team =list2[len(list2)-2]
                   if team in replacePlayers.keys():
                       team = replacePlayers[team]
                   score = list2[len(list2)-1]
                   #print("Score: "+score)
                   if score in illegalWords:
                       continue
                   score = int(score)
                   if team != '':
                       if team in NumComments.keys():
                           NumComments[team] = NumComments[team]+1
                       else:
                           NumComments[team] = 1

                       if team in ScoreByTeam.keys():
                            ScoreByTeam[team] = ScoreByTeam[team] + score
                       else:
                            ScoreByTeam[team] = score
    with open('gm'+str(gm)+'NumComments.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in NumComments.items():
            if value < 10:
                continue
            writer.writerow([key, value])

    with open('gm'+str(gm)+'ScoreByTeam.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in ScoreByTeam.items():
            writer.writerow([key, value])
    print("game: "+ str(gm))
    gm+=1

print(NumComments)
print(ScoreByTeam)