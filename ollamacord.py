from dotenv import dotenv_values
import subprocess
from json import load as json_load
import os
import requests
import discord
from discord.ext import commands
from copy import deepcopy

# Load the environment variables
config = dotenv_values('.env')
DISCORD_TOKEN = config['DISCORD_TOKEN']
del config

# Global variables
DEBUG = False
COLOR_HELP = 0x42f933
ERROR_MSG = 'Aucune réponse n\'a été reçue...\n' \
    'Cela peut être dû à une erreur ou à une question trop complexe.'
with open('models.json', 'r') as f:
    MODELS = json_load(f)

# Create the bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)


#-----------------------------#
# METHODS
#-----------------------------#


def ask_ollama(model: str, prompt: str) -> (str | None):
    """Ask a question to the Ollama model."""
    # Run the command and get the output
    command = ['ollama', 'run', model, prompt]
    result = subprocess.run(command, capture_output=True, text=True)

    # Check if the command was successful
    if result.returncode == 0:
        # Return the output of the command
        return result.stdout
    return None


def form_help() -> discord.Embed:
    """Form the help embed message."""
    # Create an embed message
    embed = discord.Embed(
        title='Aide',
        description='Voici une aide pour utiliser Ollamacord:',
        color=COLOR_HELP)
    fields = [
        ('!clear', 'pour effacer le chat'),
        ('!help', 'pour afficher cette aide'),
        ('!stop', 'pour arrêter le bot'),
        ('!quit', 'pour arrêter le bot'),
        ('!raw <question>', 'pour poser une question au modèle sans contexte'),
        ('<question>', 'pour poser une question au modèle'),
        ('Exemple', '`How many legs does a cat have?` -> `4`')
    ]
    for name, value in fields:
        embed.add_field(name=name, value=value, inline=False)
    return embed


def form_message(model: object, message: object) -> str:
    """Form the message to send to the model."""
    prompt = model['context'] + message.content
    # Attachments support
    if len(message.attachments) > 0:
        os.makedirs('tmp', exist_ok=True)
        files_lst = []
        for attachment in message.attachments:
            file = 'tmp/' + attachment.filename
            r = requests.get(attachment.url)
            with open(file, 'wb') as f:
                f.write(r.content)
            files_lst.append(file)
        prompt += '\n'
        for file in files_lst:
            with open(file, 'r') as f:
                prompt += f'\n```{f.read()}```'
            os.remove(file)
    if DEBUG:
        print('Prompt:\n#####\n' + prompt + '\n#####')
    return prompt


async def check_stop(message: str) -> bool:
    """Check if the message is `!stop` or `!quit`."""
    if message.content == '!stop' or message.content == '!quit':
        await message.channel.send('Goodbye!')
        await bot.close()
        return True
    return False


async def check_help(message: str) -> bool:
    """Check if the message is `!help`."""
    if message.content == '!help':
        await message.channel.send(embed=form_help())
        return True
    return False


async def check_clear(message: str) -> bool:
    """Check if the message is `!clear`."""
    if message.content == '!clear':
        await message.channel.purge()
        await message.channel.send(embed=form_help())
        return True
    return False


def check_raw(message: str, models: list[object]):
    """Check if the message is `!raw`."""
    is_raw = message.content.startswith('!raw')
    models_copy = deepcopy(models)
    if is_raw:
        message.content = message.content.replace('!raw', '').strip()
    for model in models_copy:
        if is_raw:
            model['context'] = ''
    return message, models_copy


async def check_model(message: object, model: object) -> bool:
    """Check if the message is for a specific model."""
    # If channel is model
    if message.channel.name == model['channel']:
        print(f'Asking {model["name"]}...')
        # Ask model
        response = ask_ollama(
            model=model['name'],
            prompt=form_message(model, message)
        )

        # Send answer
        if response is not None:
            embed = discord.Embed(
                title=model['name'].capitalize(),
                description=response,
                color=int(model['color'], 16)
            )
            await message.channel.send(embed=embed)
        else:
            await message.channel.send(ERROR_MSG)
        return True
    return False


#-----------------------------#
# EVENTS
#-----------------------------#


@bot.event
async def on_ready() -> None:
    print(f'We have logged in as {bot.user}')


@bot.event
async def on_message(message: object) -> None:
    models_list = [model['channel'] for model in MODELS]
    if DEBUG:
        print(message.channel.name, message.content)
    # Restrict the bot to the DISCORD_CHANNEL
    # [{channel: str, name: str, context: str, color: int}, ...]
    if message.channel.name not in models_list:
        return None

    if DEBUG:
        print('Passed channel check')

    # Ignore messages from the bot itself
    if message.author == bot.user:
        return None

    if DEBUG:
        print('Passed author check')

    # Log the message
    print(f'{message.author}: {message.content}')

    # Check commands
    is_stop = await check_stop(message)
    is_help = await check_help(message)
    is_clear = await check_clear(message)
    if is_stop or is_help or is_clear:
        return None
    message, models = check_raw(message, MODELS)

    # Stop unknown commands
    if message.content.startswith('!'):
        return None

    if DEBUG:
        print('Passed command check')

    # Check models
    for model in models:
        if await check_model(message, model):
            return None


#-----------------------------#
# MAIN
#-----------------------------#

if __name__ == '__main__':
    bot.run(token=DISCORD_TOKEN)
