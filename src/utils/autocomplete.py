from naff import AutocompleteContext

from db import database, CompState


def autocomplete_contest(state: CompState):
    async def inner(_, ctx: AutocompleteContext, **__):
        comp_names = [
            {"name": comp[4], "value": comp[0]}
            for comp in database.get_guild_comps(ctx.guild_id, state)
        ]
        print(comp_names)
        await ctx.send(comp_names)

    return inner
