import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
import random
from better_profanity import profanity
from replit import db
import requests
from bs4 import BeautifulSoup

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
ROLE = os.getenv('DISCORD_ROLE')
CHANNEL = os.getenv('DISCORD_CHANNEL')
intents = discord.Intents.all()
client = commands.Bot(command_prefix='-', intents=intents)
client.remove_command('help')


@client.group(invoke_without_command=True)
async def help(ctx):
    embed = discord.Embed(title='Help', description="Use -help <command> for extended information on a command.",
                          color=random.randint(0, 1627775))
    embed.add_field(name='Moderation', value='kick, ban, unban')
    embed.add_field(name='Fun', value='play')
    embed.add_field(name='Messages', value='get')
    embed.add_field(name='Status', value='ping, status')
    await ctx.send(embed=embed)
    await ctx.send('```**WARNING!!: Toxicity will result in ban from the guild.**```')


@help.command()
async def status(ctx):
    embed = discord.Embed(title='status', description="Display the guild status.",
                          color=random.randint(0, 1627775))
    embed.add_field(name='**Syntax**', value='-status')
    await ctx.send(embed=embed)


@help.command()
async def ping(ctx):
    embed = discord.Embed(title='ping', description="Display the ping of the bot.",
                          color=random.randint(0, 1627775))
    embed.add_field(name='**Syntax**', value='-ping')
    await ctx.send(embed=embed)


@help.command()
async def kick(ctx):
    embed = discord.Embed(title='kick', description="kicks a member from the guild.",
                          color=random.randint(0, 1627775))
    embed.add_field(name='**Syntax**', value='-kick <member> [reason]')
    await ctx.send(embed=embed)


@help.command()
async def ban(ctx):
    embed = discord.Embed(title='Ban', description="Bans a member from the guild.",
                          color=random.randint(0, 1627775))
    embed.add_field(name='**Syntax**', value='-ban <member> [reason]')
    await ctx.send(embed=embed)


@help.command()
async def unban(ctx):
    embed = discord.Embed(title='Unban', description="Unbans a member.",
                          color=random.randint(0, 1627775))
    embed.add_field(name='**Syntax**', value='-unban <member>')
    await ctx.send(embed=embed)


@help.command()
async def play(ctx):
    embed = discord.Embed(title='Play', description="Play a game with Vega.",
                          color=random.randint(0, 1627775))
    embed.add_field(name='**Syntax**', value='-play <game>\n\nHere are some of the games available right now'
                    '\nrock --> Play Rock Paper Scissors'
                    '\ntoss --> Flips a coin'
                    '\nrandom --> Generates a random number (range has to be specified)')
    await ctx.send(embed=embed)


@help.command()
async def get(ctx):
    embed = discord.Embed(title='Get', description="Fetch chat history",
                          color=random.randint(0, 1627775))
    embed.add_field(name='**Syntax**', value='-get <command> [<limit> <channel>]'
                    '\n\n**Command**\n'
                    'messages --> get chat history of the channel\n'
                    'links --> get links from the channel'
                    '\n\n**limit**\n'
                    'integer from 1 to 999999\n'
                    '\n\n**channel**\n'
                    'specify the name of the channel')

    await ctx.send(embed=embed)


@client.event
async def on_ready():
    print(f'{client.user} connected to server!')


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please pass in all required arguments or please check the command.')


@client.event
async def on_message(message):
    await client.process_commands(message)
    text = profanity.censor(str(message.content))
    if text != str(message.content):
        await message.channel.send(f'{message.author} mind your language\n'
                                   f'```Message by {message.author}: "{text}" has been recorded for review```')
        if str(message.author) not in db.keys():
            db[str(message.author)] = 1
        else:
            db[str(message.author)] += 1
        if db[str(message.author)] > 15:
            await message.channel.send(f'{message.author} has been banned for toxicity')
            await message.author.ban(reason='Toxicity')
        # del db[str(message.author)]


@client.event
async def on_member_join(member):
    await client.get_channel(int(CHANNEL)).send(f'Welcome {member}!')
    await client.get_channel(int(CHANNEL)).send('```**NOTE: Toxicity will result in ban from the guild.**```')


@client.event
async def on_member_remove(member):
    await client.get_channel(int(CHANNEL)).send(f'{member} has been removed :(')
    await client.get_channel(int(CHANNEL)).send('```**NOTE: Toxicity will result in ban from the guild.**```')


@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency*1000)}ms')


@client.command()
async def status(ctx):
    def filter_only_bots(member):
        if str(member.status) != 'offline' and member.bot:
            return member

    def filter_only_bots_offline(member):
        if str(member.status) == 'offline' and member.bot:
            return member

    def filter_only_users(member):
        if str(member.status) != 'offline' and not member.bot:
            return member

    def filter_only_users_offline(member):
        if str(member.status) == 'offline' and not member.bot:
            return member

    members = ctx.guild.members
    bots = list(filter(filter_only_bots, members))
    bots = [str(member.name)+"#"+str(member.discriminator) for member in bots]

    offline_bots = list(filter(filter_only_bots_offline, members))
    offline_bots = [str(member.name)+"#"+str(member.discriminator) for member in offline_bots]

    bots_online = len(bots)
    bots_offline = len(offline_bots)

    offline_bots = '\n- '.join(offline_bots) if len(offline_bots) > 0 else "NA"
    bots = '\n+ '.join(bots) if len(bots) > 0 else "NA"

    users = list(filter(filter_only_users, members))
    users = [str(member.name)+"#"+str(member.discriminator) for member in users]

    offline_users = list(filter(filter_only_users_offline, members))
    offline_users = [str(member.name)+"#"+str(member.discriminator) for member in offline_users]

    users_online = len(users)
    users_offline = len(offline_users)

    offline_users = '\n- '.join(offline_users) if len(offline_users) > 0 else "NA"
    users = '\n+ '.join(users) if len(users) > 0 else "NA"

    embed = discord.Embed(title="Server Status", description="Here's the status of your server",
                          color=random.randint(0, 1677725))

    embed.add_field(name=f'Users Online: {users_online}', value=f"""```diff\n+ {users}```""")
    embed.add_field(name=f'Users Offline: {users_offline}', value=f"""```diff\n- {offline_users}```""")
    embed.add_field(name=f'Bots Online: {bots_online}', value=f"""```diff\n+ {bots}```""")
    embed.add_field(name=f'Bots Offline: {bots_offline}', value=f"""```diff\n- {offline_bots}```""")

    await ctx.send(embed=embed)


@client.command(aliases=['8ball', 'test'])
async def _8ball(ctx, *, question):
    responses = [
        "It is certain.",
        "It is decidedly so.",
        "Without a doubt.",
        "Yes - definitely.",
        "You may rely on it.",
        "As I see it, yes.",
        "Most likely.",
        "Outlook good.",
        "Yes.",
        "Signs point to yes.",
        "Reply hazy, try again.",
        "Ask again later.",
        "Better not tell you now.",
        "Cannot predict now.",
        "Concentrate and ask again.",
        "Don't count on it.",
        "My reply is no.",
        "My sources say no.",
        "Outlook not so good.",
        "Very doubtful."
    ]
    await ctx.send(f'Question: {question}\n Answer: {random.choice(responses)}')


@client.command()
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)


@client.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    print([role.id for role in ctx.message.author.roles])
    if str(ROLE) in [str(role.id) for role in ctx.message.author.roles]:
        await member.kick(reason=reason)
        await ctx.send(f'kicked {member.mention}')
    else:
        await ctx.channel.send(f'You do not have permission to kick {member.mention}')


@client.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    if str(ROLE) in [str(role.id) for role in ctx.message.author.roles]:
        await member.ban(reason=reason)
        await ctx.send(f'Banned {member.mention}\nreason:{reason}')
    else:
        await ctx.channel.send(f'You do not have permission to ban{member.mention}')


@client.command()
async def unban(ctx, *, member):
    if str(ROLE) in [str(role.id) for role in ctx.message.author.roles]:
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for banned_user in banned_users:
            user = banned_user.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'Unbanned {user.mention}')
                return
    else:
        await ctx.channel.send(f'You do not have permission to unban{member}')


@client.command()
async def play(ctx, game):
    if str(game) == 'rock':
        await ctx.send(f"""```fix\nHey {ctx.message.author}! Lets begin Rock Paper Scissor```""")
        await ctx.send(f"""```On the scale of 0-5 How many rounds would you like to play ?```""")

        points = {'rock': 2, 'paper': 0, 'scissor': 1}
        b = 0
        u = 0

        def check(m):
            return True if len(str(m.content)) > 0 else False

        msg = await client.wait_for('message', check=check)
        results = [
            "```diff\n- Am I a joke to you??```",
            f"```diff\n+ You win {msg.author}```",
            "```diff\n+ I win HAHA```",
            f"```diff\n- Sorry {msg.author} you lose```"
        ]
        if str(msg.content) == '0':
            await ctx.send(results[random.randint(0, 3)])

        else:
            while not str(msg.content).isdigit():
                await ctx.send('```Please enter a digit between 0 - 5```')
                msg = await client.wait_for('message', check=check)

            print(msg.content)

            for i in range(int(msg.content)):
                await ctx.send("""```Rock, Paper, or Scissor?```""")
                u_choice = await client.wait_for('message', check=check)
                b_choice = ['Rock', 'Paper', 'Scissor'][random.randint(0, 2)]

                if points[str(b_choice).lower()] > points[str(u_choice.content).lower()]:
                    b += 1

                elif points[str(b_choice).lower()] < points[str(u_choice.content).lower()]:
                    u += 1

                elif points[str(b_choice).lower()] == points[str(u_choice.content).lower()]:
                    b += 1
                    u += 1

                embed = discord.Embed(title="Scores", color=random.randint(0, 1677725))
                embed.add_field(name='Vega', value=f'**{str(b)}**')
                embed.add_field(name=f'{ctx.message.author}', value=f'**{str(u)}**')
                await ctx.send(embed=embed)
                # await message.channel.send(f'''```Scores: \nVega:{b}\t{message.author}:{u}```''')

            if b > u:
                await ctx.send(random.choice(
                    ['```diff\n- Vega Wins```',
                     '```diff\n- I win my dear friend```',
                     f'```diff\n- Dear {ctx.message.author} I win```'
                     ])
                )

            elif b < u:
                await ctx.send(random.choice(
                    [f'```diff\n+ {ctx.message.author} Wins```',
                     '```diff\n+ Vega lost :(```',
                     f'```diff\n+ You win this time {ctx.message.author}```'
                     ]
                ))

            else:
                await ctx.send("""```fix\nIts a Tie```""")

            await ctx.send("""```fix\nGame Over```""")

    elif str(game) == 'toss':
        coins = ['Head', 'Tail']
        await ctx.send(random.choice(coins))

    elif str(game) == 'random':
        await ctx.send('```Enter the range to generate a random number\nExample: 0-6, 1-9, etc.```')

        def check(m):
            return True if len(str(m)) > 0 else False

        msg = await client.wait_for('message', check=check)
        msg1, msg2 = [int(i) for i in str(msg.content).split('-')]
        await ctx.send(random.randint(msg1, msg2))


@client.command()
async def get(ctx, command='messages', *, limit=5, channel='general'):
    messages = discord.utils.get(ctx.message.guild.text_channels, name=channel)
    messages = await messages.history(limit=limit).flatten()

    if command == 'messages':
        data = [str(i.author) + ":" + str(i.content) + "\n" for i in messages]
        embed = discord.Embed(title="Messages", description="Here's the chat history of this channel",
                              color=random.randint(0, 1677725))
        for i in data:
            a = i.split(':')
            try:
                embed.add_field(name=a[0], value=''.join(a[1:]) if a[1] != '\n' else 'None')

            except Exception as e:
                print(e)

        await ctx.send(embed=embed)

    if command == 'links':
        data = [str(i.content) for i in messages if 'http' in str(i.content) or 'https' in str(i.content)]
        embed = discord.Embed(title="Links", description="Here are some of the links from this channel",
                              color=random.randint(0, 1677725))
        links = list()

        if len(data) > 0:
            for i, j in enumerate(data):
                response = requests.get(j.strip())
                soup = BeautifulSoup(response.text, features='html.parser')
                metas = soup.findAll('meta')

                for meta in metas:
                    if 'name' in meta.attrs and 'description' in meta.attrs['name'].lower():
                        if len(meta.attrs['content']) > 0 and j not in links:
                            embed.add_field(name=j, value=meta.attrs['content'])
                            links.append(j)

                else:
                    if j not in links:
                        embed.add_field(name=j, value='None')
                        links.append(j)

            await ctx.send(embed=embed)
        else:
            embed.add_field(name='No links found', value='NA')
            await ctx.send(embed=embed)


client.run(TOKEN)
