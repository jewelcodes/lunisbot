import discord, ollama, random, os, time
from dotenv import load_dotenv

load_dotenv()
random.seed(time.time())

DISCORD_API_TOKEN = os.getenv("DISCORD_API_TOKEN")
DISCORD_MESSAGE_LIMIT = 2000    # discord message limit
LUNIS_CONTEXT_LIMIT = 500       # messages to keep in memory
RESPONSE_RATE = 0.7             # chance of responding to a relevant message
LUNIS_MODEL = "llama3.2"        # model to use for responses

KEYWORDS = ["linux", "linus", "torvalds", "lunis", "kernel", "git", "os",
            "windows", "java", "open-source", "open source"]

assert DISCORD_API_TOKEN, "You need to set DISCORD_API_TOKEN in your .env file"

intents = discord.Intents.default()
intents.message_content = True

lunisbot = discord.Client(intents=intents)

with open("system/linus-persona.txt", "r") as f:
    persona = f.read()

GLOBAL_CONTEXT = [
    {"role": "system", "content": persona}
]

def sanity_truncate(text: str) -> str:
    if len(text) > DISCORD_MESSAGE_LIMIT:
        text = text[:(DISCORD_MESSAGE_LIMIT-5)] + "[...]"
    return text

def is_relevant(text: str) -> bool:
    return any(keyword in text.lower() for keyword in KEYWORDS)

@lunisbot.event
async def on_ready() -> None:
    print(f"LunisBot started as {lunisbot.user.name} ({lunisbot.user.id})")

@lunisbot.event
async def on_message(message: discord.Message) -> None:
    if message.author == lunisbot.user:
        return

    global GLOBAL_CONTEXT
    GLOBAL_CONTEXT.append({
        "role": "user",
        "content": f"{message.author}: {sanity_truncate(message.content)}"
    })

    if len(GLOBAL_CONTEXT) >= LUNIS_CONTEXT_LIMIT:
        GLOBAL_CONTEXT = GLOBAL_CONTEXT[-LUNIS_CONTEXT_LIMIT:]
        GLOBAL_CONTEXT[0] = {"role": "system", "content": persona}

    if is_relevant(message.content) or lunisbot.user.mentioned_in(message):
        if lunisbot.user.mentioned_in(message):
            responding = True
        else:
            responding = random.random() < RESPONSE_RATE

        if responding:
            try:
                response = ollama.chat(LUNIS_MODEL, messages=GLOBAL_CONTEXT)
                if response:
                    response = response.get("message", {}).get("content", "")
                    response.strip()
                else:
                    response = ""
                
                if len(response):
                    if response.lower().startswith("lunisbot:"):
                        response = response[9:]
                    elif response.lower().startswith("model:"):
                        response = response[6:]
                    elif response.lower().startswith("assistant:"):
                        response = response[10:]

                    GLOBAL_CONTEXT.append({
                        "role": "assistant",
                        "content": f"LunisBot: {sanity_truncate(response)}"
                    })
                    await message.channel.send(sanity_truncate(response))
            except Exception as e:
                print(f"Exception while responding: {e}")

lunisbot.run(DISCORD_API_TOKEN)
