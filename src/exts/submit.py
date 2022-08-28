from naff import Extension, slash_command, slash_option, InteractionContext, OptionTypes


class Submit(Extension):
    """The extension holding the submit command and the submit button callback."""

    @slash_command("submit")
    @slash_option(
        "url",
        "The url to the submission.",
        OptionTypes.STRING,
        required=True
    )
    async def submit(self, ctx: InteractionContext):
        """Make a submission to a competition."""


def setup(bot):
    Submit(bot)
