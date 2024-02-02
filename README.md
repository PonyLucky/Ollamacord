# Ollamacord

This is a bot to use ollama from Discord. The bot connects to the discord guild/server then wait for an input in some channels (each model has its channel) and then answer.

I use the commandline because the API is 5x slower for some reason. If `ollama run mistral` doesn't work in your computer you need to **update the command** in `ask_ollama` method in `ollamacord.py`.

## Install

1) Open a terminal in the project's directory.
2) **(optional)** `python3 -m venv .venv`
3) **(optional)** `source .venv/bin/activate`
4) `pip3 install -r requirements.txt`

## Run

```sh
python3 ollamacord.py
# Or
source .venv/bin/activate
python3 ollamacord.py
```

## Personalize

### `models.json`

This file contains the list of models with their configurations :

- `"name"` - Name of model in ollama (mistral:latest, llama2, etc.).
- `"channel"` - Name of channel in discord guild/server.
- `"color"` - Color in hexadecimal of the left border of the 'message' in Discord (called an embed).
- `"context"` - Prompt to send before all messages sent from Discord.

This way, even with the same model you can do a channel `mistral-math` for math lessons and then a `mistral-code`, `mistral-minecraft-help`, etc.

### `ollamacord.py`

The application source code, you can change the language as it is in French for `help` method and if error from ollama in `ERROR_MSG` variable.

## License

This project is for educational purpose only. Under the GNU v3.0 [license](LICENSE).
