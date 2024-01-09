import pickle
import tools.prawCrypt as pc
from getpass import getpass
import praw
import nltk



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

    finance_subreddits = {s : reddit.subreddit(s) for s in subs}
    
    for s, v in finance_subreddits.items():
        print(s)
        for submission in v.hot(limit=5):
            print(submission.title)
    

if __name__ == '__main__':
    main()