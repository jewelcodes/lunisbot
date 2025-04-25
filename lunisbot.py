import discord, ollama, random, os, time
from dotenv import load_dotenv

load_dotenv()
random.seed(time.time())

DISCORD_API_TOKEN = os.getenv("DISCORD_API_TOKEN")
DISCORD_MESSAGE_LIMIT = 2000    # discord message limit
LUNIS_CONTEXT_LIMIT = 500       # messages to keep in memory
ACTIVITY_THRESHOLD = 120        # time elapsed since last bot response
RESPONSE_RATE = 0.65            # chance of responding to a relevant message
ACTIVE_RESPONSE_RATE = 0.95     # chance of responding to an ongoing conversation
LUNIS_MODEL = "llama3.2"        # model to use for responses

KEYWORDS = ["linux", "linus", "torvalds", "lunis", "kernel", "git", "os",
            "windows", "java", "open-source", "open source"]

assert DISCORD_API_TOKEN, "You need to set DISCORD_API_TOKEN in your .env file"

intents = discord.Intents.default()
intents.message_content = True

lunisbot = discord.Client(intents=intents)

with open("system/linus-persona.txt", "r") as f:
    persona = f.read()

context = [
    {"role": "system", "content": persona}
]

last_activity = time.time()

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
    
    if message.author.global_name:
        user = message.author.global_name
    elif message.author.display_name:
        user = message.author.display_name
    else:
        user = message.author.name

    global context, last_activity
    context.append({
        "role": "user",
        "content": f"{user}: {sanity_truncate(message.content)}"
    })

    if len(context) >= LUNIS_CONTEXT_LIMIT:
        context = context[-LUNIS_CONTEXT_LIMIT:]
        context[0] = {"role": "system", "content": persona}

    relevant = is_relevant(message.content)
    mentioned = lunisbot.user.mentioned_in(message)
    active = (time.time() - last_activity) < ACTIVITY_THRESHOLD

    if relevant or mentioned or active:
        if mentioned:
            responding = True   # unconditionally respond to mentions
        elif active:
            responding = random.random() < ACTIVE_RESPONSE_RATE
        else:
            responding = random.random() < RESPONSE_RATE

        if responding:
            try:
                response = ollama.chat(LUNIS_MODEL, messages=context)
                if response:
                    response = response.get("message", {}).get("content", "")
                    response.strip()
                else:
                    response = ""
                
                if len(response):
                    if response.lower().startswith("lunisbot:"):
                        response = response[9:]
                    elif response.lower().startswith("lunis:"):
                        response = response[6:]
                    elif response.lower().startswith("bot:"):
                        response = response[4:]
                    elif response.lower().startswith("model:"):
                        response = response[6:]
                    elif response.lower().startswith("assistant:"):
                        response = response[10:]

                    context.append({
                        "role": "assistant",
                        "content": f"LunisBot: {sanity_truncate(response)}"
                    })

                    last_activity = time.time()
                    await message.channel.send(sanity_truncate(response))
            except Exception as e:
                print(f"Exception while responding: {e}")

lunisbot.run(DISCORD_API_TOKEN)
