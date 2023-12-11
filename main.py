import os
import discord

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

terminal_channel_name = 'terminal'

@client.event
async def on_ready():
    print('Logged In With Token MTE3MDM5MDkzNjY0NDIzNTMxNQ...')

@client.event
async def recover_server(guild, message):
    # Delete existing channels and categories
    for channel in guild.channels:
        await channel.delete()
    for category in guild.categories:
        await category.delete()

    # Rename the guild (server)
    new_guild_name = 'Windy Bee'
    await guild.edit(name=new_guild_name)

    # Create categories and channels
    category_names = ['Announcements', 'Text Channels', 'VC']
    for category_name in category_names:
        category = await guild.create_category(category_name)

        if category_name == 'Announcements':
            for channel_name in ['joins', 'discord-updates', 'rules', 'announcements']: 
                await category.create_text_channel(channel_name)
        if category_name == 'Text Channels':
            for channel_name in ['general', 'bot-commands', 'sparky']:
                await category.create_text_channel(channel_name)

        if category_name == 'VC':
            await category.create_voice_channel('General')
    await send_rules_message(guild)
    await create_terminal(message)
# rules message
async def send_rules_message(guild):
    # Send rules message in the 'rules' channel
    rules_channel = discord.utils.get(guild.channels, name='rules', type=discord.ChannelType.text)
    if rules_channel:
        rules_message = """RULES:
        1: No N Word
        2: No Memes In General
        3: Follow Discord ToS
        4: No Bot Abuse
        5: No Doxxing
        6: No Flexing"""
        await rules_channel.send(rules_message)
    else:
        print("The 'rules' channel does not exist.")
async def create_terminal(message):
    terminal_channel = discord.utils.get(message.guild.channels, name='terminal', type=discord.ChannelType.text)
    if not terminal_channel:
        overwrites = {
            message.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            message.guild.me: discord.PermissionOverwrite(read_messages=True)
        }
        new_terminal_channel = await message.guild.create_text_channel('terminal', overwrites=overwrites)
        await message.channel.send("Terminal channel created successfully.")
    else:
        await message.channel.send("Terminal channel already exists.")
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('$send_rules_message') and message.author.guild_permissions.administrator:
        terminal_channel = discord.utils.get(message.guild.channels, name='terminal', type=discord.ChannelType.text)
        if not terminal_channel:
            await create_terminal(message)
            await message.channel.send("Terminal channel created successfully.")
        else:
            await message.channel.send("Terminal channel already exists.")

        if terminal_channel and message.channel == terminal_channel:
            await message.channel.send("Sending rules message in terminal...")
            await send_rules_message(message.guild)
        else:
            await message.channel.send("You can only send the rules message in the terminal channel.")
    # create terminal command
    if message.content.startswith('$create_terminal') and message.author.guild_permissions.administrator:
        await create_terminal(message)
    # sever recovery command
    if message.content.startswith('$recover_server') and message.author.guild_permissions.administrator:
        terminal_channel = discord.utils.get(message.guild.channels, name=terminal_channel_name, type=discord.ChannelType.text)

        if terminal_channel and message.channel == terminal_channel:
            # Server recovery initiated from the terminal channel
            await message.channel.send("Initiating server recovery...")
            await recover_server(message.guild, message)
        elif not terminal_channel:
            # Terminal channel doesn't exist; proceed with server recovery
            await message.channel.send("Terminal channel doesn't exist. Initiating server recovery...")
            await recover_server(message.guild, message)
        else:
            await message.channel.send("You can only use the server recovery command in the terminal channel.")
# recover the server
try:
    token = os.getenv("TOKEN") or ""
    if token == "":
        raise Exception("Please add your token to the Secrets pane.")
    client.run(token)
except discord.HTTPException as e:
    if e.status == 429:
        print(
            "The Discord servers denied the connection for making too many requests"
        )
        print(
            "Get help from https://stackoverflow.com/questions/66724687/in-discord-py-how-to-solve-the-error-for-toomanyrequests"
        )
    else:
        raise e
