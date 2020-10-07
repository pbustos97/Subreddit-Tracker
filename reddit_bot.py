import praw
from discord_bot import printReddit
from tokens import reddit_id, reddit_secret, reddit_username, reddit_password

# newInstance([string], [string], int)
async def newInstance(subredditList, flairList, channelId):
    reddit = praw.Reddit(
        user_agent="Subreddit Tracker (by u/bigboi_small_eggroll)",
        client_id=reddit_id,
        client_secret=reddit_secret,
        username=reddit_username,
        password=reddit_password
    )

    multireddit = reddit.multireddit(reddit_username, str(channelId))

    for subreddit in subredditList:
        multireddit.add(subreddit)

    for submission in multireddit.stream.submissions():
        if sumbission.link_flair_text in flairList:
            url = 'https://www.reddit.com' + str(submission.permalink)
            printReddit(url, int(channelId))