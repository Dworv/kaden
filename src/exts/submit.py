from naff import (
    Extension,
    slash_command,
    slash_option,
    InteractionContext,
    OptionTypes,
    listen,
    ComponentContext,
)

from db import database, CompState
from utils import (
    error_embed,
    success_embed,
    autocomplete_contest,
    dead_submit_button,
    info_embed,
)


class Submit(Extension):
    """The extension holding the submit command and the submit button callback."""

    @slash_command("submit")
    @slash_option(
        "contest",
        "Choose a contest to end.",
        OptionTypes.INTEGER,
        required=True,
        autocomplete=True,
    )
    @slash_option(
        "url", "The url to the submission.", OptionTypes.STRING, required=True
    )
    async def submit(self, ctx: InteractionContext, contest: int, url: str):
        """Make a submission to a competition."""
        comps = database.get_guild_comps(ctx.guild_id, CompState.SUBMIT)
        if contest not in [comp[0] for comp in comps]:
            await ctx.send(embed=error_embed("That contest is not availible."))
            return
        database.create_submission(contest, ctx.author.id, url)
        await ctx.send(
            embed=success_embed(
                "Your submission was recieved. It will be reviewed when the contest ends."
            )
        )
    submit.autocomplete("contest")(autocomplete_contest(CompState.SUBMIT))

    @listen("on_component")
    async def submit_button(self, event):
        ctx: ComponentContext = event.context
        if "submit~" not in ctx.custom_id:
            return
        comp_id = int(ctx.custom_id[7:])
        guild_comps = database.get_guild_comps(ctx.guild_id, CompState.SUBMIT)
        guild_comp_ids = [comp[0] for comp in guild_comps]
        if comp_id not in guild_comp_ids:
            await ctx.edit_origin(components=dead_submit_button())
            return
        await ctx.send(
            embed=info_embed(
                "We can't wait to see your submission!",
                "To make a submission, use </submit:123> to choose the contest and enter the url to your entry.",
            ),
            ephemeral=True,
        )


def setup(bot):
    Submit(bot)
