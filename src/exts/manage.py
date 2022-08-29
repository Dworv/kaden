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

from utils import val_tournament_desc, val_tournament_name, add_hours, success_embed, submit_button, info_embed, choose_comp
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
        comp_id = database.create_competition(ctx.guild_id, ctx.author.id, name, description, end)
        await ctx.send(embeds=success_embed(f"Competition `{name}` created! Display a nice message with a submit button using </comp show:69>"), components=submit_button(comp_id))

    @comp.subcommand("end")
    async def comp_end(self, ctx: InteractionContext):
        """Provoke an early end to an existing competition."""
        if not database.get_guild_comps(ctx.guild_id, CompState.SUBMIT):
            await ctx.send(embed=error_embed("There are no active competitions in your server."))
            return
        if (button_ctx := await choose_comp(ctx, "end", CompState.SUBMIT)) is None:
            return
        database.set_comp_state(button_ctx.values[0], CompState.PENDING)
        await button_ctx.edit_origin(embeds=success_embed("Competition successfully terminated. The submissions are awaiting review."), components=[])

    @comp.subcommand("delay")
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
    async def comp_delay(self, ctx: InteractionContext, duration: int):
        """Delay an existing competition."""
    
    @comp.subcommand("cancel")
    async def comp_cancel(self, ctx: InteractionContext):
        """Cancel a competition. CANNOT BE UNDONE!"""
    
    @comp.subcommand("show")
    async def comp_show(self, ctx: InteractionContext):
        """Display a competition accomponied by a submit button."""

def setup(bot: Client):
    Manage(bot)
