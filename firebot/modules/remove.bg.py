import io
import os
from datetime import datetime

import requests

from firebot import CMD_HELP
from firebot.utils import fire_on_cmd


@fire.on(fire_on_cmd("rmbg ?(.*)"))
async def _(event):
    HELP_STR = (
        "`.rmbg` as reply to a media, or give a link as an argument to this command"
    )
    if event.fwd_from:
        return
    if Config.REM_BG_API_KEY is None:
        await event.edit("You need API token from remove.bg to use this plugin.")
        return False
    input_str = event.pattern_match.group(1)
    start = datetime.now()
    message_id = event.message.id
    if event.reply_to_msg_id:
        message_id = event.reply_to_msg_id
        reply_message = await event.get_reply_message()
        # check if media message
        await event.edit("`Parsing the image.`")
        try:
            downloaded_file_name = await borg.download_media(
                reply_message, Config.TMP_DOWNLOAD_DIRECTORY
            )
        except Exception as e:
            await event.edit(str(e))
            return
        else:
            await event.edit("sending to ReMove.BG")
            output_file_name = ReTrieveFile(downloaded_file_name)
            os.remove(downloaded_file_name)
    elif input_str:
        await event.edit("sending to ReMove.BG")
        output_file_name = ReTrieveURL(input_str)
    else:
        await event.edit(HELP_STR)
        return
    contentType = output_file_name.headers.get("content-type")
    if "image" in contentType:
        with io.BytesIO(output_file_name.content) as remove_bg_image:
            remove_bg_image.name = "BG_less.png"
            await borg.send_file(
                event.chat_id,
                remove_bg_image,
                force_document=True,
                supports_streaming=False,
                allow_cache=False,
                reply_to=message_id,
            )
        end = datetime.now()
        ms = (end - start).seconds
        await event.edit(
            "Removed image's Background in {} seconds, powered by firebot".format(ms)
        )
    else:
        await event.edit(
            "ReMove.BG API returned Errors. Please report to @FIRE_X_CHANNEL\n`{}".format(
                output_file_name.content.decode("UTF-8")
            )
        )


# this method will call the API, and return in the appropriate format
# with the name provided.
def ReTrieveFile(input_file_name):
    headers = {
        "X-API-Key": Config.REM_BG_API_KEY,
    }
    files = {
        "image_file": (input_file_name, open(input_file_name, "rb")),
    }
    r = requests.post(
        "https://api.remove.bg/v1.0/removebg",
        headers=headers,
        files=files,
        allow_redirects=True,
        stream=True,
    )
    return r


def ReTrieveURL(input_url):
    headers = {
        "X-API-Key": Config.REM_BG_API_KEY,
    }
    data = {"image_url": input_url}
    r = requests.post(
        "https://api.remove.bg/v1.0/removebg",
        headers=headers,
        data=data,
        allow_redirects=True,
        stream=True,
    )
    return r


CMD_HELP.update(
    {
        "remove.bg": "**Remove background**\
\n\n**Syntax : **`.rmbg <reply to image>`\
\n**Usage :** Image of replyed image is removed."
    }
)
