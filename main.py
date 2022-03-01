import discord
from discord.ext import commands
import config
import traceback
import os
from utils import embed_handler
# from keep_alive import keep_alive

client = commands.Bot(command_prefix = "n!")

class CustomHelp(commands.HelpCommand):

    async def send_bot_help(self, mapping):

        cogs = {}

        embed = embed_handler.single_message(client, "Help")
        embed.title = "Commands list"

        for cog in client.cogs:
            embed.add_field(name = f"{cog}", value = "`" + "`, `".join(cmd.name for cmd in client.cogs[cog].walk_commands()) + "`", inline = False)     

        embed.add_field(name = f"Use `{client.command_prefix}help <command/category>` for more info.", value = "\u200b", inline = False)

        await self.context.reply(embed = embed, mention_author = False)

    async def send_command_help(self, command):
 
        embed = embed_handler.single_message(client, "Help")

        embed.title = self.get_command_signature(command)
        embed.add_field(name = "Description", value = command.description)

        if command.aliases:
            embed.add_field(name = "Aliases", value = "`" + "`, `".join(command.aliases) + "`", inline = False)
        else:
            embed.add_field(name = "Aliases", value = "No alias", inline = False)

        await self.context.reply(embed = embed, mention_author = False)

    async def send_cog_help(self, cog):

        embed = embed_handler.single_message(client, "Help")

        embed.title = cog.qualified_name
        embed.description = "\n".join(f'`{command.qualified_name}`ㅤㅤㅤ{command.brief}' for command in cog.walk_commands())

        await self.context.reply(embed = embed, mention_author = False)

    async def send_error_message(self, error):

        embed = embed_handler.single_message(client, "Command or cog not found")
        
        if str(error).startswith("No command called"):

            command = error.split(" ")[3].replace('"', '')

            embed.description = f'Command or cog named `{command}` not found.'

            await self.context.reply(embed = embed, mention_author = False)

        else:

            embed = embed_handler.single_message(client, "Unknown error occured")

            embed.description = f'```py{str(error)}```'
            embed.title = "An error occurred."

            await self.context.reply(embed = embed, mention_author = False)

client.help_command = CustomHelp()

@client.event
async def on_command_error(ctx, exception):

    if isinstance(exception, commands.CommandNotFound):

        words = str(exception).split(" ")
        words[1] = words[1].replace('"', "")

        await ctx.reply(f'Command `{words[1]}` not found.', mention_author = False)

    elif isinstance(exception, commands.BadArgument): 

        await ctx.reply('Argument(s) are not valid.', mention_author = False)

    elif isinstance(exception, commands.NoPrivateMessage):

        await ctx.reply('This command cannot be used inside DM.', mention_author = False)

    elif isinstance(exception, commands.errors.CommandOnCooldown):

        await ctx.reply(f"You can't use this command right now, try again in {str(exception).split(' ')[7]}.", mention_author = False)

    else:

        print(''.join(traceback.format_exception(None, exception, exception.__traceback__)))

@client.event
async def on_connect():
    print(f'Connected to Discord!\n')

    await client.wait_until_ready()

    owner = await client.fetch_user(client.owner_id)

    print(f'''Logged in as: {client.user.name}#{client.user.discriminator} - {client.user.id}\nOwner: {owner.name}#{owner.discriminator}\nDiscord API wrapper version: {discord.__version__}\n''')

    for file in os.listdir("./cogs"):
        if file.endswith(".py"):
            extension = file[:-3]
            try:
                client.load_extension(f"cogs.{extension}")
                print(f"Loaded extension '{extension}'")
            except Exception as exc:
                print(f"Failed to load extension {extension}.\n{''.join(traceback.format_exception(exc.__class__, exc, exc.__traceback__))}")
    
    print(f'\nReady!')

# keep_alive()
# client.run(config.token) # dev_bot
client.run('') # token
