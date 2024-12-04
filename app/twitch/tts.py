from gtts import gTTS
from app.style.better_print import try_print
import app.logging as log
import os
import sys
import re
from datetime import datetime


# generates the filename
def generate_filename():
    directory = 'auido path'
    highest_index = -1
    pattern = re.compile(r'tts_(\d+)\.mp3')
    
    for filename in os.listdir(directory):
        match = pattern.match(filename)
        if match:
            index = int(match.group(1))
            if index > highest_index:
                highest_index = index
    
    new_index = highest_index + 1
    return f'{directory}/tts_{new_index}.mp3'


# generates the filename for the archived tts audio files
def generate_archived_filename(username):
    directory = 'archived autdio path'
    date_and_time = datetime.now().strftime('%Y-%m-%d_%H.%M.%S')
    return f'{directory}/{date_and_time}_{username}.mp3'


# get the language from the text that was redeemed with the channel points | default language is german
def get_lang(text):
    try: 
        lang_dict = {
            'de': ['deutsch', 'de', 'german', 'ger'], 
            'en': ['englisch', 'en', 'englisch', 'us'], 
            'fr': ['französisch', 'fr', 'french'],
            'ru': ['russisch', 'ru', 'russian'],
            'it': ['italienisch', 'it', 'italian'],
            'ko': ['koreanisch', 'ko', 'korean'],
            'ja': ['japanisch', 'jp', 'japanese', 'ja'],
            'zh-CN': ['chinesisch', 'zh-ch','cn', 'chinese', 'chn'],
            'zh-TW': ['chinesisch (traditionell)', 'zh-tw','chinese (traditional)']
        }

        for true_lang in lang_dict:
            for word in lang_dict[f'{true_lang}']:
                if str(text).startswith(f'{word}:'):
                    _, text = text.split(' ', 1)
                    lang = f'{true_lang}'
                    return lang, text
                else:
                    lang = 'de'
        else:
            lang = 'de'

        return lang, text

    except Exception as err:
        error = f'[Twitch TTS] Error in get_lang: {err}'
        log.log_error(error)


# Google tts voice
def tts(text, username):
        lang, text = get_lang(text)

        filename = generate_filename()
        archived_filename = generate_archived_filename(username)

        tts = gTTS(text=text, lang=f'{lang}', slow=False)
        tts.save(filename)
        tts.save(archived_filename)





# Fehlt noch text translation und get_lang()
#from TTS.utils.synthesizer import Synthesizer
from pydub import AudioSegment


# saves a wav file from the custom tts model to a folder were the discord tts bot plays it
def tts_2(text, username):
    try:
        sys.stdout = open(os.devnull, 'w')

        tts_Toub_model = 'model path'
        tts_Toub_config = 'model config patj'
        vocoder_model = ''
        vocoder_config = ''
        
        synthesizer = Synthesizer(
            tts_checkpoint=tts_Toub_model,
            tts_config_path=tts_Toub_config,
            use_cuda=False
        )
        
        wav = synthesizer.tts(text)

        filename = generate_filename()
        archived_filename = generate_archived_filename(username)

        wav_path = f'{filename[:-4]}.wav'
        
        synthesizer.save_wav(wav, f'{wav_path}')
        synthesizer.save_wav(wav, f'{archived_filename[:-4]}.wav')


        mp3 = AudioSegment.from_wav(f'{wav_path}')
        mp3.export(f'{filename}', format="mp3")

        os.remove(wav_path)

        sys.stdout = sys.__stdout__

    except Exception as err:
        error = f'[Twitch TTS] Error in tts_2: {err}'
        log.log_error(error)





if __name__ == "__main__":
    tts('Test')
