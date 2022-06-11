import os
from utils.models.bot import SuzukaBot

from utils.helpers import TOKEN

if not os.path.exists('./databases'):
    os.mkdir('./databases')

bot = SuzukaBot()


bot.run(TOKEN)
