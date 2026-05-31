import os
import re
import asyncio
import random
import time
from datetime import datetime
from threading import Thread
from flask import Flask

from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.functions.contacts import BlockRequest, UnblockRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName

# ---------------- WEB SERVER ---------------- #

app = Flask(__name__)

@app.route('/')
def home():
    return "ADUBOT IS ONLINE!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    Thread(target=run_web).start()

# ---------------- TELEGRAM CONFIG ---------------- #

api_id = 37855367
api_hash = '9e7b3f8d5b66f1443f156678938e6b83'

session = "1AZWarzYBuyjKziCcu4hH9mXg1UGEuGzSr1w-KPb0Rnv53cvlSX-jEqm4x0RbK2xPt6a01VHkLGGi2ig7T0BrFEaAvc8W9vX4Z2N37Nfyzilf_EyNdpUTJC8pnWxVRMz7lNfJ5fZfc5BiT3h6PYWz847y5EXF2pkZvDw8znjWX2TF69R1YsAzRA0gbGmn-2ySYH2xt5Mgfkn0RM7WqkP-76_EhPUvtk_qDU8ML0IgmHNSrO_ZKCKpwIa72FVw3FRVmj9htOCJScPf9J_H3_mbi1C1te1j2tSD1KXbJX3EAVwAgA_pIlB79WgmKW078aItSHBf0a-DlZiJ1Gz0kWDlGWC7fBwTMkk="

client = TelegramClient(StringSession(session), api_id, api_hash)

TARGET_GROUP_ID = -1003624979028
GROUP_LINK = "@SWAPPINGe_WIFE"

replied_users = set()
start_time = time.time()

quotes = [
    "HeIIo",
    "Hey Boys",
    "Adds Me",
    "HeIIo Boys",
    "I'm OnIine",
    "F17 from DeIhi",
    "Try not to c*m chaIIenge"
]

# ---------------- BIO CHECK ---------------- #

ALLOWED_USERNAMES = [
    "@SWAPPINGe_WIFE",
    "@STAR_NAVYA",
    "@niximia"
]

async def has_link_in_bio(user_id):
    try:
        full = await client(GetFullUserRequest(user_id))
        bio = full.full_user.about or ""

        # remove allowed usernames
        for allowed in ALLOWED_USERNAMES:
            bio = bio.replace(allowed, "")

        patterns = [
            r"@\w+",
            r"t\.me/\w+",
            r"http[s]?://",
            r"www\."
        ]

        for pattern in patterns:
            if re.search(pattern, bio, re.IGNORECASE):
                return True

        return False

    except Exception as e:
        print("Bio check error:", e)
        return False

# ---------------- BACKGROUND TASKS ---------------- #

async def fake_typing():
    while True:
        try:
            async with client.action(TARGET_GROUP_ID, 'typing'):
                await asyncio.sleep(random.randint(6, 12))
        except Exception as e:
            print("Typing Error:", e)
            await asyncio.sleep(15)

async def send_quotes():
    while True:
        dialogs = await client.get_dialogs()

        for dialog in dialogs:
            if dialog.is_group:
                try:
                    await client.send_message(
                        dialog.id,
                        random.choice(quotes)
                    )

                    await asyncio.sleep(40)

                except Exception:
                    pass

        await asyncio.sleep(330)

# ---------------- PRIVATE AUTO REPLY ---------------- #

@client.on(events.NewMessage(incoming=True))
async def private_auto_reply(event):

    if event.is_private and not event.out:

        user_id = event.sender_id

        if user_id not in replied_users:

            replied_users.add(user_id)

            await asyncio.sleep(2)

            await event.respond('''
            𝗦𝘂𝘀𝗶❤️🎀

𝗔𝗴𝗲- 2𝟭years, 𝗦𝗶𝘇𝗲𝘀- 34/30/34

𝗦𝗘𝗫 𝗖𝗛𝗔𝗧 👅

✨𝟱𝗺𝗶𝗻𝘀- 200rs
✨𝟭𝟬𝗺𝗶𝗻𝘀- 300rs

𝗩𝗜𝗗𝗘𝗢 𝗖𝗔𝗟𝗟 📲

✨𝟱𝗺𝗶𝗻𝘀- 400rs
✨𝟭𝟬𝗺𝗶𝗻𝘀- 700rs

𝗩𝗢𝗜𝗖𝗘 𝗖𝗔𝗟𝗟 ☎️

✨𝟱𝗺𝗶𝗻𝘀- 200rs
✨𝟭𝟬𝗺𝗶𝗻𝘀- 400rs


𝗦𝗽𝗲𝗰𝗶𝗮𝗹 𝗦𝗵𝗼𝘄𝘀- 

✨𝘋𝘪𝘭𝘥𝘰 𝘴𝘩𝘰𝘸, 𝘢𝘯𝘢𝘭 𝘱𝘭𝘶𝘨 𝘴𝘩𝘰𝘸, 𝘣𝘢𝘵𝘩 𝘴𝘩𝘰𝘸, 𝘤𝘩𝘰𝘤𝘰𝘭𝘢𝘵𝘦 𝘴𝘩𝘰𝘸, 𝘣𝘪𝘬𝘪𝘯𝘪 𝘴𝘩𝘰𝘸, 𝘥𝘢𝘯𝘤𝘦 𝘴𝘩𝘰𝘸, 𝘴𝘢𝘳𝘦𝘦 𝘴𝘩𝘰𝘸, 𝘳𝘰𝘭𝘦𝘱𝘭𝘢𝘺 𝘢𝘯𝘥 𝘮𝘰𝘳𝘦

𝗗𝗺 𝗠𝗲 𝗕𝗮𝗯𝗶𝗲𝘀 ❤️🫂

𝗗𝗲𝗺𝗼 𝗩𝗖- 100rs 💋

𝗧𝗶𝗺𝗲𝗽𝗮𝘀𝘀 🔁 𝗗𝗜𝗥𝗘𝗖𝗧 𝗕𝗟𝗢𝗖𝗞!
𝗡𝗢 𝗥𝗘𝗘𝗧 𝗠𝗘𝗘𝗧!
𝗢𝗡𝗟𝗬 𝗢𝗡𝗟𝗜𝗡𝗘 𝗣𝗔𝗜𝗗 𝗦𝗘𝗥𝗩𝗜𝗖𝗘𝗦!

            '''
            )

# ---------------- KEYWORD REPLY ---------------- #

@client.on(events.NewMessage(incoming=True, pattern=r'(?i)^demo$'))
async def demo_reply(event):

    if event.is_private:
        await event.reply("demo paid hai babe.. 100rs only")

# ---------------- GROUP WELCOME ---------------- #

@client.on(events.ChatAction(chats=TARGET_GROUP_ID))
async def welcome_new_user(event):

    if event.user_joined or event.user_added:

        users = await event.get_users()

        for user in users:

            name = user.first_name or "User"

            message = f"Hello {name}, DM ME FOR FUN BABY 💋"

            entity = MessageEntityMentionName(
                offset=6,
                length=len(name),
                user_id=user.id
            )

            await client.send_message(
                TARGET_GROUP_ID,
                message,
                formatting_entities=[entity]
            )

# ---------------- DELETE USERS WITH LINKS IN BIO ---------------- #

@client.on(events.NewMessage(chats=TARGET_GROUP_ID))
async def delete_users_with_links(event):

    try:
        sender = await event.get_sender()

        # ignore bots and yourself
        if sender.bot or sender.is_self:
            return

        bad_bio = await has_link_in_bio(sender.id)

        if bad_bio:

            await event.delete()

            print(f"Deleted message from {sender.id}")

    except Exception as e:
        print("Delete Error:", e)

# ---------------- COMMANDS ---------------- #

@client.on(events.NewMessage(outgoing=True, pattern=r"\.ping"))
async def ping(event):

    start = time.time()

    msg = await event.edit("Pinging...")

    end = time.time()

    await msg.edit(f"PONG! {round((end-start)*1000)} ms")

@client.on(events.NewMessage(outgoing=True, pattern=r"\.id"))
async def get_id(event):

    await event.edit(f"CHAT ID: `{event.chat_id}`")

@client.on(events.NewMessage(outgoing=True, pattern=r"\.time"))
async def time_cmd(event):

    now = datetime.now().strftime("%H:%M:%S")

    await event.edit(f"CURRENT TIME: {now}")

@client.on(events.NewMessage(outgoing=True, pattern=r"\.alive"))
async def alive(event):

    uptime = int(time.time() - start_time)

    await event.edit(f"⚡ Alive\nUptime: {uptime} sec")

@client.on(events.NewMessage(outgoing=True, pattern=r"\.block"))
async def block_user(event):

    if event.is_private:

        await client(BlockRequest(event.chat_id))

        await event.edit("Blocked.")

@client.on(events.NewMessage(outgoing=True, pattern=r"\.unblock"))
async def unblock_user(event):

    if event.is_private:

        await client(UnblockRequest(event.chat_id))

        await event.edit("Unblocked.")

@client.on(events.NewMessage(outgoing=True, pattern=r"\.spam"))
async def spam(event):

    args = event.raw_text.split(maxsplit=2)

    if len(args) < 3:
        return await event.edit("Usage: .spam count text")

    count = int(args[1])
    text = args[2]

    await event.delete()

    for _ in range(count):
        await client.send_message(event.chat_id, text)

@client.on(events.NewMessage(outgoing=True, pattern=r"\.dm"))
async def price_list(event):

    text = """
🌸 VC SERVICE - @STAR_NAVYA
🌸 TG/WA ID - @niximia
"""

    await event.edit(text)

# ---------------- AUTO DELETE ALL GROUP MSGS ---------------- #

@client.on(events.NewMessage(chats=TARGET_GROUP_ID))
async def auto_delete_group_messages(event):

    try:
        await asyncio.sleep(60)

        await event.delete()

    except Exception as e:
        print("Auto-delete error:", e)

# ---------------- MAIN ---------------- #

async def main():

    await client.start()

    print("Userbot running...")

    asyncio.create_task(fake_typing())
    asyncio.create_task(send_quotes())

    await client.run_until_disconnected()

keep_alive()
asyncio.run(main())
