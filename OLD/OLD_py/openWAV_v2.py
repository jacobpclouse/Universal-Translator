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
 

    # initialize the recognizer
    r = sr.Recognizer()


    # open the file
    with sr.AudioFile(tempFileName) as source:
        # listen for the data (load audio to memory)
        audio_data = r.record(source)
        # recognize (convert from speech to text)
        transcription = r.recognize_google(audio_data,language = sourceLang, show_all = True )
        print(transcription)
        print(type(transcription))
        
        if (transcription != "True"):
            print("Not equal to true")
        else:
            print("Equal to true")

        print(f"Transcript Keys: {transcription.keys()}") # finding keys

        # values are stored in dict in list in dict (who designed this??)
        alternatives = transcription['alternative']
        print(type(alternatives))
        alt1 = alternatives[1]
        print(type(alt1))
        translated_text = alt1['transcript']
        print(type(translated_text))
        print(translated_text)


    # # # save string to file

    text_file = open("outText.txt", "w")
    n = text_file.write(translated_text)
    text_file.close()


# -=-=-=-


sourcelang1 = 'en-US'
destlang1 = 'en-US'

filename1 = 'noSpeech.wav'

transcribe_languages(filename1,sourcelang1,destlang1)