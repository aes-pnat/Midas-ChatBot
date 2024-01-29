import pickle
import tools.prawCrypt as pc
from getpass import getpass
import praw
from tqdm import tqdm
import pandas as pd

def retrive_submission_props(reddit, subreddits, limit=1000, time_filter='year', comment_limit=10):
    qna_dict = {'questions' : [], 'answers' : [],'tags': []}

    for s in subreddits:
        subreddit_topic = reddit.subreddit(s)
        print(s)
        for submission in tqdm(subreddit_topic.top(limit=limit, time_filter=time_filter), total=limit):
            for top_level_comment in submission.comments.list()[:comment_limit]:
                qna_dict['questions'].append(f'{submission.title} {submission.selftext}')
                qna_dict['answers'].append(top_level_comment.body)
                qna_dict['tags'].append(s)
    
    return qna_dict

def main():
    with open('./tools/encrypted_values.pkl', 'rb') as file:
        encrypted_values = pickle.load(file)

    password = getpass("Enter password: ")

    reddit_client_ID = pc.decrypt(encrypted_values['reddit_client_ID'], password)
    reddit_secret_token = pc.decrypt(encrypted_values['reddit_secret_token'], password)
    reddit_usernName = pc.decrypt(encrypted_values['reddit_usernName'], password)
    reddit_password = pc.decrypt(encrypted_values['reddit_password'], password)

    reddit = praw.Reddit(
        client_id=reddit_client_ID,
        client_secret=reddit_secret_token,
        user_agent='MidasChatBot',
        username=reddit_usernName,
        password=reddit_password
        )
    subs = [
        'wallstreetbets',
        'invest',
        'finance',
        'stocks',
        'stockmarket',
        'dividends',
        'options',
        'cryptocurrencies'
    ]

    test_subreddit = reddit.subreddit('wallstreetbets')

    for submission in test_subreddit.hot(limit=1):
        print(submission.title)
        print(submission.selftext)
        print(submission.comments)
        print(submission.comments.list())


    qna = retrive_submission_props(reddit, subs, limit=1000, time_filter='year', comment_limit=10)
    qna_df=pd.DataFrame(qna)
    qna_df.to_csv('qna_df_reddit.csv',index=False)


    

if __name__ == '__main__':
    main()