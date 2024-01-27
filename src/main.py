import json
import os

from singleton.agent import DiscordAgent
from singleton.ai import AI


def load_config(filename) -> dict:
    with open(filename, 'r') as f:
        return json.loads(f.read())


if __name__ == '__main__':
    config = load_config('./config.json')
    agent = DiscordAgent(
        os.getenv('DISCORD_TOKEN'),
        AI(),
        config.get('COMMAND_PREFIX', '!'),
        config.get('CHANNEL', 'general'),
        config.get('HISTORY_LIMIT', 30))
    agent.launch()
