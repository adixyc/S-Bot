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

api_id = 36887754
api_hash = '78df646056bc13ed72332a80271cbf41'

session = "1AZWarzcBu7Daf2vAbR-vQKs9b25kRlY4_MN7azW480U0-OJ0HKoWnckXpCuSy0TiyLrWLdgzSh2K3svTlu8WonzVrA9Y5qXFacpBojvfMWnMLK9OeAql8yS9e4yZeh78o6VG9zR9HcggCLBhbV4oiIVYM9T8wthpVstlN7BeVZX9wF5IFE_iTTB0FSYNEmC8cRQJc8zW_SApAzkVovJLXO59vESO54GD_E75Rwhg7RnPIr-mKDYqrrsX8rASNWvxdyvDM-LMZGm7HRM6akfJBJUUk9hoPMWaeaz9TYIvQ6wOQt1Z9aDhHddvpN8Tn1hoD-rjs_JdsQLZDy4FgmdbX80uUfo0fWk="

client = TelegramClient(StringSession(session), api_id, api_hash)

TARGET_GROUP_ID = -1003623091628
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
            Hey dear thank you for messaging me. 🥰
            
            Join this awesome group @SWAPPINGE_WIFE 
            
            After joining message me again. ❤️
            '''
            )

# ---------------- KEYWORD REPLY ---------------- #
@client.on(events.NewMessage(chats=TARGET_GROUP_ID))
async def delete_users_with_links(event):

    try:
        sender = await event.get_sender()

        if sender.bot or sender.is_self:
            return

        perms = await client.get_permissions(
            TARGET_GROUP_ID,
            sender.id
        )

        # Skip admins and owner
        if perms.is_admin:
            return

        if await has_link_in_bio(sender.id):
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
