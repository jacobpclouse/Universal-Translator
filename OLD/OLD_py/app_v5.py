# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Importing Libraries / Modules 
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
from flask import Flask, flash, request, redirect, url_for, render_template,send_from_directory, jsonify
import os
from os import path
import datetime
from pydub import AudioSegment
import speech_recognition as sr
import librosa
import soundfile as sf
import wave
from deep_translator import MyMemoryTranslator
import json

app = Flask(__name__)


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Functions
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# --- Function to Defang date time ---
def defang_datetime():
    current_datetime = f"_{datetime.datetime.now()}"

    current_datetime = current_datetime.replace(":","_")
    current_datetime = current_datetime.replace(".","-")
    current_datetime = current_datetime.replace(" ","_")
    
    return current_datetime


# --- Function to get JSON abbr of source language for Google speech to text ---
def getSourceLangAbbr(fullSourceLang):
    # Opening JSON file
    JSONlangFile = open('./static/assets/languages.json')
    # returns JSON object as a dictionary
    JSONlangFiledata = json.load(JSONlangFile)
  
    # get abbriviation 
    JSONAbbreviation = JSONlangFiledata[fullSourceLang]
    print(f"JSON Abbr for {fullSourceLang} is {JSONAbbreviation}")
    
    # Closing file and return value
    JSONlangFile.close()
    return JSONAbbreviation



# --- Function to Transcribe Speech ---
def transcribe_languages(pathToFile,filename,sourceLang,destLang):

    # printing out source and destination languages, file to open
    print(f"Source language: {sourceLang}")
    print(f"Destination language: {destLang}")
    origFileToConvert = f'{pathToFile}{filename}.wav'


    tempFileName = f'temp_{filename}.wav'
    print(f"Opening: {origFileToConvert}")

    # convert to temp file
    # # https://stackoverflow.com/questions/25672289/failed-to-open-file-file-wav-as-a-wav-due-to-file-does-not-start-with-riff-id
    x,_ = librosa.load(origFileToConvert, sr=16000)
    sf.write(f"{pathToFile}{tempFileName}", x, 16000)
    wave.open(f"{pathToFile}{tempFileName}",'r')

    # initialize the recognizer
    r = sr.Recognizer()

    # open the file
    with sr.AudioFile(f"{pathToFile}{tempFileName}") as source:
        # listen for the data (load audio to memory)
        audio_data = r.record(source)

        # Show_all will return a dict with a list with a dict inside that has your data
        transcription = r.recognize_google(audio_data,language = sourceLang, show_all = True )
        print(transcription)
        print(type(transcription))

        #if transcription is a dictionary file (ie: has data) or a list (ie: empty result)
        if (type(transcription) is dict):
            print("Valid Dict condition triggered")
            print(f"Transcript Keys: {transcription.keys()}") # finding keys

            # values are stored in dict in list in dict (who designed this??)
            alternatives = transcription['alternative']
            print(type(alternatives))
            alt1 = alternatives[1]
            print(type(alt1))
            translated_text = alt1['transcript']
            print(type(translated_text))
            print(translated_text)
        else:
            print(f"Not a Dict type -- \n type is: {type(transcription)}")
            translated_text = f"nothing in translated text or can't make it out, type was {type(transcription)}"


    # # # save string to file

    text_file = open(f"outText_{filename}.txt", "w")
    n = text_file.write(translated_text)
    text_file.close()




# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Routes
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
@app.route('/',methods=['GET', 'POST'])
@app.route('/audioUpload',methods=['GET', 'POST'])
def translate():
    dashboardHeader = "Speech to Speech" # in base temp, basically what this page does
    title = "Speech to Speech - Jacob Clouse Universal Translator" # in base temp, actual page title in browser
    
    uploadFolderPath = "./UPLOADS/"

    if request.method == 'POST':
        # Grab current date & time from function & store in variable
        use_this_datetime = defang_datetime()
        outputWAVName = f'output{use_this_datetime}'

        # had issues importing audio data below, used this link to gather data: https://stackoverflow.com/questions/65632555/sending-wav-file-from-frontend-to-flask-backend
        print(request.files)
        audioRecordingData = request.files['audio-file'].read()
        print(request.data)
        print(request.form) # form data incoming as this


        # print(audioRecordingData)
        defaultSourceValue = 'English'
        defaultDestinationValue = 'Spanish'

        # recieving source and destination data from form data (have default values just in case)
        sourceLanguage = request.form.get('source-language',defaultSourceValue)
        destinationLanguage = request.form.get('destination-language',defaultDestinationValue)
        print(sourceLanguage)
        print(destinationLanguage)

       
        # save to file
        # with open(os.path.abspath(f'{uploadFolderPath}{outputMP3Name}.mp3'), 'wb') as f:
        with open(os.path.abspath(f'{uploadFolderPath}{outputWAVName}.wav'), 'wb') as f:
            f.write(audioRecordingData)



        # execute transcription function
        transcribe_languages(uploadFolderPath,outputWAVName,sourceLanguage,destinationLanguage)

    return render_template('translate.html', html_title = title, dash_head = dashboardHeader)



# main statement - used to set dev mode
if __name__ == '__main__':
    app.run(debug=True)