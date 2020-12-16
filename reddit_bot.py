import praw
import threading
import asyncio
import time
from tokens import reddit_id, reddit_secret, reddit_username, reddit_password

# Used for different instances of the reddit bot
class reddit_bot (threading.Thread):
    def __init__(self, subredditList, flairList, channelId, parent, loop):
        threading.Thread.__init__(self)
        self.parent = parent
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
        self.discordLoop = loop

        # Set to True from outside of class when user calls '^leave' command
        self.deletedMultireddit = False

    def run(self):
        try:
            self.multireddit.delete()
        except Exception as e:
            print(e)
        self.deletedMultireddit = False
        self.multireddit = self.reddit.multireddit(reddit_username, str(self.channelId))

        print(f'Multireddit created in {self.channelId}')

        for subreddit in self.subredditList:
            self.multireddit.add(subreddit)
        
        while self.deletedMultireddit == False:
            try:
                print(f'Multireddit stream start in {self.channelId}')
                for submission in self.multireddit.stream.submissions(skip_existing=True):
                    if self.deletedMultireddit == True:
                        return

                    data = []
                    data.append('https://www.reddit.com' + str(submission.permalink))
                    data.append(submission.title)
                    if len(self.flairList) > 0:
                        if str(submission.link_flair_text).lower() in self.flairList:
                            result = asyncio.run_coroutine_threadsafe(self.parent.discordPrint(data, self.channelId), self.discordLoop)

                    else:
                        result = asyncio.run_coroutine_threadsafe(self.parent.discordPrint(data, self.channelId), self.discordLoop)

                    if self.deletedMultireddit == True:
                        return

            except Exception as e:
                print(f'{e}')
                print(f'Attempting to restart thread')

    # Debug terminal printer
    def printUrl(self, subredditName, url):
        print(subredditName)
        print(url)
        print()

    # Deletes multireddit and stops thread from continuing to run
    def delMultireddit(self):
        print('Deleting Multireddit')
        try:
            self.deletedMultireddit = True
            self.multireddit.delete()
            self._running = False
            self.do_run = False
            print(f'Multireddit Deleted for channel {self.channelId}')
            return True
        except Exception as e:
            print(e)
        print(f'Mulireddit Deletion Failed for channel {self.channelId}')
        return False