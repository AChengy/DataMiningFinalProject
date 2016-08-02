import praw

urls = ['https://www.reddit.com/r/nba/comments/4owimb/post_game_thread_the_cleveland_cavaliers_defeat/']

#f = open("top25submissioncomments.txt", 'w')
r = praw.Reddit(user_agent='my_cool_application')

for url in urls:
    submission = r.get_submission(url)
    print(submission.title)
    print("=" * 30)

    submission.replace_more_comments(limit=None, threshold=0)
    # for sorting all the comments by score
    all_comments = submission.comments
    all_comments = sorted(all_comments, key=lambda x: x.score)

    for comment in all_comments:
        print(comment.body)
        print("score: " + str(comment.score))
        print("flair: ", comment.author_flair_text)
        print("#" * 10)
    print("\n"*3)




# submissions = r.get_subreddit('nba').get_top_from_year(limit = 25)
#
# for submission in submissions:
#     print (submission.title)
#     f.write(submission.title+"\n")
#     #print (submission.url)
#     print ("=" * 30)
#     f.write("=" * 30)
#     #for sorting all the comments by score
#     #submission.comments = sorted(submission.comments, key=lambda x: x.score)
#     #submission.replace_more_comments(limit=None, threshold=0)
#     all_comments = submission.comments
#     for comment in all_comments:
#         print (comment.body)
#         #currently runs into an encoding problem on some comments.
#         #f.write("\n",comment.body)
#         print ("score: " + str(comment.score))
#         f.write("\nscore: " + str(comment.score) + "\n")
#
#         print("flair: ", comment.author_flair_text)
#         print ("#" * 10)
#         f.write("#" * 10)
#     print ("\n" * 3)
#     f.write("\n" * 3)
#
# f.close()