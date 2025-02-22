from firebot import CMD_HELP
from firebot.utils import fire_on_cmd
from var import Var


@fire.on(fire_on_cmd(pattern="stat$"))
async def stats(event):
    if event.fwd_from:
        return
    botusername = Var.TG_BOT_USER_NAME_BF_HER
    noob = "stats"
    if event.reply_to_msg_id:
        await event.get_reply_message()
    tap = await bot.inline_query(botusername, noob)
    await tap[0].click(event.chat_id)
    await event.delete()


@fire.on(fire_on_cmd(pattern="xogame$"))
async def gamez(event):
    if event.fwd_from:
        return
    botusername = "@xobot"
    noob = "play"
    if event.reply_to_msg_id:
        await event.get_reply_message()
    tap = await bot.inline_query(botusername, noob)
    await tap[0].click(event.chat_id)
    await event.delete()


@fire.on(fire_on_cmd(pattern="wspr ?(.*)"))
async def wspr(event):
    if event.fwd_from:
        return
    wwwspr = event.pattern_match.group(1)
    botusername = "@whisperBot"
    if event.reply_to_msg_id:
        await event.get_reply_message()
    tap = await bot.inline_query(botusername, wwwspr)
    await tap[0].click(event.chat_id)
    await event.delete()


@fire.on(fire_on_cmd(pattern="mod ?(.*)"))
async def mod(event):
    if event.fwd_from:
        return
    modr = event.pattern_match.group(1)
    botusername = "@PremiumAppBot"
    if event.reply_to_msg_id:
        await event.get_reply_message()
    tap = await bot.inline_query(botusername, modr)
    await tap[0].click(event.chat_id)
    await event.delete()


CMD_HELP.update(
    {
        "inline_fun": "**Inline Fun**\
\n\n**Syntax : **`.stat`\
\n**Usage :** Shows inline stats of your assistant bot.\
\n\n**Syntax : **`.xogame`\
\n**Usage :** starts a multiplayer xo game.\
\n\n**Syntax : **`.wspr <text> <username/ID>`\
\n**Usage :** sends a inline whisper message for given user.\
\n\n**Syntax : **`.mod <app name>`\
\n**Usage :** Provides mod APK for given app."
    }
)
