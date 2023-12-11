import os
import discord

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

terminal_channel_name = 'terminal'
recovery_running = False

@client.event
async def on_ready():
    print('Logged In With Token MTE3MDM5MDkzNjY0NDIzNTMxNQ...')

async def recover_server(guild):
    global recovery_running
    if recovery_running:
        return

    recovery_running = True
    # Rest of the recovery process...

    # After the recovery process is complete:
    recovery_running = False

# Other functions and event handlers...

@client.event
async def on_message(message):
    global recovery_running

    # Other commands...

    if message.content.startswith('$recover_server') and message.author.guild_permissions.administrator:
        terminal_channel = discord.utils.get(message.guild.channels, name=terminal_channel_name, type=discord.ChannelType.text)

        if terminal_channel and message.channel == terminal_channel:
            if not recovery_running:
                await message.channel.send("Initiating server recovery...")
                await recover_server(message.guild)
            else:
                await message.channel.send("Recovery process is already running.")
        elif not terminal_channel:
            await message.channel.send("Terminal channel doesn't exist. Initiating server recovery...")
            if not recovery_running:
                await recover_server(message.guild)
            else:
                await message.channel.send("Recovery process is already running.")
        else:
            await message.channel.send("You can only use the server recovery command in the terminal channel.")

# Recover the server using your bot token
try:
    token = os.getenv("TOKEN") or ""
    if token == "":
        raise Exception("Please add your token to the Secrets pane.")
    client.run(token)
except discord.HTTPException as e:
    if e.status == 429:
        print("The Discord servers denied the connection for making too many requests")
        print("Get help from https://stackoverflow.com/questions/66724687/in-discord-py-how-to-solve-the-error-for-toomanyrequests")
    else:
        raise e
