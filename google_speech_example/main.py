from gtts import gTTS
from io import BytesIO

mp3_fp = BytesIO()
tts = gTTS('привет, мир', lang='ru')
tts.save('hello.mp3')
