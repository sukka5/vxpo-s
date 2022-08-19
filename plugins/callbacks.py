import os
from plugins.progress import progress_for_pyrogram, humanbytes

from Translation import Translation
from pyrogram import Client, types
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

from plugins.downloader import youtube_dl_call_back

@Client.on_callback_query()
async def call_backs(bot:Client, update:CallbackQuery):
    if update.data == "help":
        await update.message.edit(
            text=f"**Hi I am a Private Video Downloader Bot**\nHow to use me ➠ Just send me a m3u8 link! Don't spam me!!\n\n__After you send the link once until it gets uploaded do not send the same link or other links again please! If you do your downloading will be corrupted!__\n\n**Made with 💖 by @ProtgrFckr**",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(text="Settings", callback_data="settings"),
                    InlineKeyboardButton(text="Close", callback_data="close")
                ]
            ])
        )
    elif update.data == "settings":
        await update.message.edit(
            text="**Settings**\n\nComming soon..",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(text="Close", callback_data="close")
                ]
            ])
        )

    elif cb.data == "close":
        await cb.message.delete(True)

    elif "|" in update.data:
        await update.message.edit(f"{update.data}")
        await youtube_dl_call_back(bot, update)
