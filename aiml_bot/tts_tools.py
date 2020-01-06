
import os
import subprocess
import tempfile

from gtts import gTTS
from io import BytesIO
from pydub import AudioSegment


def text_to_voice(text, lang, file_name):
    mp3_file_name = f'{file_name}.mp3'
    ogg_file_name = f'{file_name}.ogg'

    mp3_fp = BytesIO()
    tts = gTTS(text, lang=lang)
    tts.save(mp3_file_name)

    devnull = open(os.devnull, 'w')
    subprocess.run(["ffmpeg", '-i', mp3_file_name, '-acodec', 'libopus', ogg_file_name, '-y'], stdout=devnull)
    os.remove(mp3_file_name)

