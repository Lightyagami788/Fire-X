import asyncio
import base64
import os
import random
import shutil
import time
from datetime import datetime

from PIL import Image, ImageDraw, ImageFont
from pySmartDL import SmartDL
from telethon.errors import FloodWaitError
from telethon.tl import functions

from firebot import CMD_HELP

from ..utils import admin_cmd, edit_or_reply

AUTONAME = os.environ.get("AUTONAME", None)
DEFAULT_BIO = os.environ.get("DEFAULTBIO", None)
DEFAULTUSERBIO = str(DEFAULT_BIO) if DEFAULT_BIO else " ᗯᗩᏆᎢᏆᑎᏀ ᏞᏆᏦᗴ ᎢᏆᗰᗴ  "
CHANGE_TIME = int(os.environ.get("CHANGE_TIME", 60))
DEFAULTUSER = str(AUTONAME) if AUTONAME else "firebot"

FONT_FILE_TO_USE = "Fonts/vermin_vibes.ttf"
global AUTOPICSTART
global DIGITALPICSTART
global BLOOMSTART
global AUTONAMESTART
global AUTOBIOSTART

BLOOMSTART = False
AUTOPICSTART = False
AUTOBIOSTART = False
AUTONAMESTART = False
DIGITALPICSTART = False


@bot.on(admin_cmd(pattern="autopic ?(.*)"))
async def autopic(event):
    if event.fwd_from:
        return
    global AUTOPICSTART
    downloaded_file_name = "firebot/original_pic.png"
    downloader = SmartDL(
        Var.DOWNLOAD_PFP_URL_CLOCK, downloaded_file_name, progress_bar=False
    )
    downloader.start(blocking=False)
    photo = "firebot/photo_pfp.png"
    while not downloader.isFinished():
        pass
    input_str = event.pattern_match.group(1)
    if input_str:
        try:
            input_str = -int(input_str)
        except ValueError:
            input_str = -60
    else:
        input_str = 0
    if AUTOPICSTART:
        return await edit_or_reply(event, f"`Autopic is already enabled`")
    else:
        AUTOPICSTART = True
    counter = input_str
    await edit_or_reply(event, f"`Autopic has been started by my Master`")
    while AUTOPICSTART:
        shutil.copy(downloaded_file_name, photo)
        im = Image.open(photo)
        file_test = im.rotate(counter, expand=False).save(photo, "PNG")
        current_time = datetime.now().strftime("  Time: %H:%M \n  Date: %d.%m.%y ")
        img = Image.open(photo)
        drawn_text = ImageDraw.Draw(img)
        fnt = ImageFont.truetype(FONT_FILE_TO_USE, 30)
        drawn_text.text((150, 250), current_time, font=fnt, fill=(124, 252, 0))
        img.save(photo)
        file = await event.client.upload_file(photo)
        try:
            await event.client(functions.photos.UploadProfilePhotoRequest(file))
            os.remove(photo)
            counter -= input_str
            await asyncio.sleep(CHANGE_TIME)
        except BaseException:
            return


@bot.on(admin_cmd(pattern="digitalpfp$"))
async def main(event):
    if event.fwd_from:
        return
    global DIGITALPICSTART
    poto = "firebot/poto_pfp.png"
    cat = str(
        base64.b64decode(
            "aHR0cHM6Ly90ZWxlZ3JhLnBoL2ZpbGUvYWVhZWJlMzNiMWYzOTg4YTBiNjkwLmpwZw=="
        )
    )[2:51]
    downloaded_file_name = "firebot/original_pic.png"
    downloader = SmartDL(cat, downloaded_file_name, progress_bar=False)
    downloader.start(blocking=False)
    if DIGITALPICSTART:
        return await edit_or_reply(event, f"`Digitalpfp is already enabled`")
    else:
        DIGITALPICSTART = True
    await edit_or_reply(event, f"`digitalpfp has been started by my Master`")
    while DIGITALPICSTART:
        shutil.copy(downloaded_file_name, poto)
        Image.open(poto)
        current_time = datetime.now().strftime("%H:%M")
        img = Image.open(poto)
        drawn_text = ImageDraw.Draw(img)
        cat = str(base64.b64decode("dXNlcmJvdC9oZWxwZXJzL3N0eWxlcy9kaWdpdGFsLnR0Zg=="))[
            2:36
        ]
        fnt = ImageFont.truetype(FONT_FILE_TO_USE, 200)
        drawn_text.text((350, 100), current_time, font=fnt, fill=(124, 252, 0))
        img.save(poto)
        file = await event.client.upload_file(poto)
        await event.client(
            functions.photos.DeletePhotosRequest(
                await event.client.get_profile_photos("me", limit=1)
            )
        )
        await event.client(functions.photos.UploadProfilePhotoRequest(file))
        os.remove(poto)
        await asyncio.sleep(CHANGE_TIME)


@bot.on(admin_cmd(pattern="bloom$"))
async def autopic(event):
    if event.fwd_from:
        return
    global BLOOMSTART
    downloaded_file_name = "firebot/original_pic.png"
    downloader = SmartDL(
        Config.DOWNLOAD_PFP_URL_CLOCK, downloaded_file_name, progress_bar=True
    )
    downloader.start(blocking=False)
    photo = "firebot/photo_pfp.png"
    while not downloader.isFinished():
        pass
    if BLOOMSTART:
        return await edit_or_reply(event, f"`Bloom is already enabled`")
    else:
        BLOOMSTART = True
    await edit_or_reply(
        event, "`Bloom colour profile pic have been enabled by my master`"
    )
    while BLOOMSTART:
        # RIP Danger zone Here no editing here plox
        R = random.randint(0, 256)
        B = random.randint(0, 256)
        G = random.randint(0, 256)
        FR = 256 - R
        FB = 256 - B
        FG = 256 - G
        shutil.copy(downloaded_file_name, photo)
        image = Image.open(photo)
        image.paste((R, G, B), [0, 0, image.size[0], image.size[1]])
        image.save(photo)
        current_time = datetime.now().strftime("\n Time: %H:%M:%S \n \n Date: %d/%m/%y")
        img = Image.open(photo)
        drawn_text = ImageDraw.Draw(img)
        fnt = ImageFont.truetype(FONT_FILE_TO_USE, 60)
        ofnt = ImageFont.truetype(FONT_FILE_TO_USE, 250)
        drawn_text.text((95, 250), current_time, font=fnt, fill=(FR, FG, FB))
        drawn_text.text((95, 250), "      😈", font=ofnt, fill=(FR, FG, FB))
        img.save(photo)
        file = await event.client.upload_file(photo)
        try:
            await event.client(functions.photos.UploadProfilePhotoRequest(file))
            os.remove(photo)
            await asyncio.sleep(CHANGE_TIME)
        except BaseException:
            return


@bot.on(admin_cmd(pattern="autoname$"))
async def _(event):
    if event.fwd_from:
        return
    global AUTONAMESTART
    if AUTONAMESTART:
        return await edit_or_reply(event, f"`Autoname is already enabled`")
    else:
        AUTONAMESTART = True
    await edit_or_reply(event, "`Auto Name has been started by my Master `")
    while AUTONAMESTART:
        DM = time.strftime("%d-%m-%y")
        HM = time.strftime("%H:%M")
        name = f"⌚️ {HM}||›  {DEFAULTUSER} ‹||📅 {DM}"
        logger.info(name)
        try:
            await event.client(functions.account.UpdateProfileRequest(first_name=name))
        except FloodWaitError as ex:
            logger.warning(str(e))
            await asyncio.sleep(ex.seconds)
        await asyncio.sleep(CHANGE_TIME)


@bot.on(admin_cmd(pattern="autobio$"))
async def _(event):
    global AUTOBIOSTART
    if event.fwd_from:
        return
    if AUTOBIOSTART:
        return await edit_or_reply(event, f"`Autobio is already enabled`")
    else:
        AUTOBIOSTART = True
    await edit_or_reply(event, "`Autobio has been started by my Master`")
    while AUTOBIOSTART:
        DMY = time.strftime("%d.%m.%Y")
        HM = time.strftime("%H:%M:%S")
        bio = f"📅 {DMY} | {DEFAULTUSERBIO} | ⌚️ {HM}"
        logger.info(bio)
        try:
            await event.client(functions.account.UpdateProfileRequest(about=bio))
        except FloodWaitError as ex:
            logger.warning(str(e))
            await asyncio.sleep(ex.seconds)
        await asyncio.sleep(CHANGE_TIME)


@bot.on(admin_cmd(pattern="end (.*)"))
async def _(event):
    if event.fwd_from:
        return
    global AUTOPICSTART
    global DIGITALPICSTART
    global BLOOMSTART
    global AUTONAMESTART
    global AUTOBIOSTART
    input_str = event.pattern_match.group(1)
    if input_str == "autopic":
        if AUTOPICSTART:
            AUTOPICSTART = False
            await edit_or_reply(event, "`Autopic has been stopped now`")
        else:
            await edit_or_reply(event, "`Autopic haven't enabled`")
    elif input_str == "digitalpfp":
        if DIGITALPICSTART:
            DIGITALPICSTART = False
            await edit_or_reply(event, "`Digital profile pic has been stopped now`")
        else:
            await edit_or_reply(event, "`Digital profile pic haven't enabled`")
    elif input_str == "bloom":
        if BLOOMSTART:
            BLOOMSTART = False
            await edit_or_reply(event, "`Bloom has been stopped now`")
        else:
            await edit_or_reply(event, "`Bloom haven't enabled`")
    elif input_str == "autoname":
        if AUTONAMESTART:
            AUTONAMESTART = False
            await edit_or_reply(event, "`Autoname has been stopped now`")
        else:
            await edit_or_reply(event, "`Autoname haven't enabled`")
    elif input_str == "autobio":
        if AUTOBIOSTART:
            AUTOBIOSTART = False
            await edit_or_reply(event, "`Autobio has been stopped now`")
        else:
            await edit_or_reply(event, "`Autobio haven't enabled`")
    else:
        await edit_or_reply(event, "`What should i end ?..`")


CMD_HELP.update(
    {
        "autoprofile": """**Plugin : **`autoprofile`
        
  •  **Syntax : **`.autopic angle`
  •  **Function : **__Rotating image along with the time on it with given angle if no angle is given then doesnt rotate. You need to set __`DOWNLOAD_PFP_URL_CLOCK`__ in heroku__
  
  •  **Syntax : **`.digitalpfp`
  •  **Function : **__Your profile pic changes to digitaltime profile picutre__
  
  •  **Syntax : **`.bloom`
  •  **Function : **__Random colour profile pics will be set along with time on it. You need to set__ `DOWNLOAD_PFP_URL_CLOCK`__ in heroku__
  
  •  **Syntax : **`.autoname`
  •  **Function : **__for time along with name, you must set __`AUTONAME`__ in the heroku vars first for this to work__
  
  •  **Syntax : **`.autobio`
  •  **Function : **__for time along with your bio, Set __`DEFAULT_BIO`__ in the heroku vars first__
  
  •  **Syntax : **`.end function`
  •  **Function : **__To stop the given functions like autopic ,difitalpfp , bloom , autoname and autobio__
  
**⚠️DISCLAIMER⚠️**
__USING THIS PLUGIN CAN RESULT IN ACCOUNT BAN. WE ARE NOT RESPONSIBLE FOR YOUR BAN.__
"""
    }
)
