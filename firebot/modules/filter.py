"""Filters
Available Commands:
.savefilter
.listfilters
.clearfilter"""
import asyncio
import re

from telethon import utils
from telethon.tl import types

from firebot import CMD_HELP
from firebot.modules.sql_helper.filter_sql import (
    add_filter,
    get_all_filters,
    remove_all_filters,
    remove_filter,
)
from firebot.utils import edit_or_reply, fire_on_cmd, sudo_cmd

DELETE_TIMEOUT = 0
TYPE_TEXT = 0
TYPE_PHOTO = 1
TYPE_DOCUMENT = 2


global last_triggered_filters
last_triggered_filters = {}  # pylint:disable=E0602


@command(incoming=True)
async def on_snip(event):
    global last_triggered_filters
    name = event.raw_text
    if event.chat_id in last_triggered_filters:
        if name in last_triggered_filters[event.chat_id]:
            # avoid firebot spam
            # "I demand rights for us bots, we are equal to you humans." -Henri Koivuneva (t.me/UserbotTesting/2698)
            return False
    snips = get_all_filters(event.chat_id)
    if snips:
        for snip in snips:
            pattern = r"( |^|[^\w])" + re.escape(snip.keyword) + r"( |$|[^\w])"
            if re.search(pattern, name, flags=re.IGNORECASE):
                if snip.snip_type == TYPE_PHOTO:
                    media = types.InputPhoto(
                        int(snip.media_id),
                        int(snip.media_access_hash),
                        snip.media_file_reference,
                    )
                elif snip.snip_type == TYPE_DOCUMENT:
                    media = types.InputDocument(
                        int(snip.media_id),
                        int(snip.media_access_hash),
                        snip.media_file_reference,
                    )
                else:
                    media = None
                event.message.id
                if event.reply_to_msg_id:
                    event.reply_to_msg_id
                await event.reply(snip.reply, file=media)
                if event.chat_id not in last_triggered_filters:
                    last_triggered_filters[event.chat_id] = []
                last_triggered_filters[event.chat_id].append(name)
                await asyncio.sleep(DELETE_TIMEOUT)
                last_triggered_filters[event.chat_id].remove(name)


@fire.on(fire_on_cmd(pattern="filter (.*)"))
@fire.on(sudo_cmd(pattern="filter (.*)", allow_sudo=True))
async def on_snip_save(event):
    hitler = await edit_or_reply(event, "Processing....")
    name = event.pattern_match.group(1)
    msg = await event.get_reply_message()
    if msg:
        snip = {"type": TYPE_TEXT, "text": msg.message or ""}
        if msg.media:
            media = None
            if isinstance(msg.media, types.MessageMediaPhoto):
                media = utils.get_input_photo(msg.media.photo)
                snip["type"] = TYPE_PHOTO
            elif isinstance(msg.media, types.MessageMediaDocument):
                media = utils.get_input_document(msg.media.document)
                snip["type"] = TYPE_DOCUMENT
            if media:
                snip["id"] = media.id
                snip["hash"] = media.access_hash
                snip["fr"] = media.file_reference
        add_filter(
            event.chat_id,
            name,
            snip["text"],
            snip["type"],
            snip.get("id"),
            snip.get("hash"),
            snip.get("fr"),
        )
        await hitler.edit(f"filter {name} saved successfully. Get it with {name}")
    else:
        await hitler.edit(
            "Reply to a message with `savefilter keyword` to save the filter"
        )


@fire.on(fire_on_cmd(pattern="filters$"))
@fire.on(sudo_cmd(pattern="filters$", allow_sudo=True))
async def on_snip_list(event):
    indiaislove = await edit_or_reply(event, "Processing....")
    all_snips = get_all_filters(event.chat_id)
    OUT_STR = "Available Filters in the Current Chat:\n"
    if len(all_snips) > 0:
        for a_snip in all_snips:
            OUT_STR += f"👉 {a_snip.keyword} \n"
    else:
        OUT_STR = "No Filters. Start Saving using `.filter`"
    if len(OUT_STR) > 4096:
        with io.BytesIO(str.encode(OUT_STR)) as out_file:
            out_file.name = "filters.text"
            await bot.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption="Available Filters in the Current Chat",
                reply_to=event,
            )
            await event.delete()
    else:
        await indiaislove.edit(OUT_STR)


@fire.on(fire_on_cmd(pattern="stop (.*)"))
@fire.on(sudo_cmd(pattern="stop (.*)", allow_sudo=True))
async def on_snip_delete(event):
    iloveindia = await edit_or_reply(event, "Processing...")
    name = event.pattern_match.group(1)
    remove_filter(event.chat_id, name)
    await iloveindia.edit(f"filter {name} deleted successfully")


@fire.on(fire_on_cmd(pattern="rmfilters$"))
@fire.on(sudo_cmd(pattern="rmfilters$", allow_sudo=True))
async def on_all_snip_delete(event):
    edit_or_reply(event, "Processing....")
    remove_all_filters(event.chat_id)
    await event.edit(f"filters **in current chat** deleted successfully")


CMD_HELP.update(
    {
        "filters": "**Filters**\
\n\n**Syntax : **`.filter <word to trigger> <reply to triggered message>`\
\n**Usage :** save filters using this plugin.\
\n\n**Syntax : **`.filters`\
\n**Usage :** All the filters of current chat are listed.\
\n\n**Syntax : **`.stop <filter word to stop>`\
\n**Usage :** Deletes given trigger word.\
\n\n**Syntax : **`.rmfilters`\
\n**Usage :** All the filters in a chat are deleted."
    }
)
