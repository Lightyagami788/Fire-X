from faker import Faker as dc

from Fire-X import bot as Fire-X

from ..utils import admin_cmd as wtf


@Fire-X.on(wtf("card"))
async def _firee(fire):
    cyber = dc()
    killer = cyber.name()
    kali = cyber.address()
    chris = cyber.credit_card_full()
    await fire.edit(f"ℕ𝕒𝕞𝕖:-\n`{killer}`\n\n𝔸𝕕𝕕𝕣𝕖𝕤𝕤:-\n`{kali}`\n\nℂ𝕒𝕣𝕕:-\n`{chris}`")
