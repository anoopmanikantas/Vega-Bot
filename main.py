import os
import random
import discord
from dotenv import load_dotenv
from discord.ext import commands
import Messages

intents = discord.Intents.all()
intents.members = True
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='+', intents=intents)


@bot.event
async def on_ready():
    global guild
    for guild in bot.guilds:
        if str(guild) == GUILD:
            break
    print(
        f'{bot.user} has connected to the server!\n'
        f'{guild.name}(id: {guild.id})'
    )
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n {members}')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    elif message.content.startswith('-'):
        c = discord.utils.get(message.guild.text_channels, name='general')
        messages = await c.history().flatten()
        messages = Messages.Messages(messages=messages, message=message, guild=guild)

        if len(message.content.split()) > 1:
            parameters = message.content.split()[1:]
            if parameters[0] == 'get':
                if parameters[1] == 'messages':
                    await messages.get_messages()
                elif parameters[1] == 'links':
                    await messages.get_links()
                elif parameters[1] == 'status':
                    await messages.get_status()

            elif parameters[0] == 'play':
                if parameters[1] == 'rock':
                    await message.channel.send(f"""```fix\nHey {message.author}! Lets begin Rock Paper Scissor```""")
                    await message.channel.send(f"""```On the scale of 0-5 How many rounds would you like to play ?```""")

                    points = {'rock': 2, 'paper': 0, 'scissor': 1}
                    b = 0
                    u = 0

                    def check(m):
                        return True if len(str(m.content)) > 0 else False

                    msg = await bot.wait_for('message', check=check)
                    results = [
                                "```diff\n- Am I a joke to you??```",
                                f"```diff\n+ You win {msg.author}```",
                                "```diff\n+ I win AHAHA```",
                                f"```diff\n- Sorry {msg.author} you lose```"
                            ]

                    if str(msg.content) == '0':
                        await message.channel.send(results[random.randint(0, 3)])

                    else:
                        while not str(msg.content).isdigit():
                            await message.channel.send('```Please enter a digit between 0 - 5```')
                            msg = await bot.wait_for('message', check=check)

                        print(msg.content)

                        for i in range(int(msg.content)):
                            await message.channel.send("""```Rock, Paper, or Scissor?```""")
                            u_choice = await bot.wait_for('message', check=check)
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
                            embed.add_field(name=f'{message.author}', value=f'**{str(u)}**')
                            await message.channel.send(embed=embed)
                            # await message.channel.send(f'''```Scores: \nVega:{b}\t{message.author}:{u}```''')

                        if b > u:
                            await message.channel.send(
                                ['```diff\n- Vega Wins```',
                                 '```diff\n- I win my dear friend```',
                                 f'```diff\n- Dear {message.author} I win```'
                                ][random.randint(0, 2)]
                            )

                        elif b < u:
                            await message.channel.send(
                                [f'```diff\n+ {message.author} Wins```',
                                 '```diff\n+ Vega lost :(```',
                                 f'```diff\n+ You win this time {message.author}```'
                                 ][random.randint(0, 2)]
                            )

                        else:
                            await message.channel.send("""```fix\nIts a Tie```""")

                        await message.channel.send("""```fix\nGame Over```""")

            elif parameters[0] == 'help':
                await messages.get_help()

bot.run(TOKEN)
