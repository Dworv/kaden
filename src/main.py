from naff import Activity, ActivityType, Client, Intents

bot = Client(
    activity=Activity(
        "through submissions.",
        ActivityType.STREAMING,
        "https://github.com/dworv",
    ),
    debug_scope=
)