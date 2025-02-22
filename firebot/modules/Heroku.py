# Copyright (C) 2020 Adek Maulana.
# All rights reserved.
"""
   Heroku manager for your firebot
"""

import asyncio
import math
import os

import heroku3
import requests
from telegraph import Telegraph

from firebot import CMD_HELP
from firebot.utils import edit_or_reply, fire_on_cmd, sudo_cmd

telegraph = Telegraph()
tgnoob = telegraph.create_account(short_name="Fire 🇮🇳")

Heroku = heroku3.from_key(Var.HEROKU_API_KEY)
heroku_api = "https://api.heroku.com"


@fire.on(
    fire_on_cmd(pattern="(set|get|del) var(?: |$)(.*)(?: |$)([\s\S]*)", outgoing=True)
)
@fire.on(
    sudo_cmd(pattern="(set|get|del) var(?: |$)(.*)(?: |$)([\s\S]*)", allow_sudo=True)
)
async def variable(var):
    """
    Manage most of ConfigVars setting, set new var, get current var,
    or delete var...
    """
    if Var.HEROKU_APP_NAME is not None:
        app = Heroku.app(Var.HEROKU_APP_NAME)
    else:
        return await edit_or_reply(
            var, "`[HEROKU]:" "\nPlease setup your` **HEROKU_APP_NAME**"
        )
    exe = var.pattern_match.group(1)
    heroku_var = app.config()
    if exe == "get":
        await edit_or_reply(var, "`Getting information...`")
        await asyncio.sleep(1.5)
        try:
            variable = var.pattern_match.group(2).split()[0]
            if variable in heroku_var:
                return await edit_or_reply(
                    var,
                    "**ConfigVars**:" f"\n\n`{variable} = {heroku_var[variable]}`\n",
                )
            else:
                return await edit_or_reply(
                    var, "**ConfigVars**:" f"\n\n`Error:\n-> {variable} don't exists`"
                )
        except IndexError:
            configs = prettyjson(heroku_var.to_dict(), indent=2)
            with open("configs.json", "w") as fp:
                fp.write(configs)
            with open("configs.json", "r") as fp:
                result = fp.read()
                if len(result) >= 4096:
                    await var.client.send_file(
                        var.chat_id,
                        "configs.json",
                        reply_to=var.id,
                        caption="`Output too large, sending it as a file`",
                    )
                else:
                    await edit_or_reply(
                        var,
                        "`[HEROKU]` ConfigVars:\n\n"
                        "================================"
                        f"\n```{result}```\n"
                        "================================",
                    )
            os.remove("configs.json")
            return
    elif exe == "set":
        await edit_or_reply(var, "`Setting information...`")
        variable = var.pattern_match.group(2)
        if not variable:
            return await edit_or_reply(var, ">`.set var <ConfigVars-name> <value>`")
        value = var.pattern_match.group(3)
        if not value:
            variable = variable.split()[0]
            try:
                value = var.pattern_match.group(2).split()[1]
            except IndexError:
                return await edit_or_reply(var, ">`.set var <ConfigVars-name> <value>`")
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await edit_or_reply(
                var, f"**{variable}**  `successfully changed to`  ->  **{value}**"
            )
        else:
            await edit_or_reply(
                var, f"**{variable}**  `successfully added with value`  ->  **{value}**"
            )
        heroku_var[variable] = value
    elif exe == "del":
        await edit_or_reply(var, "`Getting information to deleting variable...`")
        try:
            variable = var.pattern_match.group(2).split()[0]
        except IndexError:
            return await edit_or_reply(
                var, "`Please specify ConfigVars you want to delete`"
            )
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await edit_or_reply(var, f"**{variable}**  `successfully deleted`")
            del heroku_var[variable]
        else:
            return await edit_or_reply(var, f"**{variable}**  `is not exists`")


@fire.on(fire_on_cmd(pattern="usage$", outgoing=True))
@fire.on(sudo_cmd(pattern="usage$", allow_sudo=True))
async def dyno_usage(dyno):
    """
    Get your account Dyno Usage
    """
    await edit_or_reply(dyno, "`Trying To Fetch Dyno Usage....`")
    useragent = (
        "Mozilla/5.0 (Linux; Android 10; SM-G975F) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/80.0.3987.149 Mobile Safari/537.36"
    )
    user_id = Heroku.account().id
    headers = {
        "User-Agent": useragent,
        "Authorization": f"Bearer {Var.HEROKU_API_KEY}",
        "Accept": "application/vnd.heroku+json; version=3.account-quotas",
    }
    path = "/accounts/" + user_id + "/actions/get-quota"
    r = requests.get(heroku_api + path, headers=headers)
    if r.status_code != 200:
        return await edit_or_reply(
            dyno, "`Error: something bad happened`\n\n" f">.`{r.reason}`\n"
        )
    result = r.json()
    quota = result["account_quota"]
    quota_used = result["quota_used"]

    """ - Used - """
    remaining_quota = quota - quota_used
    percentage = math.floor(remaining_quota / quota * 100)
    minutes_remaining = remaining_quota / 60
    hours = math.floor(minutes_remaining / 60)
    minutes = math.floor(minutes_remaining % 60)

    """ - Current - """
    App = result["apps"]
    try:
        App[0]["quota_used"]
    except IndexError:
        AppQuotaUsed = 0
        AppPercentage = 0
    else:
        AppQuotaUsed = App[0]["quota_used"] / 60
        AppPercentage = math.floor(App[0]["quota_used"] * 100 / quota)
    AppHours = math.floor(AppQuotaUsed / 60)
    AppMinutes = math.floor(AppQuotaUsed % 60)

    await asyncio.sleep(1.5)

    return await edit_or_reply(
        dyno,
        "**Dyno Usage Data**:\n\n"
        f"✗ **APP NAME =>** `{Var.HEROKU_APP_NAME}` \n"
        f"✗ **Usage in Hours And Minutes =>** `{AppHours}h`  `{AppMinutes}m`"
        f"✗ **Usage Percentage =>** [`{AppPercentage} %`]\n"
        "\n\n"
        "✗ **Dyno Remaining This Months 📆:**\n"
        f"✗ `{hours}`**h**  `{minutes}`**m** \n"
        f"✗ **Percentage :-** [`{percentage}`**%**]",
    )


@command(pattern="^.info heroku")
async def info(event):
    await borg.send_message(
        event.chat_id,
        "**Info for Module to Manage Heroku:**\n\n`.usage`\nUsage:__Check your heroku dyno hours status.__\n\n`.set var <NEW VAR> <VALUE>`\nUsage: __add new variable or update existing value variable__\n**!!! WARNING !!!, after setting a variable the bot will restart.**\n\n`.get var or .get var <VAR>`\nUsage: __get your existing varibles, use it only on your private group!__\n**This returns all of your private information, please be cautious...**\n\n`.del var <VAR>`\nUsage: __delete existing variable__\n**!!! WARNING !!!, after deleting variable the bot will restarted**",
    )
    await event.delete()


def prettyjson(obj, indent=2, maxlinelength=80):
    """Renders JSON content with indentation and line splits/concatenations to fit maxlinelength.
    Only dicts, lists and basic types are supported"""

    items, _ = getsubitems(
        obj,
        itemkey="",
        islast=True,
        maxlinelength=maxlinelength - indent,
        indent=indent,
    )
    return indentitems(items, indent, level=0)


@fire.on(fire_on_cmd(pattern="logs$", outgoing=True))
@fire.on(sudo_cmd(pattern="logs$", allow_sudo=True))
async def _(givelogs):
    try:
        Heroku = heroku3.from_key(Var.HEROKU_API_KEY)
        app = Heroku.app(Var.HEROKU_APP_NAME)
    except:
        return await givelogs.reply(
            " Please make sure your Heroku API Key, Your App name are configured correctly in the heroku var !"
        )
    await edit_or_reply(givelogs, "`Trying To Fetch Logs...`")
    with open("logs.txt", "w") as log:
        log.write(app.get_log())
    hmm = app.get_log()
    starky = f"<code> {hmm} </code>"
    title_of_page = "firebot UserBot Logs"
    response = telegraph.create_page(title_of_page, html_content=starky)
    km = response["path"]
    suger = f"`Logs Can Be Found` [Here](https://telegra.ph/{km})"
    await givelogs.client.send_file(
        givelogs.chat_id,
        "logs.txt",
        reply_to=givelogs.id,
        caption=suger,
    )


CMD_HELP.update(
    {
        "heroku": "**Heroku**\
\n\n**Syntax : **`.set var <var key> <var value>`\
\n**Usage :** Add new variable or update existing value variable.\
\n\n**Syntax : **`.get var <var>`\
\n**Usage :** Get your existing variables, use it only on your private group!\
\n\n**Syntax : **`.del var <var>`\
\n**Usage :** Deletes existing variable.\
\n\n**Syntax : **`.usage`\
\n**Usage :** Gives you information about Dyno usage.\
\n\n**Syntax : **`.info heroku`\
\n**Usage :** Gives you information to use other commands of heroku.\
\n\n**Syntax : **`.logs`\
\n**Usage :** Gets logs from heroku."
    }
)
