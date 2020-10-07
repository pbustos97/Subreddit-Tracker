import discord
from tokens import discord_token

client = discord.Client()

DISPATCH = {
    '^setup'    : setup,
    '^leave'    : leave,
    '^help'     : assist,
}

async def printReddit(url, channelId):
    channel = client.get_channel(channelId)
    if channel:
        await channel.send('{}'.format(url))

async def assist():
    msg = '```\n'
    msg += '^setup\n'
    msg += '^leave\n'
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
    # Save channel location to file or append to list


    await channel.send('What subreddits do you want to track? (Space Separated)')

    def addSubreddits(m):
        if m.author.id == message.author.id:
            subredditList = m.content.split()
            subredditTemplate = 'r/'
            multiredditList = []
            for subreddit in subredditList:
                subredditLink = subredditTemplate + subreddit
                multiredditList.append(subredditLink)

            # Call multireddit creation from reddit_bot.py
            return True
        else:
            await channel.send('Only {.author} can reply with subreddits to track'.format(message))
            return False

    def addFlairs(m):
        if m.author.id == message.author.id:
            flairList = m.content.split(',')

        else:
            await channel.send('Only {.author} can reply with flairs to track'.format(message))
            return False

    await channel.send('What subreddits do you want to track? (Space Separated)')

    msg = await client.wait_for('message', addSubreddits=addSubreddits)

    if msg == false:
        await channel.send('Setup failed')
        return


    await channel.send('What subreddits do you want to track? (Space Separated)')
    msg = msg = await client.wait_for('message', addFlairs=addFlairs)

    if msg == True:
        await channel.send('Setup complete')
        return
    else:
        await channel.send('Setup failed')


#async def leave(message):



@client.event
async def on_ready():
    print("Logged in as: {0.user}".format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

@client.event
async def display_new_posts():
    await 

client.run(discord_token)