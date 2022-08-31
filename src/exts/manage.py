import time

from naff import (
    Extension,
    Client,
    InteractionContext,
    OptionTypes,
    SlashCommandChoice,
    Permissions,
    slash_command,
    slash_option,
)

from utils import (
    val_tournament_desc,
    val_tournament_name,
    add_hours,
    success_embed,
    submit_button,
    info_embed,
    choose_comp,
    autocomplete_contest,
    comp_embed,
)
from db import database, CompState
from utils.embeds import error_embed


class Manage(Extension):
    @slash_command("comp", default_member_permissions=Permissions.ADMINISTRATOR)
    async def comp(self, _):
        """Manage competitions."""

    @comp.subcommand("new")
    @slash_option(
        "name",
        "The name of the competition.",
        OptionTypes.STRING,
        required=True,
        max_length=16,
    )
    @slash_option(
        "description",
        "The description of the competition.",
        OptionTypes.STRING,
        required=True,
        max_length=100,
    )
    @slash_option(
        "length",
        "How long the tournament should stay open.",
        OptionTypes.INTEGER,
        required=True,
        choices=[
            SlashCommandChoice("1 Hour", 1),
            SlashCommandChoice("2 Hours", 2),
            SlashCommandChoice("3 Hours", 3),
            SlashCommandChoice("6 Hours", 6),
            SlashCommandChoice("12 Hours", 12),
            SlashCommandChoice("24 Hours", 24),
            SlashCommandChoice("2 Days", 2 * 24),
            SlashCommandChoice("3 Days", 3 * 24),
            SlashCommandChoice("4 Days", 4 * 24),
            SlashCommandChoice("5 Days", 5 * 24),
            SlashCommandChoice("6 Days", 6 * 24),
            SlashCommandChoice("7 Days", 7 * 24),
            SlashCommandChoice("2 Weeks", 2 * 7 * 24),
            SlashCommandChoice("3 Weeks", 3 * 7 * 24),
            SlashCommandChoice("4 Weeks", 4 * 7 * 24),
        ],
    )
    async def comp_new(
        self, ctx: InteractionContext, name: str, description: str, length: int
    ):
        """Create a new competition."""
        if not await val_tournament_name(ctx, name):
            return
        if not await val_tournament_desc(ctx, description):
            return
        end = add_hours(length)
        database.create_competition(ctx.guild_id, ctx.author.id, name, description, end)
        await ctx.send(
            embeds=success_embed(
                f"Competition `{name}` created! Display a nice message with a submit button using </comp show:69>"
            )
        )

    @comp.subcommand("end")
    @slash_option(
        "contest",
        "Choose a contest to end.",
        OptionTypes.INTEGER,
        required=True,
        autocomplete=True,
    )
    async def comp_end(self, ctx: InteractionContext, contest: int):
        """Provoke an early end to a competition review the submissions."""
        if contest not in [
            comp[0] for comp in database.get_guild_comps(ctx.guild_id, CompState.SUBMIT)
        ]:
            await ctx.send(embed=error_embed("That contest is not availible."))
            return
        database.set_comp_state(contest, CompState.PENDING)
        await ctx.send(
            embeds=success_embed(
                "Competition successfully ended early. The submissions are now awaiting review."
            )
        )

    comp_end.autocomplete("contest")(autocomplete_contest(CompState.SUBMIT))

    @comp.subcommand("extend")
    @slash_option(
        "contest",
        "Choose a contest to extend.",
        OptionTypes.INTEGER,
        required=True,
        autocomplete=True,
    )
    @slash_option(
        "duration",
        "How long the tournament should stay open.",
        OptionTypes.INTEGER,
        required=True,
        choices=[
            SlashCommandChoice("1 Hour", 1),
            SlashCommandChoice("2 Hours", 2),
            SlashCommandChoice("3 Hours", 3),
            SlashCommandChoice("6 Hours", 6),
            SlashCommandChoice("12 Hours", 12),
            SlashCommandChoice("24 Hours", 24),
            SlashCommandChoice("2 Days", 2 * 24),
            SlashCommandChoice("3 Days", 3 * 24),
            SlashCommandChoice("4 Days", 4 * 24),
            SlashCommandChoice("5 Days", 5 * 24),
            SlashCommandChoice("6 Days", 6 * 24),
            SlashCommandChoice("7 Days", 7 * 24),
            SlashCommandChoice("2 Weeks", 2 * 7 * 24),
            SlashCommandChoice("3 Weeks", 3 * 7 * 24),
            SlashCommandChoice("4 Weeks", 4 * 7 * 24),
        ],
    )
    async def comp_extend(self, ctx: InteractionContext, contest: int, duration: int):
        """Delay an existing competition. Max contest length is 4 weeks."""
        if contest not in [
            comp[0] for comp in database.get_guild_comps(ctx.guild_id, CompState.SUBMIT)
        ]:
            await ctx.send(embed=error_embed("That contest is not availible."))
            return
        current_end: int = database.get_comp(contest)[6]
        new_end = min(
            current_end + duration * 60 * 60, round(time.time()) + 60 * 60 * 24 * 7 * 4
        )  # cap the end time to 4 weeks in future
        extension = new_end - current_end
        database.extend_comp_end(contest, extension)
        await ctx.send(
            embeds=success_embed(
                f"The competition has been extended until <t:{new_end}:F>"
            )
        )

    comp_extend.autocomplete("contest")(autocomplete_contest(CompState.SUBMIT))

    @comp.subcommand("cancel")
    @slash_option(
        "contest",
        "Choose a contest to cancel.",
        OptionTypes.INTEGER,
        required=True,
        autocomplete=True,
    )
    async def comp_cancel(self, ctx: InteractionContext, contest: int):
        """Cancel a competition. FORGETS ALL SUBMISSIONS CANNOT BE UNDONE!"""
        if contest not in [
            comp[0] for comp in database.get_guild_comps(ctx.guild_id, CompState.SUBMIT)
        ]:
            await ctx.send(embed=error_embed("That contest is not availible."))
            return
        database.set_comp_state(contest, CompState.OVER)
        await ctx.send(
            embeds=success_embed("Competition successfully removed."), components=[]
        )

    comp_cancel.autocomplete("contest")(autocomplete_contest(CompState.SUBMIT))

    @comp.subcommand("show")
    @slash_option(
        "contest",
        "Choose a contest to display.",
        OptionTypes.INTEGER,
        required=True,
        autocomplete=True,
    )
    async def comp_show(self, ctx: InteractionContext, contest: int):
        """Display a competition accomponied by a submit button."""
        comps = database.get_guild_comps(ctx.guild_id, CompState.SUBMIT)
        if contest not in [comp[0] for comp in comps]:
            await ctx.send(embed=error_embed("That contest is not availible."))
            return
        comp = [comp for comp in comps if comp[0] == contest][0]
        await ctx.send(embed=comp_embed(comp), components=submit_button(contest))

    comp_show.autocomplete("contest")(autocomplete_contest(CompState.SUBMIT))


def setup(bot: Client):
    Manage(bot)
