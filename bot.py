import os
import discord
from discord.ext import commands
intents = discord.Intents.default()
intents.message_content = True
# Create an instance of commands.Bot
bot = commands.Bot(command_prefix='$', intents=intents)
  # Set your desired command prefix here

# Define your bot commands, events, and other functionalities
# ...

# Ensure to start the bot using bot.run()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

terminal_channel_name = 'terminal'
recovery_running = False
guild_id = 1167262054609064007

async def restore_terminal(guild):
    terminal_channel = discord.utils.get(guild.channels, name='terminal', type=discord.ChannelType.text)
    if terminal_channel:
        print('Restoring Terminal...')
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True)
        }
        await terminal_channel.edit(overwrites=overwrites)
        print('Terminal Recovered!')
    else:
        print("Failed To Recover, Terminal Channel Exists")


@client.event
async def on_ready():
    print('Logged In With Token MTE3MDM5MDkzNjY0NDIzNTMxNQ...')
async def recover_server(guild):
    global recovery_running
    if recovery_running:
        return

    recovery_running = True

    # Perform the recovery process here...
    # For example: Delete existing channels, create new ones, rename the guild, etc.

    # Simulating the recovery process for demonstration purposes
    print("Server Recovery Process Triggered")
    print("Deleting existing channels...")
    for channel in guild.channels:
        await channel.delete()

    print("Creating new categories and channels...")
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

    print("Renaming the guild...")
    new_guild_name = 'Windy Bee'
    await guild.edit(name=new_guild_name)
    
    recovery_running = False
async def ban_spammer(guild, user):
    # If a member gets banned, initiate server recovery
    await user.ban(reason="Spamming")
    await guild.owner.send(f"{user.mention} has been banned for spamming. Initiating server recovery")
    await recover_server(guild)  # Call the recover_server function
@client.event
async def on_message(message):
    # Anti-spam mechanism
    # You can adjust these variables to suit your needs
    spam_threshold = 10  # Number of messages within the timeframe
    spam_seconds = 5  # Timeframe in seconds

    if message.author.bot:
        return  # Ignore bot messages

    user = message.author
    channel = message.channel
    user_messages = [msg for msg in channel.history(limit=spam_threshold).flatten() if msg.author == user]

    if len(user_messages) >= spam_threshold:
        # If the user has sent more messages than the threshold within the timeframe
        await ban_spammer(message.guild, user)

    await bot.process_commands(message)
    global recovery_running

    if message.author == client.user:
        return

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
    