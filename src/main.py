from naff import Activity, ActivityType, Client

from utils import read_config

bot = Client(
    activity=Activity(
        "through submissions.",
        ActivityType.STREAMING,
        "https://github.com/dworv",
    ),
    debug_scope=read_config("debug_scope")
)

with open("TOKEN") as f:
    token = f.readlines()[0].strip()

bot.start(token)