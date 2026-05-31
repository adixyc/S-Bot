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
from telethon.tl.types import (
    ChannelParticipantAdmin,
    ChannelParticipantCreator
)
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
    "HeIIo ji"
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
            𝗦
            '''
            )

# ---------------- KEYWORD REPLY ---------------- #



# ---------------- GROUP WELCOME ---------------- #
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

@client.on(events.NewMessage(outgoing=True, pattern=r"\.hi"))
async def alive(event):

    uptime = int(time.time() - start_time)

    await event.edit(f"Online")

@client.on(events.NewMessage(outgoing=True, pattern=r"\.rl"))
async def rate_list(event):

    rates = """
📋 RATE LIST

🇮🇳 India: ₹10
🇺🇸 USA: ₹20
🇬🇧 UK: ₹25

💳 Payment: UPI Only
⚡ Instant Delivery
"""

    await event.edit(rates)
    
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

    print("ALL SET")

    asyncio.create_task(fake_typing())
    asyncio.create_task(send_quotes())

    await client.run_until_disconnected()

keep_alive()
asyncio.run(main())
