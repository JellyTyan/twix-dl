import random
from .user_agent import USER_AGENTS

def get_random_user_agent():
    return random.choice(USER_AGENTS)