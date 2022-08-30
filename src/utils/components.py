from db import database, CompState
from naff import (
    Button,
    ButtonStyles,
    Select,
    SelectOption,
    InteractionContext,
    PartialEmoji,
    ComponentContext,
)

from .embeds import error_embed, info_embed


def submit_button(comp_id: int):
    return Button(ButtonStyles.GREEN, "Make Submission!", "✉", f"submit~{comp_id}")


def comp_select(guild_id: int, state: CompState):
    comps = database.get_guild_comps(guild_id, state)
    options = [
        SelectOption(comp[4], str(comp[0]), comp[5], PartialEmoji(name="➡️"))
        for comp in comps
    ]
    return Select(options, "contest_chooser", "Pick a contest from your guild.")


async def choose_comp(
    ctx: InteractionContext, msg: str, state: CompState
) -> ComponentContext:
    select = comp_select(ctx.guild_id, state)
    origin = await ctx.send(
        embed=info_embed("Choose a contest.", f"Pick a contest to {msg}."),
        components=select,
    )

    def check(component: Select):
        # print("COMMAND INTERACTION ID:", origin.interaction.id)
        # print("COMPONENT INTERACTION ID:", origin.interaction.id)
        return (
            # component.context.message.interaction.id == origin.interaction.id
            ctx.author.id
            == component.context.author.id
        )

    try:
        used = await ctx.bot.wait_for_component(origin, select, check, timeout=30)
    except TimeoutError:
        select.disabled = True
        await used.context.edit_origin(
            embed=error_embed("Timed out. Please try again, and be quicker this time."),
            components=select,
        )
    else:
        return used.context
