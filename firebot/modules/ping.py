import time

from firebot import ALIVE_NAME, CMD_HELP
from firebot.utils import admin_cmd, sudo_cmd

DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else "firebot"


@borg.on(admin_cmd(pattern="ping$"))
@borg.on(sudo_cmd(pattern="ping$", allow_sudo=True))
async def _(event):
    text = f"""
┏━━━┓━━━━━━━━━┓
┃┏━┓┃━━━━━━━━━┃
┃┗━┛┃━━┓━┓━━━┓┃
┃┏━━┛┏┓┃┏┓┓┏┓┃┛
┃┃━━━┗┛┃┃┃┃┗┛┃┓
┗┛━━━━━┛┛┗┛━┓┃┛
━━━━━━━━━━━━┛┃━
━━━━━━━━━━━━━┛━
__FIRE-X__ is **ON!**ツ
•My Master→ {DEFAULTUSER}
↓||•Ms•||↓
"""
    st = time.time()

    await event.edit(text)

    et = time.time()
    text += f"\n`{round((et - st), 3)} ms`"

    await event.edit(text)


CMD_HELP.update(
    {
        "ping": "**Ping**\
\n\n**Syntax : **`.ping`\
\n**Usage :** Get speed of your bot."
    }
)
