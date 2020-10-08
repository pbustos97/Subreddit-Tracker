import threading
import time
from discord_bot import discord_bot
from reddit_bot import reddit_bot
from tokens import discord_token
class intermediate:
    def __init__(self):
        self.subredditList = ['askreddit']
        self.flairList = []
        #self.channelId = None
        self.redditBotList = []
        self.discordBot = None

    def startRedditBot(self, subredditList, channelId):
        redditBot = reddit_bot(subredditList, self.flairList, channelId, self)
        redditBot.start()
        self.redditBotList.append(redditBot)
        print('----------')
        print(self.redditBotList)
        print('----------')
        #redditBot.join()

    def stopRedditBot(self, channelId):
        for i in self.redditBotList:
            if i.channelId == channelId:
                i.delMultireddit()
                self.redditBotList.remove(i)

    def discordPrint(self, url, channelId):
        yield self.discordBot.printReddit(url, channelId)

    def startDiscordBot(self):
        discordBot = discord_bot(self)
        self.discordBot = discordBot
        self.discordBot.run(str(discord_token))
        #self.discordBot.start()
        #self.discordBot.join()

intermediate = intermediate()
intermediate.startDiscordBot()
# intermediate.startRedditBot(['askreddit'], 1234)
# intermediate.startRedditBot(['teenagers','games','gaming','dankmemes', 'memes', 'funny'], 12345)
# time.sleep(1)
# print(intermediate.stopRedditBot(1234))
# time.sleep(0.25)
# print(intermediate.redditBotList)
#intermediate.startDiscordBot()