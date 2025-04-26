# LunisBot
> "I'm not here to be helpful. I'm here to be _right_." – LunisBot probably

**LunisBot** is an AI Discord bot designed to roleplay a sarcastic, easily-annoyed, no-nonsense software engineer loosely inspired by Linus Torvalds. It lurks in your chat and ignores most of what you say, but when it _does_ respond, it's probably to roast you. And you probably deserved it.

This bot was created purely for fun, to troll a troll in one of my Discord servers who thought arguing with a bot that sent random Linus Torvalds quotes was a good use of his time. I wasted 3 hours building this so that you can waste your time too.

## ✨ Features

* Selective human-like responses based on context, message relevance, and keywords
* Blunt, sarcastic, and straight-up rude
* Short, casual, no-flood messages (because Lunis has better things to do than talking to you)
* Roasts your bad code
* Randomly ignores people like a real person unless directly provoked

## ⁉️ Why would you do this?

Because sometimes you need to build something that serves no real purpose just to brighten the mood. That's the biggest W use of AI. Also, AI _should_ be used to put the trolls in their place.

## 🛠️ Deployment

You will need to install Python, the `ollama` client, and local `llama-3.2` weights. You will also need a Discord API key. The minimal Discord permissions required by the bot are **send messages** and **read message history**. You can optionally also allow **sending messages in threads**.

After you do that, start by cloning the repo:

```bash
git clone https://github.com/jewelcodes/lunisbot.git
cd lunisbot
```

Next, save your API key in your `.env` file:

```bash
echo "DISCORD_API_KEY=your-api-key-goes-here" > .env
```

Finally, install the requirements and run the bot:

```bash
python3 -m pip install -r requirements.txt
python3 lunisbot.py
```

## 🫶🏼 Credits
* Linus Torvalds for being the absolute genius he is
* The troll who was arguing with a bot for giving me this idea
* [@Dcraftbg](https://github.com/Dcraftbg) for coming up with the name LunisBot
* Me, for wasting a perfectly sunny day staying in to build this

## ⚖️ License

GPLv2 because Linus Torvalds said the GPLv3 sucks – and honestly who am I to argue with him?

`// EOF`
