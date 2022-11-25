# https://stackoverflow.com/questions/25672289/failed-to-open-file-file-wav-as-a-wav-due-to-file-does-not-start-with-riff-id

import os
from os import path
import datetime
from pydub import AudioSegment
import speech_recognition as sr

import json

import librosa
import soundfile as sf
import wave

from deep_translator import MyMemoryTranslator

# --- Function to get JSON abbr of source language for Google speech to text ---
def getSourceLangAbbr(fullSourceLang):
    # Opening JSON file
    JSONlangFile = open('../../Languages/languages.json')
    # returns JSON object as a dictionary
    JSONlangFiledata = json.load(JSONlangFile)
  
    # get abbriviation 
    JSONAbbreviation = JSONlangFiledata[fullSourceLang]
    print(f"JSON Abbr for {fullSourceLang} is {JSONAbbreviation}")
    
    # Closing file and return value
    JSONlangFile.close()
    return JSONAbbreviation


# --- Function to Transcribe Speech ---
def transcribe_languages(filename,sourceLang,destLang):
    # YOU HAVE TO HAVE THE INCOME AUDIO IN A WAVE FORMAT!!!
    
    # getting abreviation for source lang
    AbbrSourceLang = getSourceLangAbbr(sourceLang)

    # printing out source and destination languages, file to open
    print(f"Source language: {sourceLang}")
    print(f"Destination language: {destLang}")
    print(f"Abbr Source Lang: {AbbrSourceLang}")
    file_path = f'./{filename}.wav'
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
        transcription = r.recognize_google(audio_data,language = AbbrSourceLang, show_all = True )
        print(transcription)
        findType = type(transcription)
        print(findType)

        
        
        #if empty file with no words
        if (type(transcription) is dict):
            print("Valid Dict condition triggered")
            print(f"Transcript Keys: {transcription.keys()}") # finding keys

            # values are stored in dict in list in dict (who designed this??)
            alternatives = transcription['alternative']
            print(type(alternatives))
            alt1 = alternatives[1]
            print(type(alt1))
            transcribed_text = alt1['transcript']
            print(type(transcribed_text))
            print(transcribed_text)

            # translating data
            translated = MyMemoryTranslator(source="english", target=destLang).translate(text=transcribed_text)

        else:
            print(f"Not a Dict type -- \n type is: {findType}")
            translated = f"nothing in translated text or can't make it out, type was {findType}"


    # # # save string to file

    text_file = open(f"outText_{filename}.txt", "w")
    n = text_file.write(translated)
    text_file.close()


# -=-=-=-


sourcelang1 = 'english'
destlang1 = 'marathi'

filename1 = 'noSpeech'
filename2 = 'engToeng'


transcribe_languages(filename1,sourcelang1,destlang1)
transcribe_languages(filename2,sourcelang1,destlang1)