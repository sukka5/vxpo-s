
import logging

from hachoir.parser import createParser
from hachoir.metadata import extractMetadata


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

  # Getting Video duration & other meta data for the video
def get_duration(filepath):
    print(filepath)
    metadata = extractMetadata(createParser(filepath))
    if metadata.has("duration"):
        return metadata.get('duration').seconds
    else:
      	return 0


def get_width_height(filepath):
    print(filepath)
    metadata = extractMetadata(createParser(filepath))
    if metadata.has("width") and metadata.has("height"):
        return metadata.get("width"), metadata.get("height")
    else:
      	return 1280, 720