import discord
#import reddit_bot
from tokens import discord_token

class discord_bot(discord.Client):
    def __init__(self, parent, loop):
        super().__init__(loop=loop)
        self.parent = parent

    async def printReddit(self, url, channelId):
        channel = self.get_channel(channelId)
        #print(channel)
        if channel:
            await channel.send(f'{url}')
        else:
            print(f'Channel {channel} does not exist')

    async def assist(self):
        msg = '```\n'
        msg += '^setup subreddit1 subreddit2 ... subredditN\n'
        msg += '^leave\n'
        msg += '^help\n'
        msg += '```'
        return msg

    async def setup(self, message):
        channel = message.channel
        subredditList = message.content.split()
        subredditList = subredditList[1:]
        flairList = []
        def check(msg):
            if msg.author == message.author:
                return msg
        await channel.send('What flairs do you want to add? (Comma separated ex. [gpu,cpu,m.2 ssd,serious replies only,])')
        try:
            msg = await self.wait_for('message', check=check)
        except:
            await chanel.send(f'{message.author} needs to set the flairs in the {channel} text channel')
            return
        flairList = msg.content.split(',')
        for i in range(0, len(flairList)):
            flairList[i] = flairList[i].lower()
        #print(flairList)
        result = self.parent.startRedditBot(subredditList, flairList, channel.id)
        if result != True:
            await channel.send(result)

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
