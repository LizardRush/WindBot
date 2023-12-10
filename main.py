import os
import discord

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

terminal_channel_name = 'terminal'

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$create_terminal') and message.author.guild_permissions.administrator:
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

    if message.content.startswith('$recover_server') and message.author.guild_permissions.administrator:
        terminal_channel = discord.utils.get(message.guild.channels, name=terminal_channel_name, type=discord.ChannelType.text)

        if terminal_channel and message.channel == terminal_channel:
            # Server recovery initiated from the terminal channel
            await message.channel.send("Initiating server recovery...")
            await recover_server(message.guild, message)  # Pass 'message' as an argument
        elif not terminal_channel:
            # Terminal channel doesn't exist; proceed with server recovery
            await message.channel.send("Terminal channel doesn't exist. Initiating server recovery...")
            await recover_server(message.guild, message)  # Pass 'message' as an argument
        else:
            await message.channel.send("You can only use the server recovery command in the terminal channel.")

async def recover_server(guild, message):  # Accept 'message' as an argument
    # Your recovery logic here...
    # Delete channels, create categories, etc.

    if message.channel.name == 'terminal':
        await message.delete()

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
