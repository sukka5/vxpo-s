
import os
import json
import time
import shutil
import asyncio
import logging
import subprocess

from pyrogram.types import *
from datetime import datetime
from config import Config

from plugins.utitities import get_duration, get_width_height
from plugins.screenshot import take_screen_shot
from Translation import Translation
from plugins.random import random_char
from plugins.progress import progress_for_pyrogram, humanbytes

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


async def youtube_dl_call_back(bot, update):
    cb_data = update.data
    # youtube_dl extractors
    tg_send_type, youtube_dl_format, youtube_dl_ext, ranom = cb_data.split("|")
    print(cb_data)
    random1 = random_char(5)
    save_ytdl_json_path = Config.DOWNLOAD_LOCATION + \
        "/" + str(update.from_user.id) + f'{ranom}' + ".json"
    try:
        with open(save_ytdl_json_path, "r", encoding="utf8") as f:
            response_json = json.load(f)
            
    except (FileNotFoundError) as e:
        await update.message.delete()
        return False
    youtube_dl_url = update.message.reply_to_message.text
    custom_file_name = str(response_json.get("title")) + \
        "_" + youtube_dl_format + "." + youtube_dl_ext
    if "|" in youtube_dl_url:
        url_parts = youtube_dl_url.split("|")
        if len(url_parts) == 2:
            youtube_dl_url = url_parts[0]
            custom_file_name = url_parts[1]
            custom_caption = url_parts[2]
        if youtube_dl_url is not None:
            youtube_dl_url = youtube_dl_url.strip()
        if custom_file_name is not None:
            custom_file_name = custom_file_name.strip()
        # https://stackoverflow.com/a/761825/4723940

        logger.info(youtube_dl_url)
        logger.info(custom_file_name)
    else:
        for entity in update.message.reply_to_message.entities:
            if entity.type == "text_link":
                youtube_dl_url = entity.url
            elif entity.type == "url":
                o = entity.offset
                l = entity.length
                youtube_dl_url = youtube_dl_url[o:o + l]
    await update.message.edit_caption(
        caption=Translation.DOWNLOAD_START.format(custom_file_name)

    )
    description = Translation.CUSTOM_CAPTION_UL_FILE
    if custom_file_name:
        description = f"▪️**{custom_caption}**"
        # escape Markdown and special characters
    tmp_directory_for_each_user = Config.DOWNLOAD_LOCATION + \
        "/" + str(update.from_user.id) + f'{random1}'
    if not os.path.isdir(tmp_directory_for_each_user):
        os.makedirs(tmp_directory_for_each_user)
    download_directory = f"{tmp_directory_for_each_user}/{custom_file_name}"

    command_to_exec = []
    if tg_send_type == "audio":
        print("fuuuccck!")
    else:
        # command_to_exec = ["yt-dlp", "-f", youtube_dl_format, "--hls-prefer-ffmpeg", "--recode-video", "mp4", "-k", youtube_dl_url, "-o", download_directory]
        minus_f_format = youtube_dl_format
        command_to_exec = [
            "youtube-dl",
            "-c",
            "--max-filesize", str(Config.TG_MAX_FILE_SIZE),
            "--embed-subs",
            "-f", minus_f_format,
            "--hls-prefer-ffmpeg", youtube_dl_url,
            "-o", download_directory
        ]

    command_to_exec.append("--no-warnings")
    # command_to_exec.append("--quiet")
    logger.info(command_to_exec)
    start = datetime.now()
    process = await asyncio.create_subprocess_exec(
        *command_to_exec,
        # stdout must a pipe to be accessible as process.stdout
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    # Wait for the subprocess to finish
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()
    logger.info(e_response)
    logger.info(t_response)
    ad_string_to_replace = "please report this issue on https://yt-dl.org/bug . Make sure you are using the latest version; see  https://yt-dl.org/update  on how to update. Be sure to call youtube-dl with the --verbose flag and include its complete output."
    if e_response and ad_string_to_replace in e_response:
        error_message = e_response.replace(ad_string_to_replace, "")
        await update.message.edit_caption(

            text=error_message
        )
        return False

    if t_response:
        logger.info(t_response)
        try:
            os.remove(save_ytdl_json_path)
        except FileNotFoundError as exc:
            pass

        end_one = datetime.now()
        time_taken_for_download = (end_one - start).seconds
        file_size = Config.TG_MAX_FILE_SIZE + 1
        try:
            file_size = os.stat(download_directory).st_size
        except FileNotFoundError as exc:
            download_directory = os.path.splitext(
                download_directory)[0] + "." + "mkv"
            # https://stackoverflow.com/a/678242/4723940
            file_size = os.stat(download_directory).st_size
        if ((file_size > Config.TG_MAX_FILE_SIZE)):
            await update.message.edit_caption(

                caption=Translation.RCHD_TG_API_LIMIT.format(
                    time_taken_for_download, humanbytes(file_size))

            )
        else:
            await update.message.edit_caption(
                caption=Translation.UPLOAD_START.format(custom_file_name)

            )
            
            # ref: message from @Sources_codes
            start_time = time.time()
            thumb = await take_screen_shot(download_directory, tmp_directory_for_each_user)
            width, height = get_width_height(download_directory)
            duration = get_duration(download_directory)
            await update.message.reply_video(
                    # chat_id=update.message.chat.id,
                video=download_directory,
                caption=description,
                duration=duration,
                width=width,
                height=height,
                thumb=thumb,
                supports_streaming=True,
                    # reply_to_message_id=update.id,
                progress=progress_for_pyrogram,
                progress_args=(
                    Translation.UPLOAD_START,
                    update.message,
                    start_time
                )
            )
            end_two = datetime.now()
            time_taken_for_upload = (end_two - end_one).seconds
            try:
                shutil.rmtree(tmp_directory_for_each_user)
            except Exception:
                pass
            await update.message.edit_caption(
                caption=Translation.AFTER_SUCCESSFUL_UPLOAD_MSG_WITH_TS.format(
                    time_taken_for_download, time_taken_for_upload)

            )

            logger.info(f"Downloaded in: {str(time_taken_for_download)}")
            logger.info(f"Uploaded in: {str(time_taken_for_upload)}")
