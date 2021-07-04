import random
import discord
import requests
from bs4 import BeautifulSoup


class Messages:
    def __init__(self, messages, message, guild):
        self.__messages = messages
        self.__message = message
        self.__guild = guild

    def filterOnlyBots(self, member):
        if str(member.status) != 'offline' and member.bot:
            return str(member.name)+"#"+str(member.discriminator)

    def filterOnlyBotsOffline(self, member):
        if str(member.status) == 'offline' and member.bot:
            return str(member.name)+"#"+str(member.discriminator)

    def filterOnlyUsers(self, member):
        if str(member.status) != 'offline' and not member.bot:
            return str(member.name)+"#"+str(member.discriminator)

    def filterOnlyUsersOffline(self, member):
        if str(member.status) == 'offline' and not member.bot:
            return str(member.name)+"#"+str(member.discriminator)

    async def get_help(self):
        embed = discord.Embed(title="Help", description="Below are some of the commands",
                              color=random.randint(0, 1677725))
        embed.add_field(name='- get messages', value='```fix\nDisplay the chat history of the channel```')
        embed.add_field(name='- get links', value='```fix\nDisplay the links shared in the channel```')
        embed.add_field(name='- get status', value="""```fix\nDisplay the number of participants```""")
        embed.add_field(name='- play rock', value='```fix\nPlay Rock, Paper, Scissor with Vega```')

        embed.set_author(name='Vega', icon_url=self.__guild.icon_url)
        print(self.__guild.id)
        await self.__message.channel.send(embed=embed)

    async def get_messages(self):
        data = [str(i.author)+":"+str(i.content)+"\n" for i in self.__messages]
        embed = discord.Embed(title="Messages", description="Here's the chat history of this channel",
                              color=random.randint(0, 1677725))
        for i in data:
            a = i.split(':')
            try:
                embed.add_field(name=a[0], value=''.join(a[1:]) if a[1] != '\n' else 'None')
            except Exception as e:
                print(e)
        await self.__message.channel.send(embed=embed)

    async def get_links(self):
        data = [str(i.content) + "\n" for i in self.__messages if 'http' in str(i.content) or 'https' in str(i.content)]
        print(data)
        embed = discord.Embed(title="Links", description="Here are some of the links from this channel",
                              color=random.randint(0, 1677725))
        links = list()
        for i, j in enumerate(data):
            response = requests.get(j.strip('\n'))
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

        await self.__message.channel.send(embed=embed)

    async def get_status(self):
        members = self.__message.guild.members
        channel = self.__message.channel

        bots = list(filter(self.filterOnlyBots, members))
        bots = [str(member.name)+"#"+str(member.discriminator) for member in bots]

        offline_bots = list(filter(self.filterOnlyBotsOffline, members))
        offline_bots = [str(member.name)+"#"+str(member.discriminator) for member in offline_bots]

        bots_online = len(bots)
        bots_offline = len(offline_bots)

        offline_bots = '\n- '.join(offline_bots) if len(offline_bots) > 0 else "NA"
        bots = '\n+ '.join(bots) if len(bots) > 0 else "NA"

        users = list(filter(self.filterOnlyUsers, members))
        users = [str(member.name)+"#"+str(member.discriminator) for member in users]

        offline_users = list(filter(self.filterOnlyUsersOffline, members))
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

        await self.__message.channel.send(embed=embed)
