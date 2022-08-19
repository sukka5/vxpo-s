from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

@Client.on_message(filters.private & filters.command(['start']))
async def start(c:Client, m:Message):
    await m.reply_text(
        text=f"**Hey 👋 {m.from_user.mention} Dear!**\n\n**First you should get an idea about what can this bot upload and what links are supported/how to send links for me by pressing /help**",
        reply_markup=InlineKeyboardMarkup([
          [
            InlineKeyboardButton(text="Settings", callback_data="settings") ,
            InlineKeyboardButton(text="Help", callback_data="help")
          ]
        ]),
        quote=True
    )

