import json
import logging
import os

from singleton.agent import DiscordAgent
from singleton.ai import AI


logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    handlers=[logging.StreamHandler()]
)


def load_config(filename) -> dict:
    with open(filename, 'r') as f:
        return json.loads(f.read())


if __name__ == '__main__':
    config = load_config('./config.json')
    agent = DiscordAgent(
        os.getenv('DISCORD_TOKEN'),
        AI(os.getenv('OPENAI_TOKEN')),
        config.get('COMMAND_PREFIX', '!'),
        config.get('CHANNEL', 'general'),
        config.get('HISTORY_LIMIT', 30))
    agent.launch()
