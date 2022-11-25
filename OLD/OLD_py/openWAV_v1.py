# https://stackoverflow.com/questions/25672289/failed-to-open-file-file-wav-as-a-wav-due-to-file-does-not-start-with-riff-id

import os
from os import path
import datetime
from pydub import AudioSegment
import speech_recognition as sr

import librosa
import soundfile as sf
import wave



def transcribe_languages(filename,sourceLang,destLang):
    # YOU HAVE TO HAVE THE INCOME AUDIO IN A WAVE FORMAT!!!

    # printing out source and destination languages, file to open
    print(f"Source language: {sourceLang}")
    print(f"Destination language: {destLang}")
    file_path = f'./{filename}'
    tempFileName = 'tempfilename.wav'
    print(f"Opening: {file_path}")


    # convert to temp file
    # # https://stackoverflow.com/questions/25672289/failed-to-open-file-file-wav-as-a-wav-due-to-file-does-not-start-with-riff-id
    x,_ = librosa.load(file_path, sr=16000)
    sf.write(tempFileName, x, 16000)
    wave.open(tempFileName,'r')
    # sf.write(f'{filename}_tmp.wav', x, 16000)
    # wave.open(f'{filename}_tmp.wav','r')


    # initialize the recognizer
    r = sr.Recognizer()


    # open the file
    with sr.AudioFile(tempFileName) as source:
        # listen for the data (load audio to memory)
        audio_data = r.record(source)
        # recognize (convert from speech to text)
        text = r.recognize_google(audio_data)
        print(text)


# -=-=-=-


sourcelang1 = 'english'
destlang1 = 'spanish'

filename1 = 'engToeng.wav'

transcribe_languages(filename1,sourcelang1,destlang1)