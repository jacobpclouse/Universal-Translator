# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Importing Libraries / Modules 
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
from flask import Flask, flash, request, redirect, url_for, render_template,send_from_directory, jsonify
import os
from os import path
import datetime
from pydub import AudioSegment
import speech_recognition as sr

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


# --- Function to Transcribe Speech ---

def transcribe_languages(pathToFile,filename,sourceLang,destLang):

    # printing out source and destination languages, file to open
    print(f"Source language: {sourceLang}")
    print(f"Destination language: {destLang}")
    origFileToConvert = f'{pathToFile}{filename}.wav'
    print(f"Opening: {origFileToConvert}")

    # initialize the recognizer
    r = sr.Recognizer()


    # open the file
    with sr.AudioFile(origFileToConvert) as source:
        # listen for the data (load audio to memory)
        audio_data = r.record(source)
        # recognize (convert from speech to text)
        text = r.recognize_google(audio_data)
        print(text)

'''
def transcribe_languages(pathToFile,filename,sourceLang,destLang):

    # printing out source and destination languages
    print(f"Source language: {sourceLang}")
    print(f"Destination language: {destLang}")

    # convert mp3 file to wav
    transcribed_filename = f"transcribed_{filename}"
    # transcribe audio file                                                         
    AUDIO_FILE = f"{transcribed_filename}.wav"
    print(AUDIO_FILE)
    
    # converting
    sound = AudioSegment.from_mp3(f"{pathToFile}{filename}.mp3")
    sound.export(f"{pathToFile}{AUDIO_FILE}", format="wav")


    # use the audio file as the audio source                                        
    r = sr.Recognizer()
    with sr.AudioFile(f"{pathToFile}{AUDIO_FILE}") as source:
            audio = r.record(source)  # read the entire audio file                  

            transcription = "Transcription: " + r.recognize_google(audio)
            print(transcription)

    # save to file
    with open(os.path.abspath(f'{pathToFile}{transcribed_filename}.txt'), 'wb') as f:
        f.write(transcription)
'''    



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