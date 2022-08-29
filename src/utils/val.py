from naff import InteractionContext

from .embeds import error_embed
from .config import read_config

async def val_tournament_name(ctx: InteractionContext, name: str):
    allowed: list = read_config("allowed_title_chars")
    if any(char not in allowed for char in name.lower()):
        await ctx.send(embeds=error_embed("The name you chose was not valid."), ephemeral=True)
        return False
    return True

async def val_tournament_desc(ctx: InteractionContext, desc: str):
    allowed: list = read_config("allowed_description_chars")
    if any(char not in allowed for char in desc.lower()):
        await ctx.send(embeds=error_embed("The description you chose was not valid."), ephemeral=True)
        return False
    return True