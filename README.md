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

## License

This project is for educational purpose only. Under the GNU v3.0 [license](LICENSE).
