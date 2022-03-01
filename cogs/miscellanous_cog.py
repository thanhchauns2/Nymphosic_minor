import os
import random
import playsound
from discord.ext import commands
import discord
from utils import search_pictures
import shutil
from utils.embed_handler import *

class _Misc(commands.Cog, name = "Miscelaneous"):
    def __init__(self, client):
        self.client = client

    # Miscelaneous zone

        # servers_count

    @commands.command(brief = "Count the number of guilds I'm currently in", aliases = ['gc'], description = "Count the number of guilds I'm currently in")
    async def guild_count(self, ctx):
        try:
            await ctx.send(embed = single_message(self.client, "I'm in " + str(len(self.client.guilds)) + " servers!"))
        except Exception as e:
            await ctx.send(embed = error_handler(self.client, e, ctx))

        # ~servers_count
    
        # search_image

    @commands.command(brief = "Search an image of anything", aliases = ['se'], description = "Search an image of anything")
    async def search(self, ctx, *text):
        txt = ""
        for i in text:
            txt += i + ' '
        path = str(os.getcwdb())[2:-1].replace('\\\\','/') + '/dataset/pictures/' + str(ctx.message.author.id)
        if os.path.exists(path):
            shutil.rmtree(path)
        os.makedirs(path)
        search_pictures.download(txt, path)
        f = random.choice(os.listdir(path))
        f = path + '/' + f
        await ctx.send(file=discord.File(f), embed = single_message(self.client, "Is this what you were looking for?"))

        # ~search_image

        # random_number

    @commands.command(brief = "Generate a random number", description = "Generate a random number in range [a, b]", aliases = ["rd"])
    async def rand(self, ctx, a = 0, b = 100):
        # await ctx.send('ready')
        k = random.randint(a, b)
        await ctx.send(embed = single_message(self.client, "Random number: " + str(k)))
        print(k)

        # ~random_number

        # gift_music

    # @commands.command(brief = "Gift admin some music", hidden = True)
    # async def gotem(self, ctx):
    #     await ctx.send('Playing \"hare hare ya\"')
    #     path = str(os.getcwdb())[2:-1].replace('\\\\','\\') + '\\hare hare ya.mp3'
    #     playsound.playsound(path)

        # ~gift_music

        # waifu(s)

    # @commands.command(brief = "Dev\'s waifu(s)", hidden = True)
    # async def waifu(self, ctx):
    #     path = str(os.getcwdb())[2:-1].replace('\\\\','\\') + '\\dataset\\waifu'
    #     f = random.choice(os.listdir(path))
    #     f = path + "\\" + f
    #     await ctx.send(file=discord.File(f), embed = single_message(self.client, "My waifu!"))

        # ~waifu(s)

        # author_info

    # @commands.command(brief = "author dep trai so mot he mat troi", hidden = True)
    # async def cursorceror(self, ctx):
    #     path = str(os.getcwdb())[2:-1].replace('\\\\','\\') + '\\dataset\\author'
    #     f = random.choice(os.listdir(path))
    #     f = path + "\\" + f
    #     await ctx.send(file=discord.File(f))

        # ~author_info

    # ~Miscellaneous zone

def setup(bot):

    bot.add_cog(_Misc(bot))
