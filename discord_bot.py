import discord
#import reddit_bot
from tokens import discord_token

#client = discord.Client()

class discord_bot(discord.Client):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

    async def printReddit(self, url, channelId):
        channel = self.get_channel(channelId)
        print(channel)
        if channel:
            await channel.send(f'{url}')

    async def assist(self):
        msg = '```\n'
        msg += '^setup subreddit1 subreddit2 ... subredditN\n'
        msg += '^leave\n'
        msg += '^help\n'
        msg += '```'
        return msg

    async def setup(self, message):
        channel = message.channel
        multiredditList = []
        subredditList = message.content.split()
        subredditList = subredditList[1:]
        flairList = ['CPU', 'GPU']
        self.parent.startRedditBot(subredditList, channel.id)

    async def leave(self, channelId):
        self.parent.stopRedditBot(channelId)

    #@client.event
    async def on_ready(self):
        print("Logged in as: {0.user}".format(self))

    #@client.event
    async def on_message(self, message):
        if message.author == self.user:
            return

        serverId = message.guild.id
        channelId = message.channel.id
        if message.content.startswith('^setup'):
            await self.setup(message)
        if message.content.startswith('^leave'):
            await self.leave(message.channel.id)


# client = discord_bot()
# client.run(discord_token)