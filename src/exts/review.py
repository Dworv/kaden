from naff import Client, Extension, InteractionContext, slash_command


class Review(Extension):
    @slash_command("review")
    async def review(selfctx: InteractionContext):
        """Review the submissions of a competition."""


def setup(bot: Client):
    Review(bot)
