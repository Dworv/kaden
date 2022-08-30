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
        description=f"**{comp[4]}**\n{'~'*len(comp[4])}\n{comp[5]}",
        color=read_config("colors", "success"),
        timestamp=Timestamp.fromtimestamp(comp[7]),
    )
