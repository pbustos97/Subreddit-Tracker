import praw
import threading
import time
from tokens import reddit_id, reddit_secret, reddit_username, reddit_password

# Used for different instances of the reddit bot
class reddit_bot (threading.Thread):
    def __init__(self, subredditList, flairList, channelId):
        threading.Thread.__init__(self)
        self.subredditList = subredditList
        self.flairList = flairList
        self.channelId = channelId
        self.reddit = reddit = praw.Reddit(
            user_agent="Subreddit Tracker (by u/bigboi_small_eggroll)",
            client_id=reddit_id,
            client_secret=reddit_secret,
            username=reddit_username,
            password=reddit_password
        )
        self.multireddit = self.reddit.multireddit(reddit_username, str(channelId))

        # Set to True from outside of class when user calls '^leave' command
        self.deletedMultireddit = False

    def run(self):
        try:
            self.multireddit.delete()
        except Exception as e:
            print(e)
        self.deletedMultireddit = False
        self.multireddit = self.reddit.multireddit(reddit_username, str(self.channelId))

        for subreddit in self.subredditList:
            self.multireddit.add(subreddit)

        for submission in self.multireddit.stream.submissions():
            if self.deletedMultireddit == True:
                return
            print(submission.title)
            print(submission.link_flair_text)
            url = 'https://www.reddit.com' + str(submission.permalink)
            if self.flairList:
                if submission.link_flair_text in self.flairList:
                    self.printUrl(submission.subreddit.display_name, url)
                    # Send url and channelId back into the intermediate class
            else:
                self.printUrl(submission.subreddit.display_name, url)
                # Send url and channelId back into the intermediate class
            if self.deletedMultireddit == True:
                return

    def printUrl(self, subredditName, url):
        print(subredditName)
        print(url)
        print()

    def delMultireddit(self):
        print('Deleting Multireddit')
        try:
            self.deletedMultireddit = True
            self.multireddit.delete()
            self._running = False
            self.do_run = False
            return True
        except Exception as e:
            print(e)
        return False