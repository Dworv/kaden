#!/usr/local/bin/python3.10
import os

from naff import Activity, ActivityType, Client

from utils import read_config

bot = Client(
    activity=Activity(
        "your submissions.",
        ActivityType.WATCHING,
        "https://github.com/dworv",
    ),
    debug_scope=read_config("debug_scope"),
)

for root, _, files in os.walk("exts"):
    for file in files:
        if file.endswith(".py") and not file.startswith("__init__"):
            file = file.removesuffix(".py")
            path = os.path.join(root, file)
            python_import_path = path.replace("/", ".").replace("\\", ".")

            # load the extension
            bot.load_extension(python_import_path)

with open("TOKEN") as f:
    token = f.readlines()[0].strip()

bot.start(token)
