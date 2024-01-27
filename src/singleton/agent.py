import logging
from typing import List

import discord
from discord.ext import commands


logger = logging.getLogger(__name__)


class DiscordAgent:

    def __init__(self, token, ai, command_prefix='!', channel=None, history_limit=30):
        self.token = token
        self.ai = ai
        self.command_prefix = command_prefix
        self.channel = channel
        self.history_limit = history_limit

        logger.info(f'Initializing Agent')
        self.agent = commands.Bot(command_prefix=command_prefix, intents=self._get_intents())

        async def on_ready():
            """Callback for when the agent is ready."""
            logging.info(f"Logged in as {self.agent.user.name} ({self.agent.user.id})")

        async def on_message(message: discord.Message):
            """Callback for when a message is sent."""
            logging.info(f'received: {message}')
            if self._should_respond(message):
                # history = await self._fetch_channel_history(message.channel)
                # messages = [self._normalize_message(msg) for msg in history]
                # response = await self.ai.handle_message(messages[::-1])
                response = self.ai.handle_message(message.content)
                if response:
                    await message.channel.send(response)

        self.agent.add_listener(on_ready, 'on_ready')
        self.agent.add_listener(on_message, 'on_message')

    @staticmethod
    def _get_intents() -> discord.Intents:
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True
        return intents

    def launch(self):
        self.agent.run(self.token)

    def _should_respond(self, message: discord.Message) -> bool:
        """Check if the bot should respond to a message."""
        # Let's not talk to ourselves.
        if self.agent.user == message.author:
            return False

        # Check if the message is a DM.
        if isinstance(message.channel, discord.DMChannel):
            return True

        # Check if the message is in the bot channel.
        if self.channel and self.channel == message.channel.name:
            return True

        # Check if the message mentions the bot.
        if self.agent.user in message.mentions:
            return True

        return False

    async def _fetch_channel_history(self, channel: discord.TextChannel) -> List[discord.Message]:
        return [message async for message in channel.history(limit=self.history_limit)]

    @staticmethod
    def _normalize_message(message: discord.Message) -> dict:
        """Convert a Discord message to a JSON-serializable format, or return the message if it's already a string."""
        if isinstance(message.channel, discord.DMChannel):
            channel_name = 'Direct Message'
        else:
            channel_name = getattr(message.channel, 'name', 'unknown channel')
        author_name = getattr(message.author, 'name', 'unknown author')
        content = message.content if message.content else 'unknown content'
        return {
            "role": 'assistant' if author_name == 'Singleton' else 'user',
            "content": f'In {channel_name}, {author_name} said: {content}'
        }
