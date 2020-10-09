import threading
import asyncio
import time
from discord_bot import discord_bot
from reddit_bot import reddit_bot
from tokens import discord_token

# Intermediate class to circumvent the circular dependency needed between the two API wrappers
class intermediate:
    def __init__(self):
        self.redditBotList = []
        self.discordBot = None

        # Required for synchronous reddit_bot to be compatible with asynchronous discord_bot
        self.discordLoop = asyncio.new_event_loop()

    # Create a new thread of a reddit bot
    def startRedditBot(self, subredditList, flairList, channelId):
        for i in self.redditBotList:
            if i.channelId == channelId:
                return 'Bot is already setup in this channel, use ^leave to disconnect the bot'

        redditBot = reddit_bot(subredditList, flairList, channelId, self, self.discordLoop)
        redditBot.start()
        self.redditBotList.append(redditBot)

        return True

    # Stops the thread and deletes the multireddit containing the channelId of the passed in channelId
    def stopRedditBot(self, channelId):
        for i in self.redditBotList:
            if i.channelId == channelId:
                i.delMultireddit()
                self.redditBotList.remove(i)

    # Intermediate function to send urls from Reddit to Discord
    async def discordPrint(self, url, channelId):
        await self.discordBot.printReddit(url, channelId)

    # Starts the Discord bot and stores it inside the class
    def startDiscordBot(self):
        asyncio.set_event_loop(self.discordLoop)
        discordBot = discord_bot(self, self.discordLoop)
        self.discordBot = discordBot
        self.discordBot.run(str(discord_token))


intermediate = intermediate()
intermediate.startDiscordBot()