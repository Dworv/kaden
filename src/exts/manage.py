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

    @comp.subcommand("end")
    async def comp_end(self, ctx: InteractionContext):
        """Provoke an early end to an existing competition."""

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

def setup(bot: Client):
    Manage(bot)
