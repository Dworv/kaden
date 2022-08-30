from naff import InteractionContext

from db import database, CompState
from .embeds import error_embed
from .config import read_config


async def val_tournament_name(ctx: InteractionContext, name: str):
    allowed: list = read_config("allowed_title_chars")
    if any(char not in allowed for char in name.lower()):
        await ctx.send(
            embed=error_embed("The name you chose was not valid."), ephemeral=True
        )
        return False
    if name in [
        comp[4]
        for comp in database.get_guild_comps(int(ctx.guild_id), CompState.SUBMIT)
    ]:
        await ctx.send(
            embed=error_embed(
                "There is already an active tournament with this name in your server."
            ),
            ephemeral=True,
        )
    return True


async def val_tournament_desc(ctx: InteractionContext, desc: str):
    allowed: list = read_config("allowed_description_chars")
    if any(char not in allowed for char in desc.lower()):
        await ctx.send(
            embeds=error_embed("The description you chose was not valid."),
            ephemeral=True,
        )
        return False
    return True
