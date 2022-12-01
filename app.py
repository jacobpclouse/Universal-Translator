# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Importing Libraries / Modules 
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
from flask import Flask, flash, request, redirect, url_for, render_template,send_from_directory, jsonify, Response
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
from gtts import gTTS
from pathlib import Path
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Variables
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# paths to JSON files stored in vars
JSONSourceLanguagesPath = './static/assets/languages.json'
JSONgTTSPath = './static/assets/languagesOrig.json'

# File and folder Names
textToReturnToFrontEnd = "RETURNTHISTEXTTOFRONTEND"
mp3ToReturnToFrontEnd = "RETURNTHISMP3TOFRONTEND"
uploadFolderPath = "./UPLOADS/"
storeSourceLang = 'sourceLang'
storeDestLang = 'destLang'

ALLOWED_EXTENSIONS = set(['txt'])

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Functions
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# --- Function used to find ending type for file AND checking to make sure that it is an allowed type
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# --- Function used to find ending type for file only (for creating temp file in UPLOADS)
def getExtension(inputFile):
    return '.' and inputFile.rsplit(".",1)[1].lower()


# --- Function to delete files inside directory (without deleting directory itself) ---
def emptyFolder(directoryPath):
    [f.unlink() for f in Path(directoryPath).glob("*") if f.is_file()] 


# --- Function to Defang date time ---
def defang_datetime():
    current_datetime = f"_{datetime.datetime.now()}"

    current_datetime = current_datetime.replace(":","_")
    current_datetime = current_datetime.replace(".","-")
    current_datetime = current_datetime.replace(" ","_")
    
    return current_datetime


# --- Function to get JSON abbr of source language for Google speech to text ---
def getSourceLangAbbr(fullSourceLang,pathToJson):
    # Opening JSON file
    JSONlangFile = open(pathToJson)
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

    # getting abreviation for source lang
    AbbrSourceLang = getSourceLangAbbr(sourceLang,JSONSourceLanguagesPath)


    # printing out source and destination languages, file to open
    print(f"Source language: {sourceLang}")
    print(f"Destination language: {destLang}")
    print(f"Abbr Source Lang: {AbbrSourceLang}")
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
        #transcription = r.recognize_google(audio_data,language = sourceLang, show_all = True )
        transcription = r.recognize_google(audio_data,language = AbbrSourceLang, show_all = True )
        print(transcription)
        print(type(transcription))

        #if transcription is a dictionary file (ie: has data) or a list (ie: empty result)
        if (type(transcription) is dict):
            print("Valid Dict condition triggered")
            print(f"Transcript Keys: {transcription.keys()}") # finding keys

            # values are stored in dict in list in dict (who designed this??)
            alternatives = transcription['alternative']
            print(type(alternatives))
            print(f"In Alternatives we see: {alternatives}")
            #alt1 = alternatives[1]
            alt1 = alternatives[0]
            print(type(alt1))
            transcribed_text = alt1['transcript']
            print(type(transcribed_text))
            print(transcribed_text)

            # translating data
            translated = MyMemoryTranslator(source=sourceLang, target=destLang).translate(text=transcribed_text)


            # converting to speech in destination language
            AbbrgTTSLang = getSourceLangAbbr(destLang,JSONgTTSPath)
            textToSpeech = gTTS(translated, lang=AbbrgTTSLang)
            # textToSpeech.save(f'{pathToFile}outText_{filename}.mp3')
            #textToSpeech.save(f'{pathToFile}RETURNTOFRONTEND.mp3')
            textToSpeech.save(f'{pathToFile}{mp3ToReturnToFrontEnd}.mp3')

        else:
            print(f"Not a Dict type -- \n type is: {type(transcription)}")
            translated = f"nothing in translated text or can't make it out, type was {type(transcription)}"

            # converting to speech - use english as it failed
            textToSpeech = gTTS(translated, lang='en')
            # textToSpeech.save(f'outText_{filename}.mp3')
            #textToSpeech.save(f'{pathToFile}RETURNTOFRONTEND.mp3')
            textToSpeech.save(f'{pathToFile}{mp3ToReturnToFrontEnd}.mp3')

    # # # save string to file
    text_file = open(f"{pathToFile}{textToReturnToFrontEnd}.txt", "w")
    n = text_file.write(translated)
    text_file.close()
    return translated
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Routes
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
@app.route('/',methods=['GET', 'POST'])
@app.route('/audioUpload',methods=['GET', 'POST'])
def translate():
    dashboardHeader = "Speech to Speech" # in base temp, basically what this page does
    title = "Speech to Speech - Jacob Clouse Universal Translator" # in base temp, actual page title in browser
    
    returned_translated = "Translated text will display here"

    # uploadFolderPath = "./UPLOADS/"

    if request.method == 'POST':
        # Grab current date & time from function & store in variable
        use_this_datetime = defang_datetime()
        print(use_this_datetime)
        # outputWAVName = f'output{use_this_datetime}'
        outputWAVName = f'output_File'

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


       
        # save sound to file
        with open(os.path.abspath(f'{uploadFolderPath}{outputWAVName}.wav'), 'wb') as f:
            f.write(audioRecordingData)

        # save souce to file
        text_file_source = open(f"{uploadFolderPath}{storeSourceLang}.txt", "w")
        z = text_file_source.write(sourceLanguage)
        print(z)
        text_file_source.close()

        # save destination to file
        text_file_dest = open(f"{uploadFolderPath}{storeDestLang}.txt", "w")
        y = text_file_dest.write(destinationLanguage)
        print(y)
        text_file_dest.close()

        # execute transcription function
        returned_translated = transcribe_languages(uploadFolderPath,outputWAVName,sourceLanguage,destinationLanguage)
        print(returned_translated)
        # 

# """ This Will let the user download the file, then deletes all files in outbound and uploads """
            
    # flash(returned_translated)
    return render_template('translate.html', html_title = title, dash_head = dashboardHeader, translated = returned_translated)




# Route used after initial submit that grabs translations and data
@app.route('/returnResults',methods=['GET', 'POST'])
def seperateRoute():
    print("Seperate Route, opening up files")
    # uploadFolderPath = "./UPLOADS/"

    dashboardHeader = "Speech to Speech" # in base temp, basically what this page does
    title = "Speech to Speech - Jacob Clouse Universal Translator" # in base temp, actual page title in browser
    
    """ PUT AN IF EMPTY CATCH STATEMENT HERE for empty uploads """

    # getting data to send
    openedFile = open(f"{uploadFolderPath}{textToReturnToFrontEnd}.txt", "r")
    returned_translated = openedFile.read()
    print(f"Translated Text: {returned_translated}")

    # Swap languages - open source and dest files
    previousSourceFile = open(f"{uploadFolderPath}{storeSourceLang}.txt", "r")
    previousSource = previousSourceFile.read()
    print(f"Previous Source: {previousSource}")

    previousDestFile = open(f"{uploadFolderPath}{storeDestLang}.txt", "r")
    previousDest = previousDestFile.read()
    print(f"Previous Source: {previousDest}")

    
    return render_template('returnTranslated.html', html_title = title, dash_head = dashboardHeader, translated = returned_translated, prev_source_lang = previousSource, prev_dest_lang = previousDest)



# this route will open up a sepearate page and return the translation
@app.route('/wav',methods=['GET', 'POST'])
def getWav():
    """ PUT AN IF EMPTY CATCH STATEMENT HERE for empty uploads """
    def generate():
        with open(f"{uploadFolderPath}{mp3ToReturnToFrontEnd}.mp3", "rb") as fmp3:
            data = fmp3.read(1024)
            while data:
                yield data
                data = fmp3.read(1024)
    return Response(generate(), mimetype="audio/mp3")



# this route will allow user to upload a file, translate it and download it
@app.route('/fileUpload',methods=['GET', 'POST'])
def fileUpload():

    dashboardHeader = "Text File Upload" # in base temp, basically what this page does
    title = "Text File Upload - Jacob Clouse Universal Translator" # in base temp, actual page title in browser
    
    # for post data from form
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            # GRABBING FORM INFO -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
            # getting input with source = sourceLangID in HTML form
            source_lang = request.form.get("sourceLangID")
            # getting input with dest = destinationLangID in HTML form
            destination_lang = request.form.get("destinationLangID")

            secureTheFile = secure_filename(file.filename)
            extensionType = getExtension(secureTheFile)

            # Filename below - Important for functions 
            filename = "Temp_Pic_Upload." + extensionType

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            uploaded_file = secureTheFile

    ''' OPEN DOC, CONVERT FROM SOURCE LANGUAGE TO DEST LANGUAGE, SAVE TO FILE, RETURN '''

    return render_template('fileUpload.html', html_title = title, dash_head = dashboardHeader)


# main statement - used to set dev mode
if __name__ == '__main__':
    app.run(debug=True)