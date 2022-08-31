from naff import Client, Extension, InteractionContext, slash_command, slash_option, OptionTypes

from db import database, CompState
from utils import error_embed


class Review(Extension):
    @slash_command("review")
    @slash_option(
        "contest",
        "Choose a contest to end.",
        OptionTypes.INTEGER,
        required=True,
        autocomplete=True,
    )
    async def review(self, ctx: InteractionContext, contest: int):
        """Review the submissions of a competition."""
        comps = database.get_guild_comps(ctx.guild_id, CompState.SUBMIT)
        if contest not in [comp[0] for comp in comps]:
            await ctx.send(embed=error_embed("That contest is not availible."))
            return
            

def setup(bot: Client):
    Review(bot)
