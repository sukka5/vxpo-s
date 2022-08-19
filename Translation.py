from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class Translation(object):

    PROGRESS = """
**Speed** ➥ {3}/s\n
**Done** ➥ {1}\n
**Size** ➥ {2}\n
**Time left** ➥ {4}\n\n
"""

    START_BUTTONS = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton('❓ Help', callback_data='help'),
            InlineKeyboardButton('🦊 About', callback_data='about')
        ], [
            InlineKeyboardButton('📛 Close', callback_data='close')
        ]]
    )
    HELP_BUTTONS = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton('🏠 Home', callback_data='home'),
            InlineKeyboardButton('🦊 About', callback_data='about')
        ], [
            InlineKeyboardButton('📛 Close', callback_data='close')
        ]]
    )
    ABOUT_BUTTONS = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton('🏠 Home', callback_data='home'),
            InlineKeyboardButton('❓ Help', callback_data='help')
        ], [
            InlineKeyboardButton('📛 Close', callback_data='close')
        ]]
    )
    BUTTONS = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton('📛 Close', callback_data='close')
        ]]
    )
    FORMAT_SELECTION = "**Now Select the desired format**"
    SET_CUSTOM_USERNAME_PASSWORD = """"""
    DOWNLOAD_START = "**Downloading** ⌛ {}\n\n__If the processing message stays for long and your document doesn't get uploaded by me, Try again with few meniutes__ </i>"
    UPLOAD_START = "➥ {} \n\n📤 **Uploading Please Wait**"
    RCHD_TG_API_LIMIT = "Downloaded in {} seconds.\nDetected File Size: {}\nSorry. But, I cannot upload files greater than 2GB due to Telegram API limitations."
    AFTER_SUCCESSFUL_UPLOAD_MSG_WITH_TS = "Downloaded in ➥ {} Seconds\nUploaded in ➥ {} seconds"
    FF_MPEG_DEL_ETED_CUSTOM_MEDIA = "✅ Media cleared succesfully."
    CUSTOM_CAPTION_UL_FILE = " "
    NO_VOID_FORMAT_FOUND = "ERROR... <code>{}</code>"
    SLOW_URL_DECED = "Gosh that seems to be a very slow URL. Since you were screwing my home, I am in no mood to download this file. Meanwhile, why don't you try this:==> https://shrtz.me/PtsVnf6 and get me a fast URL so that I can upload to Telegram, without me slowing down for other users."
