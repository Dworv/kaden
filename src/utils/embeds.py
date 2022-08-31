from naff import Embed, EmbedFooter, EmbedField, EmbedAuthor, Timestamp

from .config import read_config


def error_embed(msg: str):
    return Embed(
        title="Something went wrong...",
        description=msg,
        color=read_config("colors", "error"),
        timestamp=Timestamp.now(),
    )


def success_embed(msg: str):
    return Embed(
        title="Action Successful!",
        description=msg,
        color=read_config("colors", "success"),
        timestamp=Timestamp.now(),
    )


def info_embed(title: str, msg: str):
    return Embed(
        title=title,
        description=msg,
        color=read_config("colors", "info"),
        timestamp=Timestamp.now(),
    )


def comp_embed(comp):
    return Embed(
        title="Check out this contest!",
        description=f"**{comp[4]}**",
        color=read_config("colors", "success"),
        timestamp=Timestamp.now(),
        fields=[
            EmbedField("Description", comp[5]),
            EmbedField("Began", f"<t:{comp[7]}:R>", True),
            EmbedField("Ends", f"<t:{comp[6]}:R>", True),
            EmbedField("Creator", f"<@{comp[2]}>", True)
        ]
    )
