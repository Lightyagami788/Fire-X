import requests
from firebot.utils import fire_on_cmd,edit_or_reply


@fire.on(fire_on_cmd(pattern="vaccine"))
async def fire(event):
    "corona vaccine"
    input_text = event.pattern_match.group(1)
    if input_text and " " in input_text:
        pin,date = input_text.split()
    else:
        return await edit_or_reply(event,"Give input values correctly.")
    url = f'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={int(pin)}&date={date}'
    res = requests.get(url)
    a = res.json()
    i = 0
    my_string ="<b>Center No : 1 </b>\n\n"
    if (not 'centers' in a) or (not a['centers']):
        return await edit_delete(event,"Can't find any deatils for this pin code")
    else:
        await edit_or_reply(event,"Processing...")
        for x in a['centers']:
            for items in a['centers'][i]:
                if type(a['centers'][i][items]) is list:
                    j=0
                    for s in a['centers'][i][items]:
                        for subitem in a['centers'][i][items][j]:
                            val = a['centers'][i][items][j][subitem]
                            if "_" in subitem:
                                subitem = subitem.replace("_"," ")
                            my_string += f"<b>   • {subitem.title()}  :</b>  <code>{val}</code>\n"
                        j+=1
                else:
                    value = a['centers'][i][items]
                    if "_" in items:
                        items = items.replace("_"," ")
                    my_string += f"<b>✘ {items.title()}   :</b>  <code>{value}</code>\n"
            i+=1
            if i<len(a['centers']):
                my_string +=f"\n\n<b>Center No : {i+1}</b>\n\n"
   fire = my_string.replace("',","\n       ").replace("['","• ").replace("']","").replace("'","• ")
    await edit_or_reply(event,Fire,parse_mode="html")
