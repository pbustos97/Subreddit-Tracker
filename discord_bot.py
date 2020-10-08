import discord
#import reddit_bot
from tokens import discord_token

#client = discord.Client()

class discord_bot(discord.Client):
    async def printReddit(url, channelId):
        channel = client.get_channel(channelId)
        if channel:
            await channel.send(f'{url}')

    async def assist():
        msg = '```\n'
        msg += '^setup subreddit1 subreddit2 ... subredditN\n'
        msg += '^leave\n'
        msg += '^help\n'
        msg += '```'
        return msg

    async def dispatch(function, message):
        msg = ''
        func = DISPATCH[function]
        author = message.author
        if func == setup:
            msg = func(message)


    async def setup(message):
        channel = message.channel
        multiredditList = []
        subredditList = message.content.split()
        subredditList = subredditList[1:]
        flairList = ['CPU', 'GPU']
        from intermediate import intermediate
        intermediate = intermediate(subredditList, flairList, int(channel.id))
        intermediate.reddit()

    async def leave(message):
        return

    #@client.event
    async def on_ready():
        print("Logged in as: {0.user}".format(client))

    #@client.event
    async def on_message(message):
        if message.author == client.user:
            return

        serverId = message.guild.id
        channelId = message.channel.id
        if message.content.startswith('^setup'):
            await setup(message)
        if message.content.startswith('^hello'):
            await message.channel.send('hello {}'.format(message.author))



    DISPATCH = {
        '^setup'    : setup,
        '^leave'    : leave,
        '^help'     : assist,
    }

#client.run(discord_token)