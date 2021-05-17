import os
import json
import pyrogram
from pyrogram import filters #pip3 install pyrogram
import config
import glob

#define app

app = pyrogram.Client(
    "upvote_bot",
    bot_token = config.bot_token,
    api_id = 6,
    api_hash = "eb06d4abfb49dc3eeb1aeb98ae0f581e"
)
regex_upvote = r"^((?i)\+|\+\+|\+1|thx|tnx|ty|thank you|thanx|thanks|pro|cool|good|👍|pro af)$"
regex_downvote = r"^(\-|\-\-|\-1|👎)$"

# intro message

@app.on_message(pyrogram.filters.command(["start"]))
async def start(_, message):
    await message.reply_text(
        "Hi, I am an upvote bot, you can upvote or downvote someone's message in your group by using me. Contact @ri5h46h for support"
    )

@app.on_message(pyrogram.filters.command(["help"]))
async def help(_, message):
    await message.reply_text(
        '''+ to upvote a message.
        - to downvote a message :P
        use /karma command to check the points of memeber in this group.'''
    )

@app.on_message(pyrogram.filters.text
& pyrogram.filters.group
& pyrogram.filters.incoming
& pyrogram.filters.reply
& pyrogram.filters.regex(regex_upvote)
& ~pyrogram.filters.via_bot
& ~pyrogram.filters.bot
& ~pyrogram.filters.edited
)

async def upvote(_, message):
    if message.reply_to_message.from_user.id == message.from_user.id:
        return
    chat_id = message.chat.id
    user_id = message.reply_to_message.from_user.id
    user_mention = message.reply_to_message.from_user.mention
    filename = f"{chat_id}.json"

    if not os.path.exists(filename):
        sample_bot = {"1527962675": 1}
        with open(filename, "w") as f:
            f.write(json.dumps(sample_bot))
    with open(filename) as f2:
        members = json.load(f2)
    if not f"{user_id}" in members:
        members[f"{user_id}"] = 1
    else:
        members[f"{user_id}"] += 1
    with open(filename, "w") as f3:
        f3.write(json.dumps(members))
    await message.reply_text(
        f'Incremented points of {user_mention} By 1 \nTotal Points: {members[f"{user_id}"]}'
    )

@app.on_message(pyrogram.filters.text
                & pyrogram.filters.group
                & pyrogram.filters.incoming
                & pyrogram.filters.reply
                & pyrogram.filters.regex(regex_downvote)
                & ~pyrogram.filters.via_bot
                & ~pyrogram.filters.bot
                & ~pyrogram.filters.edited)
async def downvote(_, message):
    if message.reply_to_message.from_user.id == message.from_user.id:
        return
    chat_id = message.chat.id
    user_id = message.reply_to_message.from_user.id
    user_mention = message.reply_to_message.from_user.mention
    filename = f"{chat_id}.json"

    if not os.path.exists(filename):
        sample_bot = {"1527962675": 1}
        with open(filename, "w") as f:
            f.write(json.dumps(sample_bot))
    with open(filename) as f2:
        members = json.load(f2)
    if not f"{user_id}" in members:
        members[f"{user_id}"] = 1
    else:
        members[f"{user_id}"] -= 1
    with open(filename, "w") as f3:
        f3.write(json.dumps(members))
    await message.reply_text(
        f'Decremented Karma Of {user_mention} By 1 \nTotal Points: {members[f"{user_id}"]}'
    )

import operator
@app.on_message(pyrogram.filters.command(["karma"]) & filters.group)
async def karma(_, message):
    chat_id = message.chat.id
    filename = f"{chat_id}.json"
    with open(filename) as f2:
        members = json.load(f2)
    fmembers = dict(sorted(members.items(), key=operator.itemgetter(1),reverse=True))
    if not message.reply_to_message:
        output = ""
        m = 0
        for i in fmembers.keys():
            try:
                output += f"`{(await app.get_chat(i)).username}: {list(fmembers.values())[m]}`\n"
            except:
                pass
            if m == 10:
                break
            m += 1
        await message.reply_text(output)

    else:
        user_id = message.reply_to_message.from_user.id
        await message.reply_text(f'Total Points: {members[f"{user_id}"]}')


@app.on_message(pyrogram.filters.command(["backup"]) & filters.user(config.owner_id))
async def backup(_, message):
    m = await message.reply_text("Sending..")
    files = glob.glob("*n")
    for i in files:
        await app.send_document(config.owner_id, i)
    await m.edit("Backup Sent In Your PM")


app.run()